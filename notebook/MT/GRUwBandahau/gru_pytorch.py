import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
        super(Encoder, self).__init__()
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim, enc_units, batch_first=True)
        
    def forward(self, x, hidden):
        # x shape: (batch_size, seq_length)
        x = self.embedding(x)  # (batch_size, seq_length, embedding_dim)
        output, state = self.gru(x, hidden)
        return output, state
    
    def initialize_hidden_state(self, device, batch_size=None):
        # Use provided batch_size if available, otherwise use the default
        batch_sz = batch_size if batch_size is not None else self.batch_sz
        return torch.zeros((1, batch_sz, self.enc_units), device=device)
    
class Decoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim + dec_units, dec_units, batch_first=True)
        self.fc = nn.Linear(dec_units, vocab_size)
        
        # used for attention
        self.W1 = nn.Linear(dec_units, dec_units)
        self.W2 = nn.Linear(dec_units, dec_units)
        self.V = nn.Linear(dec_units, 1)
        
    def forward(self, x, hidden, enc_output):
        """
        Forward pass for the decoder
        
        Args:
            x: Input tensor of shape (batch_size, 1)
            hidden: Hidden state tensor of shape (1, batch_size, dec_units)
            enc_output: Encoder output tensor of shape (batch_size, max_length, enc_units)
            
        Returns:
            x: Output tensor of shape (batch_size, vocab_size)
            state: Updated hidden state
            attention_weights: Attention weights for visualization
        """
        # x shape: (batch_size, 1)
        # hidden shape: (1, batch_size, dec_units)
        # enc_output shape: (batch_size, max_length, enc_units)
        
        # Add time axis to hidden state
        # hidden shape: (1, batch_size, dec_units) -> (batch_size, 1, dec_units)
        hidden_with_time_axis = hidden.transpose(0, 1)
        
        # score shape == (batch_size, max_length, 1)
        # we get 1 at the last axis because we are applying tanh(FC(EO) + FC(H)) to self.V
        score = self.V(torch.tanh(self.W1(enc_output) + self.W2(hidden_with_time_axis)))
        
        # attention_weights shape == (batch_size, max_length, 1)
        attention_weights = F.softmax(score, dim=1)
        
        # context_vector shape after sum == (batch_size, dec_units)
        context_vector = attention_weights * enc_output
        context_vector = context_vector.sum(dim=1)  # sum along max_length dimension
        
        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        x = self.embedding(x)
        
        # Add time dimension to context_vector to match x's shape
        # context_vector shape: (batch_size, dec_units) -> (batch_size, 1, dec_units)
        context_vector = context_vector.unsqueeze(1)
        
        # x shape after concatenation == (batch_size, 1, embedding_dim + dec_units)
        x = torch.cat([context_vector, x], dim=2)
        
        # passing the concatenated vector to the GRU
        output, state = self.gru(x, hidden)
        
        # output shape == (batch_size, 1, dec_units)
        # reshape to (batch_size * 1, dec_units)
        output = output.reshape(-1, output.shape[2])
        
        # output shape == (batch_size * 1, vocab_size)
        x = self.fc(output)
        
        return x, state, attention_weights
        
    def initialize_hidden_state(self, device):
        return torch.zeros((1, self.batch_sz, self.dec_units), device=device)

#putting the model tgt
class EncoderDecoder(nn.Module):
    def __init__(self, input_vocab_size, output_vocab_size, embedding_dim, units, batch_size, 
                 max_length_input, max_length_output, device, start_token_id, end_token_id):
        super(EncoderDecoder, self).__init__()
        self.encoder = Encoder(input_vocab_size, embedding_dim, units, batch_size)
        self.decoder = Decoder(output_vocab_size, embedding_dim, units, batch_size)
        self.max_length_input = max_length_input
        self.max_length_output = max_length_output
        self.device = device
        self.start_token_id = start_token_id
        self.end_token_id = end_token_id
        
    def forward(self, inputs, targets=None, teacher_forcing_ratio=0.5):
        batch_size = inputs.size(0)  # Get actual batch size from input
        
        # Initialize encoder hidden state with actual batch size
        enc_hidden = self.encoder.initialize_hidden_state(self.device, batch_size)
        
        # Encoder forward pass
        enc_output, enc_hidden = self.encoder(inputs, enc_hidden)
        
        # Initialize decoder hidden state with encoder's final hidden state
        dec_hidden = enc_hidden
        
        # Initialize decoder input with start token
        dec_input = torch.tensor([[self.start_token_id]], device=self.device).repeat(batch_size, 1)
        
        # Initialize output tensor
        outputs = torch.zeros(batch_size, self.max_length_output, self.decoder.fc.out_features, device=self.device)
        attention_weights = torch.zeros(batch_size, self.max_length_output, self.max_length_input, device=self.device)
        
        # Decoder forward pass
        for t in range(self.max_length_output):
            # Decoder step
            dec_output, dec_hidden, attention = self.decoder(dec_input, dec_hidden, enc_output)
            
            # Store output
            outputs[:, t, :] = dec_output
            
            # Store attention weights
            attention_weights[:, t, :] = attention.squeeze(-1)
            
            # Teacher forcing: use target as next input with probability teacher_forcing_ratio
            if targets is not None and torch.rand(1).item() < teacher_forcing_ratio:
                dec_input = targets[:, t].unsqueeze(1)
            else:
                # Use predicted token as next input
                dec_input = dec_output.argmax(dim=1).unsqueeze(1)
                
        return outputs, attention_weights
    
    def predict(self, inputs, max_length=None):
        
        if max_length is None:
            max_length = self.max_length_output
            
        batch_size = inputs.size(0)
        
        # Initialize encoder hidden state
        enc_hidden = self.encoder.initialize_hidden_state(self.device, batch_size)
        
        # Encoder forward pass
        enc_output, enc_hidden = self.encoder(inputs, enc_hidden)
        
        # Initialize decoder hidden state with encoder's final hidden state
        dec_hidden = enc_hidden
        
        # Initialize decoder input with start token
        dec_input = torch.tensor([[self.start_token_id]], device=self.device).repeat(batch_size, 1)
        
        # Initialize output tensor
        predicted_ids = torch.zeros(batch_size, max_length, dtype=torch.long, device=self.device)
        attention_weights = torch.zeros(batch_size, max_length, self.max_length_input, device=self.device)
        
        # Decoder forward pass
        for t in range(max_length):
            # Decoder step
            dec_output, dec_hidden, attention = self.decoder(dec_input, dec_hidden, enc_output)
            
            # Store predicted token ID and attention weights
            predicted_ids[:, t] = dec_output.argmax(dim=1)
            attention_weights[:, t, :] = attention.squeeze(-1)
            
            # Use predicted token as next input
            dec_input = dec_output.argmax(dim=1).unsqueeze(1)
            
            # Stop if end token is predicted
            if (predicted_ids[:, t] == self.end_token_id).all():
                break
                
        return predicted_ids, attention_weights

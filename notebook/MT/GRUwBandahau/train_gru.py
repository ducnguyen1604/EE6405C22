import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import pickle
import pandas as pd

# Import the model
from gru_pytorch import EncoderDecoder

# Hyperparameter configuration
HYPERPARAMETERS = {
    # Data paths
    'train_path': '../data/it_train.csv',
    'val_path': '../data/it_val.csv',
    'test_path': '../data/it_test.csv',
    'output_dir': './models',
    

    'vocab_size': 10000,
    'embedding_dim': 256,
    'units': 1024,
    'batch_size': 64,
    

    'epochs': 50,
    'learning_rate': 0.001,
    'clip': 1.0,
    'teacher_forcing_ratio': 0.5,
    'save_every': 5,
    'seed': 42,
    'no_cuda': False,
    
    
    'dropout': 0.1,
    'early_stopping_patience': 5,
    'scheduler_factor': 0.1,
    'scheduler_patience': 2,
    'warmup_epochs': 2
}

# Set random seeds for reproducibility
def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Custom dataset class for translation data
class TranslationDataset(Dataset):
    def __init__(self, source_data, target_data, source_vocab, target_vocab, max_length_source, max_length_target):
        self.source_data = source_data
        self.target_data = target_data
        self.source_vocab = source_vocab
        self.target_vocab = target_vocab
        self.max_length_source = max_length_source
        self.max_length_target = max_length_target
        
        # Get special token IDs
        self.start_token_id = self.target_vocab.get('<start>', 2)
        self.end_token_id = self.target_vocab.get('<end>', 3)
        
    def __len__(self):
        return len(self.source_data)
    
    def __getitem__(self, idx):
        source_text = self.source_data[idx]
        target_text = self.target_data[idx]
        
        # Convert text to token IDs
        source_ids = [self.source_vocab.get(token, self.source_vocab.get('<unk>', 1)) for token in source_text.split()]
        target_ids = [self.target_vocab.get(token, self.target_vocab.get('<unk>', 1)) for token in target_text.split()]
        
        # Add start and end tokens to target
        target_ids = [self.start_token_id] + target_ids + [self.end_token_id]
        
        # Pad sequences to max length
        source_ids = source_ids + [0] * (self.max_length_source - len(source_ids))
        target_ids = target_ids + [0] * (self.max_length_target - len(target_ids))
        
        # Convert to tensors
        source_tensor = torch.tensor(source_ids, dtype=torch.long)
        target_tensor = torch.tensor(target_ids, dtype=torch.long)
        
        return source_tensor, target_tensor

# Collate function for batching
def collate_fn(batch):
    source_batch, target_batch = zip(*batch)
    # No need to pad here since we already padded in the dataset
    source_batch = torch.stack(source_batch)
    target_batch = torch.stack(target_batch)
    return source_batch, target_batch

def load_data(train_path, val_path, test_path, vocab_size=10000):
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETLoad data from CSV files and create vocabulariesREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    # Load CSV files
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)
    
    # Extract data and target texts
    train_source = train_df['data'].tolist()
    train_target = train_df['target'].tolist()
    val_source = val_df['data'].tolist()
    val_target = val_df['target'].tolist()
    test_source = test_df['data'].tolist()
    test_target = test_df['target'].tolist()
    
    # Create vocabularies
    source_vocab = {'<pad>': 0, '<unk>': 1}
    target_vocab = {'<pad>': 0, '<unk>': 1, '<start>': 2, '<end>': 3}
    
    # Count word frequencies (using training data only)
    source_word_freq = {}
    target_word_freq = {}
    
    for text in train_source:
        for word in text.split():
            source_word_freq[word] = source_word_freq.get(word, 0) + 1
    
    for text in train_target:
        for word in text.split():
            target_word_freq[word] = target_word_freq.get(word, 0) + 1
    
    # Sort words by frequency
    source_words = sorted(source_word_freq.items(), key=lambda x: x[1], reverse=True)
    target_words = sorted(target_word_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Add top words to vocabularies
    for word, _ in source_words[:vocab_size-2]:
        source_vocab[word] = len(source_vocab)
    
    for word, _ in target_words[:vocab_size-4]:
        target_vocab[word] = len(target_vocab)
    
    # Calculate max lengths from all splits
    all_source = train_source + val_source + test_source
    all_target = train_target + val_target + test_target
    
    # Calculate max lengths including padding
    max_length_source = max(len(text.split()) for text in all_source)
    max_length_target = max(len(text.split()) for text in all_target) + 2  # +2 for <start> and <end> tokens
    
    print(fREMOVED_SECRETMax source length: {max_length_source}REMOVED_SECRET)
    print(fREMOVED_SECRETMax target length: {max_length_target}REMOVED_SECRET)
    
    return (train_source, train_target, val_source, val_target, test_source, test_target,
            source_vocab, target_vocab, max_length_source, max_length_target)

# Training function
def train_epoch(model, dataloader, optimizer, criterion, device, clip=1.0, teacher_forcing_ratio=0.5):
    model.train()
    epoch_loss = 0
    
    for batch_idx, (source, target) in enumerate(tqdm(dataloader, desc=REMOVED_SECRETTrainingREMOVED_SECRET)):
        source = source.to(device)
        target = target.to(device)
        
        # Forward pass
        output, _ = model(source, target, teacher_forcing_ratio)
        
        # Reshape output and target for loss calculation
        output = output.view(-1, output.shape[-1])
        target = target.view(-1)
        
        # Calculate loss
        loss = criterion(output, target)
        
        # Backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        
        optimizer.step()
        
        epoch_loss += loss.item()
    
    return epoch_loss / len(dataloader)

# Validation function
def validate(model, dataloader, criterion, device):
    model.eval()
    val_loss = 0
    
    with torch.no_grad():
        for source, target in tqdm(dataloader, desc=REMOVED_SECRETValidationREMOVED_SECRET):
            source = source.to(device)
            target = target.to(device)
            
            # Forward pass
            output, _ = model(source, target, teacher_forcing_ratio=1.0)
            
            # Reshape output and target for loss calculation
            output = output.view(-1, output.shape[-1])
            target = target.view(-1)
            
            # Calculate loss
            loss = criterion(output, target)
            val_loss += loss.item()
    
    return val_loss / len(dataloader)

# Function to save model and vocabulary
def save_model(model, source_vocab, target_vocab, optimizer, epoch, loss, save_path):
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'epoch': epoch,
        'loss': loss,
        'source_vocab': source_vocab,
        'target_vocab': target_vocab,
        'model_config': {
            'input_vocab_size': model.encoder.embedding.num_embeddings,
            'output_vocab_size': model.decoder.embedding.num_embeddings,
            'embedding_dim': model.encoder.embedding.embedding_dim,
            'units': model.encoder.enc_units,
            'batch_size': model.encoder.batch_sz,
            'max_length_input': model.max_length_input,
            'max_length_output': model.max_length_output,
            'start_token_id': model.start_token_id,
            'end_token_id': model.end_token_id
        }
    }
    
    torch.save(checkpoint, save_path)
    print(fREMOVED_SECRETModel saved to {save_path}REMOVED_SECRET)

def main():
    # Set seed for reproducibility
    set_seed(HYPERPARAMETERS['seed'])
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() and not HYPERPARAMETERS['no_cuda'] else 'cpu')
    print(fREMOVED_SECRETUsing device: {device}REMOVED_SECRET)
    
    # Create output directory
    os.makedirs(HYPERPARAMETERS['output_dir'], exist_ok=True)
    
    # Save hyperparameters
    with open(os.path.join(HYPERPARAMETERS['output_dir'], 'hyperparameters.json'), 'w') as f:
        json.dump(HYPERPARAMETERS, f, indent=4)
    
    # Load data
    print(REMOVED_SECRETLoading data...REMOVED_SECRET)
    (train_source, train_target, val_source, val_target, test_source, test_target,
     source_vocab, target_vocab, max_length_source, max_length_target) = load_data(
        HYPERPARAMETERS['train_path'],
        HYPERPARAMETERS['val_path'],
        HYPERPARAMETERS['test_path'],
        HYPERPARAMETERS['vocab_size']
    )
    
    # Create datasets
    train_dataset = TranslationDataset(
        train_source, train_target, source_vocab, target_vocab,
        max_length_source, max_length_target
    )
    val_dataset = TranslationDataset(
        val_source, val_target, source_vocab, target_vocab,
        max_length_source, max_length_target
    )
    test_dataset = TranslationDataset(
        test_source, test_target, source_vocab, target_vocab,
        max_length_source, max_length_target
    )
    
    # Create dataloaders
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=HYPERPARAMETERS['batch_size'],
        shuffle=True,
        collate_fn=collate_fn
    )
    val_dataloader = DataLoader(
        val_dataset,
        batch_size=HYPERPARAMETERS['batch_size'],
        shuffle=False,
        collate_fn=collate_fn
    )
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=HYPERPARAMETERS['batch_size'],
        shuffle=False,
        collate_fn=collate_fn
    )
    
    # Initialize model
    print(REMOVED_SECRETInitializing model...REMOVED_SECRET)
    model = EncoderDecoder(
        input_vocab_size=len(source_vocab),
        output_vocab_size=len(target_vocab),
        embedding_dim=HYPERPARAMETERS['embedding_dim'],
        units=HYPERPARAMETERS['units'],
        batch_size=HYPERPARAMETERS['batch_size'],
        max_length_input=max_length_source,
        max_length_output=max_length_target,
        device=device,
        start_token_id=target_vocab.get('<start>', 2),
        end_token_id=target_vocab.get('<end>', 3)
    ).to(device)
    
    # Initialize optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=HYPERPARAMETERS['learning_rate'])
    criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding token
    
    # Initialize learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode='min',
        factor=HYPERPARAMETERS.get('scheduler_factor', 0.1),
        patience=HYPERPARAMETERS.get('scheduler_patience', 2),
        verbose=True
    )
    
    # Training loop
    print(REMOVED_SECRETStarting training...REMOVED_SECRET)
    best_val_loss = float('inf')
    train_losses = []
    val_losses = []
    patience_counter = 0
    
    for epoch in range(HYPERPARAMETERS['epochs']):
        start_time = time.time()
        
        # Train
        train_loss = train_epoch(
            model, train_dataloader, optimizer, criterion, device,
            clip=HYPERPARAMETERS['clip'],
            teacher_forcing_ratio=HYPERPARAMETERS['teacher_forcing_ratio']
        )
        train_losses.append(train_loss)
        
        # Validate
        val_loss = validate(model, val_dataloader, criterion, device)
        val_losses.append(val_loss)
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Print epoch results
        epoch_time = time.time() - start_time
        print(fREMOVED_SECRETEpoch {epoch+1}/{HYPERPARAMETERS['epochs']} | Time: {epoch_time:.2f}sREMOVED_SECRET)
        print(fREMOVED_SECRETTrain Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}REMOVED_SECRET)
        
        # Save model if validation loss improved
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            save_model(
                model, source_vocab, target_vocab, optimizer, epoch+1, val_loss,
                os.path.join(HYPERPARAMETERS['output_dir'], 'best_model.pt')
            )
        else:
            patience_counter += 1
        
        # Early stopping
        if patience_counter >= HYPERPARAMETERS.get('early_stopping_patience', 5):
            print(REMOVED_SECRETEarly stopping triggered!REMOVED_SECRET)
            break
        
        # Save checkpoint every N epochs
        if (epoch + 1) % HYPERPARAMETERS['save_every'] == 0:
            save_model(
                model, source_vocab, target_vocab, optimizer, epoch+1, val_loss,
                os.path.join(HYPERPARAMETERS['output_dir'], f'checkpoint_epoch_{epoch+1}.pt')
            )
    
    # Final evaluation on test set
    test_loss = validate(model, test_dataloader, criterion, device)
    print(fREMOVED_SECRETFinal test loss: {test_loss:.4f}REMOVED_SECRET)
    
    # Save final model
    save_model(
        model, source_vocab, target_vocab, optimizer, HYPERPARAMETERS['epochs'], val_loss,
        os.path.join(HYPERPARAMETERS['output_dir'], 'final_model.pt')
    )
    
    # Plot training and validation losses
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Losses')
    plt.legend()
    plt.savefig(os.path.join(HYPERPARAMETERS['output_dir'], 'loss_plot.png'))
    plt.close()
    
    print(REMOVED_SECRETTraining completed!REMOVED_SECRET)

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    main() 
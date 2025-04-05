import os
import torch
import argparse
import json
from gru_pytorch import EncoderDecoder

def load_model(model_path, device):
    """
    Load a trained model from a checkpoint file
    
    Args:
        model_path: Path to the model checkpoint
        device: Device to load the model on
        
    Returns:
        model: Loaded model
        source_vocab: Source vocabulary
        target_vocab: Target vocabulary
    """
    # Load checkpoint
    checkpoint = torch.load(model_path, map_location=device)
    
    # Extract model configuration
    config = checkpoint['model_config']
    
    # Create model
    model = EncoderDecoder(
        input_vocab_size=config['input_vocab_size'],
        output_vocab_size=config['output_vocab_size'],
        embedding_dim=config['embedding_dim'],
        units=config['units'],
        batch_size=config['batch_size'],
        max_length_input=config['max_length_input'],
        max_length_output=config['max_length_output'],
        device=device,
        start_token_id=config['start_token_id'],
        end_token_id=config['end_token_id']
    ).to(device)
    
    # Load model state
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # Extract vocabularies
    source_vocab = checkpoint['source_vocab']
    target_vocab = checkpoint['target_vocab']
    
    # Create reverse vocabularies for decoding
    source_reverse_vocab = {v: k for k, v in source_vocab.items()}
    target_reverse_vocab = {v: k for k, v in target_vocab.items()}
    
    return model, source_vocab, target_vocab, source_reverse_vocab, target_reverse_vocab

def tokenize(text, vocab, max_length=None):
    """
    Tokenize text into token IDs
    
    Args:
        text: Text to tokenize
        vocab: Vocabulary dictionary
        max_length: Maximum sequence length
        
    Returns:
        token_ids: List of token IDs
    """
    # Split text into tokens
    tokens = text.split()
    
    # Convert tokens to IDs
    token_ids = [vocab.get(token, vocab.get('<unk>', 1)) for token in tokens]
    
    # Truncate if necessary
    if max_length is not None and len(token_ids) > max_length:
        token_ids = token_ids[:max_length]
    
    return token_ids

def detokenize(token_ids, reverse_vocab):
    """
    Convert token IDs back to text
    
    Args:
        token_ids: List of token IDs
        reverse_vocab: Reverse vocabulary dictionary
        
    Returns:
        text: Decoded text
    """
    # Convert IDs to tokens
    tokens = [reverse_vocab.get(id, '<unk>') for id in token_ids]
    
    # Join tokens into text
    text = ' '.join(tokens)
    
    return text

def translate(model, text, source_vocab, target_reverse_vocab, device, max_length=None):
    """
    Translate text using the model
    
    Args:
        model: Trained model
        text: Text to translate
        source_vocab: Source vocabulary
        target_reverse_vocab: Target reverse vocabulary
        device: Device to run inference on
        max_length: Maximum output length
        
    Returns:
        translation: Translated text
        attention_weights: Attention weights for visualization
    """
    # Tokenize input text
    token_ids = tokenize(text, source_vocab, max_length)
    
    # Convert to tensor
    input_tensor = torch.tensor([token_ids], dtype=torch.long).to(device)
    
    # Generate translation
    with torch.no_grad():
        predicted_ids, attention_weights = model.predict(input_tensor, max_length=max_length)
    
    # Convert to list
    predicted_ids = predicted_ids[0].cpu().numpy().tolist()
    
    # Remove end token and everything after it
    if model.end_token_id in predicted_ids:
        end_idx = predicted_ids.index(model.end_token_id)
        predicted_ids = predicted_ids[:end_idx]
    
    # Detokenize
    translation = detokenize(predicted_ids, target_reverse_vocab)
    
    return translation, attention_weights[0].cpu().numpy()

def main(args):
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() and not args.no_cuda else 'cpu')
    print(f"Using device: {device}")
    
    # Load model and vocabularies
    print(f"Loading model from {args.model_path}...")
    model, source_vocab, target_vocab, source_reverse_vocab, target_reverse_vocab = load_model(args.model_path, device)
    
    # Interactive translation
    if args.interactive:
        print("Enter text to translate (or 'quit' to exit):")
        while True:
            text = input("> ")
            if text.lower() == 'quit':
                break
            
            # Translate
            translation, _ = translate(model, text, source_vocab, target_reverse_vocab, device)
            print(f"Translation: {translation}")
            print()
    
    # Translate from file
    elif args.input_file:
        print(f"Translating from file {args.input_file}...")
        with open(args.input_file, 'r', encoding='utf-8') as f:
            input_texts = [line.strip() for line in f.readlines()]
        
        translations = []
        for text in input_texts:
            translation, _ = translate(model, text, source_vocab, target_reverse_vocab, device)
            translations.append(translation)
        
        # Save translations
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                for translation in translations:
                    f.write(f"{translation}\n")
            print(f"Translations saved to {args.output_file}")
        else:
            for i, (text, translation) in enumerate(zip(input_texts, translations)):
                print(f"Input {i+1}: {text}")
                print(f"Translation {i+1}: {translation}")
                print()
    
    # Single text translation
    else:
        print(f"Translating: {args.text}")
        translation, _ = translate(model, args.text, source_vocab, target_reverse_vocab, device)
        print(f"Translation: {translation}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate text using a trained GRU-based encoder-decoder model')
    
    # Model arguments
    parser.add_argument('--model_path', type=str, required=True, help='Path to the trained model checkpoint')
    
    # Input arguments (one of these must be provided)
    parser.add_argument('--text', type=str, help='Text to translate')
    parser.add_argument('--input_file', type=str, help='Path to file containing texts to translate')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    # Output arguments
    parser.add_argument('--output_file', type=str, help='Path to save translations (only used with --input_file)')
    parser.add_argument('--no_cuda', action='store_true', help='Disable CUDA')
    
    args = parser.parse_args()
    
    # Check that at least one input method is specified
    if not args.text and not args.input_file and not args.interactive:
        parser.error("At least one of --text, --input_file, or --interactive must be specified")
    
    main(args) 
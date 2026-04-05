"""
Deep Learning Pipeline Training Script
- Uses train.csv
- Applies SAME preprocessing from text_cleaner.py
- Trains LSTM model for classification using PyTorch
- Saves model and tokenizer
"""

import pandas as pd
import numpy as np
import pickle
import sys
import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seeds for reproducibility
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

# Configuration
MAX_LENGTH = 100
EMBEDDING_DIM = 128
LSTM_UNITS = 64
DROPOUT_RATE = 0.2
DENSE_UNITS = 32
EPOCHS = 10
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
LEARNING_RATE = 0.001

class SimpleTokenizer:
    """Simple tokenizer compatible with Keras-style API"""
    def __init__(self, oov_token="<UNK>"):
        self.oov_token = oov_token
        self.word_index = {}
        self.index_word = {}
        
    def fit_on_texts(self, texts):
        """Build vocabulary from texts"""
        word_counts = {}
        for text in texts:
            for word in text.split():
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Build word_index (1-indexed, 0 reserved for padding)
        self.word_index = {self.oov_token: 1}
        for idx, (word, _) in enumerate(sorted_words, start=2):
            self.word_index[word] = idx
        
        # Build reverse index
        self.index_word = {v: k for k, v in self.word_index.items()}
        
    def texts_to_sequences(self, texts):
        """Convert texts to sequences of integers"""
        sequences = []
        oov_idx = self.word_index[self.oov_token]
        
        for text in texts:
            sequence = [self.word_index.get(word, oov_idx) for word in text.split()]
            sequences.append(sequence)
        
        return sequences

def pad_sequences(sequences, maxlen, padding='post'):
    """Pad sequences to same length"""
    padded = np.zeros((len(sequences), maxlen), dtype=np.int64)
    
    for i, seq in enumerate(sequences):
        if len(seq) > maxlen:
            if padding == 'post':
                padded[i] = seq[:maxlen]
            else:
                padded[i] = seq[-maxlen:]
        else:
            if padding == 'post':
                padded[i, :len(seq)] = seq
            else:
                padded[i, -len(seq):] = seq
    
    return padded

class TicketDataset(Dataset):
    """PyTorch Dataset for tickets"""
    def __init__(self, sequences, labels):
        self.sequences = torch.LongTensor(sequences)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx]

class LSTMClassifier(nn.Module):
    """LSTM model for classification"""
    def __init__(self, vocab_size, embedding_dim, lstm_units, dropout_rate, dense_units, num_classes):
        super(LSTMClassifier, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, lstm_units, batch_first=True)
        self.dropout = nn.Dropout(dropout_rate)
        self.dense = nn.Linear(lstm_units, dense_units)
        self.relu = nn.ReLU()
        self.output = nn.Linear(dense_units, num_classes)
        
    def forward(self, x):
        # Embedding
        embedded = self.embedding(x)
        
        # LSTM
        lstm_out, (hidden, cell) = self.lstm(embedded)
        
        # Use last hidden state
        last_hidden = hidden[-1]
        
        # Dropout
        dropped = self.dropout(last_hidden)
        
        # Dense
        dense_out = self.relu(self.dense(dropped))
        
        # Output
        output = self.output(dense_out)
        
        return output

def load_and_preprocess_data():
    """Load train.csv and apply preprocessing"""
    print("=" * 80)
    print("DEEP LEARNING PIPELINE - TRAINING")
    print("=" * 80)
    
    print("\n[1/7] Loading training data...")
    try:
        train_df = pd.read_csv('data/train.csv')
        print(f"✓ Loaded {len(train_df)} training samples")
    except FileNotFoundError:
        print("❌ train.csv not found. Please run data/prepare_dataset.py first.")
        return None, None, None
    
    print("\n[2/7] Preprocessing text (using text_cleaner.py)...")
    processed_texts = []
    failed_count = 0
    
    for text in train_df['text']:
        try:
            processed, _ = preprocess_pipeline(text, return_string=True)
            processed_texts.append(processed)
        except PreprocessingError:
            processed_texts.append("")
            failed_count += 1
    
    train_df['processed_text'] = processed_texts
    train_df = train_df[train_df['processed_text'] != ""].reset_index(drop=True)
    
    print(f"✓ Preprocessed {len(train_df)} samples")
    if failed_count > 0:
        print(f"⚠ Skipped {failed_count} samples due to preprocessing errors")
    
    X_train = train_df['processed_text'].values
    y_train = train_df['category'].values
    
    return train_df, X_train, y_train

def create_tokenizer(X_train):
    """Create and fit tokenizer on training data only"""
    print("\n[3/7] Creating tokenizer...")
    
    tokenizer = SimpleTokenizer(oov_token="<UNK>")
    tokenizer.fit_on_texts(X_train)
    
    vocab_size = len(tokenizer.word_index) + 1  # +1 for padding token
    
    print(f"✓ Tokenizer created")
    print(f"  Vocabulary size: {vocab_size}")
    print(f"  OOV token: <UNK>")
    
    # Convert texts to sequences
    X_sequences = tokenizer.texts_to_sequences(X_train)
    
    # Pad sequences
    X_padded = pad_sequences(X_sequences, maxlen=MAX_LENGTH, padding='post')
    
    print(f"  Sequence shape: {X_padded.shape}")
    print(f"  Max length: {MAX_LENGTH}")
    print(f"  Padding: post")
    
    return tokenizer, X_padded, vocab_size

def encode_labels(y_train):
    """Encode labels"""
    print("\n[4/7] Encoding labels...")
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_train)
    
    print(f"✓ Labels encoded")
    print(f"  Classes: {list(label_encoder.classes_)}")
    print(f"  Encoded shape: {y_encoded.shape}")
    
    return label_encoder, y_encoded

def build_model(vocab_size, num_classes):
    """Build LSTM model with specified architecture"""
    print("\n[5/7] Building LSTM model...")
    
    model = LSTMClassifier(
        vocab_size=vocab_size,
        embedding_dim=EMBEDDING_DIM,
        lstm_units=LSTM_UNITS,
        dropout_rate=DROPOUT_RATE,
        dense_units=DENSE_UNITS,
        num_classes=num_classes
    )
    
    print("\n" + "=" * 80)
    print("MODEL ARCHITECTURE")
    print("=" * 80)
    print(model)
    print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters())}")
    print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}")
    
    return model

def train_model(model, X_padded, y_encoded):
    """Train the model"""
    print("\n[6/7] Training model...")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Validation split: {VALIDATION_SPLIT}")
    
    # Split into train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_padded, y_encoded,
        test_size=VALIDATION_SPLIT,
        random_state=SEED,
        stratify=y_encoded
    )
    
    # Create datasets
    train_dataset = TicketDataset(X_train, y_train)
    val_dataset = TicketDataset(X_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    # Training loop
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(EPOCHS):
        # Training
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for sequences, labels in train_loader:
            sequences, labels = sequences.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(sequences)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        train_loss /= len(train_loader)
        train_acc = train_correct / train_total
        
        # Validation
        model.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for sequences, labels in val_loader:
                sequences, labels = sequences.to(device), labels.to(device)
                
                outputs = model(sequences)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_loss /= len(val_loader)
        val_acc = val_correct / val_total
        
        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        print(f"Epoch {epoch+1}/{EPOCHS} - "
              f"loss: {train_loss:.4f} - acc: {train_acc:.4f} - "
              f"val_loss: {val_loss:.4f} - val_acc: {val_acc:.4f}")
    
    print("\n✓ Training complete")
    
    return history, device

def save_models(model, tokenizer, label_encoder, device):
    """Save trained model and tokenizer"""
    print("\n[7/7] Saving models...")
    
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model.to('cpu')  # Move to CPU before saving
    torch.save(model.state_dict(), 'models/dl_model.pth')
    print("✓ Saved dl_model.pth")
    
    # Save tokenizer
    with open('models/tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    print("✓ Saved tokenizer.pkl")
    
    # Save label encoder
    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    print("✓ Saved label_encoder.pkl")
    
    # Save model architecture info
    model_info = {
        'vocab_size': model.embedding.num_embeddings,
        'embedding_dim': EMBEDDING_DIM,
        'lstm_units': LSTM_UNITS,
        'dropout_rate': DROPOUT_RATE,
        'dense_units': DENSE_UNITS,
        'num_classes': model.output.out_features
    }
    with open('models/dl_model_info.pkl', 'wb') as f:
        pickle.dump(model_info, f)
    print("✓ Saved dl_model_info.pkl")

def plot_training_history(history):
    """Plot training and validation accuracy/loss"""
    print("\n" + "=" * 80)
    print("TRAINING CURVES")
    print("=" * 80)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history['train_acc']) + 1)
    
    # Plot accuracy
    ax1.plot(epochs, history['train_acc'], label='Training Accuracy', linewidth=2)
    ax1.plot(epochs, history['val_acc'], label='Validation Accuracy', linewidth=2)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Plot loss
    ax2.plot(epochs, history['train_loss'], label='Training Loss', linewidth=2)
    ax2.plot(epochs, history['val_loss'], label='Validation Loss', linewidth=2)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    os.makedirs('results/graphs', exist_ok=True)
    plt.savefig('results/graphs/dl_training_curves.png', dpi=300, bbox_inches='tight')
    print("\n✓ Training curves saved to results/graphs/dl_training_curves.png")
    plt.close()
    
    # Print final metrics
    final_train_acc = history['train_acc'][-1]
    final_val_acc = history['val_acc'][-1]
    final_train_loss = history['train_loss'][-1]
    final_val_loss = history['val_loss'][-1]
    
    print(f"\n📊 Final Metrics:")
    print(f"  Training Accuracy:   {final_train_acc * 100:.2f}%")
    print(f"  Validation Accuracy: {final_val_acc * 100:.2f}%")
    print(f"  Training Loss:       {final_train_loss:.4f}")
    print(f"  Validation Loss:     {final_val_loss:.4f}")

def demonstrate_predictions(train_df, model, tokenizer, label_encoder, device):
    """Show sample predictions"""
    print("\n" + "=" * 80)
    print("SAMPLE PREDICTIONS")
    print("=" * 80)
    
    # Select 5 random samples
    samples = train_df.sample(n=5, random_state=SEED)
    
    model.eval()
    model.to(device)
    
    for idx, (i, row) in enumerate(samples.iterrows(), 1):
        print(f"\nSample {idx}:")
        print(f"  Raw text: {row['text'][:80]}...")
        print(f"  Processed: {row['processed_text'][:80]}...")
        print(f"  True category: {row['category']}")
        
        # Predict
        sequence = tokenizer.texts_to_sequences([row['processed_text']])
        padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
        
        with torch.no_grad():
            inputs = torch.LongTensor(padded).to(device)
            outputs = model(inputs)
            probabilities = torch.softmax(outputs, dim=1).cpu().numpy()[0]
        
        predicted_idx = np.argmax(probabilities)
        predicted_category = label_encoder.inverse_transform([predicted_idx])[0]
        confidence = probabilities[predicted_idx]
        
        print(f"  Predicted category: {predicted_category}")
        print(f"  Confidence: {confidence * 100:.2f}%")
        
        # Show all probabilities
        print(f"  All probabilities:")
        for class_idx, prob in enumerate(probabilities):
            class_name = label_encoder.inverse_transform([class_idx])[0]
            print(f"    {class_name}: {prob * 100:.2f}%")

def main():
    """Main training pipeline"""
    # Load and preprocess
    train_df, X_train, y_train = load_and_preprocess_data()
    if train_df is None:
        return
    
    # Create tokenizer
    tokenizer, X_padded, vocab_size = create_tokenizer(X_train)
    
    # Encode labels
    label_encoder, y_encoded = encode_labels(y_train)
    
    # Build model
    num_classes = len(label_encoder.classes_)
    model = build_model(vocab_size, num_classes)
    
    # Train model
    history, device = train_model(model, X_padded, y_encoded)
    
    # Save models
    save_models(model, tokenizer, label_encoder, device)
    
    # Plot training history
    plot_training_history(history)
    
    # Demonstrate predictions
    demonstrate_predictions(train_df, model, tokenizer, label_encoder, device)
    
    print("\n" + "=" * 80)
    print("✅ DEEP LEARNING PIPELINE TRAINING COMPLETE")
    print("=" * 80)
    print("\nSaved models:")
    print("  - models/dl_model.pth")
    print("  - models/tokenizer.pkl")
    print("  - models/label_encoder.pkl")
    print("  - models/dl_model_info.pkl")
    print("\n⚠️ Note: Duplicate detection not implemented yet (as per requirements)")

if __name__ == "__main__":
    main()

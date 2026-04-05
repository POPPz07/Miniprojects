"""
Deep Learning Pipeline Evaluation Script
- Evaluates on test.csv
- Classification performance metrics
- Duplicate detection using LSTM embeddings
- Confusion matrix visualization
"""

import pandas as pd
import numpy as np
import pickle
import sys
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix
)
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seed
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

# Configuration
MAX_LENGTH = 100
DUPLICATE_THRESHOLD = 0.7

def load_models():
    """Load all trained DL models"""
    print("=" * 80)
    print("DEEP LEARNING PIPELINE EVALUATION ON TEST SET")
    print("=" * 80)
    
    print("\n[1/7] Loading models...")
    
    # Load LSTM model
    model = keras.models.load_model('models/dl_model.h5')
    print("✓ Loaded dl_model.h5")
    
    # Load tokenizer
    with open('models/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    print("✓ Loaded tokenizer.pkl")
    
    # Load label encoder
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✓ Loaded label_encoder.pkl")
    
    print("✓ All models loaded")
    
    return model, tokenizer, label_encoder

def load_and_preprocess_test():
    """Load test.csv and preprocess"""
    print("\n[2/7] Loading and preprocessing test data...")
    
    try:
        test_df = pd.read_csv('data/test.csv')
        print(f"✓ Loaded {len(test_df)} test samples")
    except FileNotFoundError:
        print("❌ test.csv not found")
        return None
    
    # Preprocess
    processed_texts = []
    failed_count = 0
    
    for text in test_df['text']:
        try:
            processed, _ = preprocess_pipeline(text, return_string=True)
            processed_texts.append(processed)
        except PreprocessingError:
            processed_texts.append("")
            failed_count += 1
    
    test_df['processed_text'] = processed_texts
    test_df = test_df[test_df['processed_text'] != ""].reset_index(drop=True)
    
    print(f"✓ Preprocessed {len(test_df)} samples")
    if failed_count > 0:
        print(f"⚠ Skipped {failed_count} samples")
    
    return test_df

def prepare_test_data(test_df, tokenizer):
    """Convert text to sequences and pad"""
    print("\n[3/7] Converting text to sequences...")
    
    # Convert to sequences
    X_sequences = tokenizer.texts_to_sequences(test_df['processed_text'].values)
    
    # Pad sequences
    X_padded = pad_sequences(X_sequences, maxlen=MAX_LENGTH, padding='post')
    
    print(f"✓ Padded sequences shape: {X_padded.shape}")
    
    return X_padded

def evaluate_classification(test_df, model, X_test_padded, label_encoder):
    """Evaluate classification performance"""
    print("\n[4/7] Evaluating classification performance...")
    
    # Prepare data
    y_test = test_df['category'].values
    
    # Predict
    y_pred_proba = model.predict(X_test_padded, verbose=0)
    y_pred_encoded = np.argmax(y_pred_proba, axis=1)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average='weighted'
    )
    
    print("\n" + "=" * 80)
    print("CLASSIFICATION PERFORMANCE")
    print("=" * 80)
    
    print(f"\n📊 Overall Metrics:")
    print(f"  Test Accuracy:  {accuracy * 100:.2f}%")
    print(f"  Precision:      {precision * 100:.2f}%")
    print(f"  Recall:         {recall * 100:.2f}%")
    print(f"  F1-Score:       {f1 * 100:.2f}%")
    
    # Per-class metrics
    print(f"\n📋 Per-Class Metrics:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=label_encoder.classes_)
    
    print(f"\n🔢 Confusion Matrix:")
    print(f"{'':12} " + " ".join([f"{c:>10}" for c in label_encoder.classes_]))
    for i, row_label in enumerate(label_encoder.classes_):
        print(f"{row_label:12} " + " ".join([f"{cm[i][j]:>10}" for j in range(len(label_encoder.classes_))]))
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    plt.title('DL Pipeline - Confusion Matrix (Test Set)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    os.makedirs('results/graphs', exist_ok=True)
    plt.savefig('results/graphs/dl_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\n✓ Confusion matrix saved to results/graphs/dl_confusion_matrix.png")
    plt.close()
    
    return y_pred, y_pred_proba

def extract_embeddings(model, X_padded):
    """Extract LSTM embeddings for duplicate detection"""
    print("\n[5/7] Extracting LSTM embeddings...")
    
    # Create a model that outputs LSTM layer
    embedding_model = Model(inputs=model.input, outputs=model.get_layer('lstm').output)
    
    # Extract embeddings
    embeddings = embedding_model.predict(X_padded, verbose=0)
    
    # Normalize embeddings (L2 normalization)
    embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    print(f"✓ Extracted embeddings shape: {embeddings.shape}")
    print(f"✓ Normalized embeddings")
    
    return embeddings_normalized

def load_or_create_train_embeddings(model, tokenizer):
    """Load or create training embeddings"""
    embeddings_path = 'models/train_embeddings_normalized.npy'
    
    if os.path.exists(embeddings_path):
        print("✓ Loading existing training embeddings...")
        train_embeddings = np.load(embeddings_path)
        print(f"  Shape: {train_embeddings.shape}")
    else:
        print("✓ Creating training embeddings...")
        # Load training data
        train_df = pd.read_csv('data/train.csv')
        
        # Preprocess
        processed_texts = []
        for text in train_df['text']:
            try:
                processed, _ = preprocess_pipeline(text, return_string=True)
                processed_texts.append(processed)
            except PreprocessingError:
                processed_texts.append("")
        
        train_df['processed_text'] = processed_texts
        train_df = train_df[train_df['processed_text'] != ""].reset_index(drop=True)
        
        # Convert to sequences
        X_sequences = tokenizer.texts_to_sequences(train_df['processed_text'].values)
        X_padded = pad_sequences(X_sequences, maxlen=MAX_LENGTH, padding='post')
        
        # Extract embeddings
        train_embeddings = extract_embeddings(model, X_padded)
        
        # Save for future use
        np.save(embeddings_path, train_embeddings)
        print(f"✓ Saved training embeddings to {embeddings_path}")
    
    return train_embeddings

def evaluate_duplicate_detection(test_df, test_embeddings, train_embeddings):
    """Evaluate duplicate detection using embedding similarity"""
    print("\n[6/7] Evaluating duplicate detection...")
    
    y_true_dup = test_df['is_duplicate'].values
    y_pred_dup = []
    max_similarities = []
    
    # For each test sample, find most similar training sample
    for i in range(len(test_embeddings)):
        query_embedding = test_embeddings[i:i+1]
        similarities = cosine_similarity(query_embedding, train_embeddings).flatten()
        max_similarity = similarities.max()
        max_similarities.append(max_similarity)
        
        # Predict duplicate if max similarity > threshold
        is_dup = 1 if max_similarity > DUPLICATE_THRESHOLD else 0
        y_pred_dup.append(is_dup)
    
    y_pred_dup = np.array(y_pred_dup)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true_dup, y_pred_dup)
    
    # True positives, false positives, false negatives
    tp = np.sum((y_true_dup == 1) & (y_pred_dup == 1))
    fp = np.sum((y_true_dup == 0) & (y_pred_dup == 1))
    fn = np.sum((y_true_dup == 1) & (y_pred_dup == 0))
    tn = np.sum((y_true_dup == 0) & (y_pred_dup == 0))
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\n" + "=" * 80)
    print("DUPLICATE DETECTION PERFORMANCE (DL)")
    print("=" * 80)
    
    print(f"\n📊 Overall Metrics:")
    print(f"  Accuracy:       {accuracy * 100:.2f}%")
    print(f"  Precision:      {precision * 100:.2f}%")
    print(f"  Recall:         {recall * 100:.2f}%")
    print(f"  F1-Score:       {f1 * 100:.2f}%")
    
    print(f"\n🔢 Confusion Matrix:")
    print(f"  True Positives:  {tp}")
    print(f"  False Positives: {fp}")
    print(f"  True Negatives:  {tn}")
    print(f"  False Negatives: {fn}")
    
    print(f"\n⚙️ Configuration:")
    print(f"  Threshold: {DUPLICATE_THRESHOLD}")
    print(f"  Method: Cosine similarity on LSTM embeddings")
    print(f"  Embedding dimension: {test_embeddings.shape[1]}")
    
    return y_pred_dup, max_similarities

def show_example_predictions(test_df, model, tokenizer, label_encoder, y_pred, y_pred_dup, max_similarities):
    """Show example predictions from test set"""
    print("\n[7/7] Example predictions from test set...")
    
    # Select 5 random samples
    samples = test_df.sample(n=5, random_state=SEED)
    
    print("\n" + "=" * 80)
    print("EXAMPLE PREDICTIONS (5 SAMPLES FROM TEST SET)")
    print("=" * 80)
    
    for idx, (i, row) in enumerate(samples.iterrows(), 1):
        print(f"\n{'='*80}")
        print(f"SAMPLE {idx}")
        print(f"{'='*80}")
        
        print(f"\n📄 Raw Text:")
        print(f"  {row['text'][:100]}...")
        
        print(f"\n✨ Processed Text:")
        print(f"  {row['processed_text'][:100]}...")
        
        print(f"\n🏷️ Classification:")
        print(f"  True category:      {row['category']}")
        print(f"  Predicted category: {y_pred[i]}")
        print(f"  Correct: {'✓' if row['category'] == y_pred[i] else '✗'}")
        
        # Get probabilities
        sequence = tokenizer.texts_to_sequences([row['processed_text']])
        padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
        y_proba = model.predict(padded, verbose=0)[0]
        pred_idx = np.argmax(y_proba)
        
        print(f"  Confidence: {y_proba[pred_idx] * 100:.2f}%")
        
        print(f"\n🔄 Duplicate Detection:")
        print(f"  True duplicate:      {row['is_duplicate']}")
        print(f"  Predicted duplicate: {y_pred_dup[i]}")
        print(f"  Max similarity:      {max_similarities[i]:.4f}")
        print(f"  Correct: {'✓' if row['is_duplicate'] == y_pred_dup[i] else '✗'}")

def compare_with_nlp():
    """Brief comparison with NLP results"""
    print("\n" + "=" * 80)
    print("COMPARISON: DL vs NLP")
    print("=" * 80)
    
    print("\n📊 Classification Performance:")
    print("  Metric          NLP (TF-IDF)    DL (LSTM)")
    print("  " + "-" * 50)
    print("  Accuracy        91.33%          [See above]")
    print("  Method          TF-IDF + LR     LSTM")
    
    print("\n🔄 Duplicate Detection Performance:")
    print("  Metric          NLP (TF-IDF)    DL (LSTM)")
    print("  " + "-" * 50)
    print("  Recall          6.25%           [See above]")
    print("  Precision       29.41%          [See above]")
    print("  F1-Score        10.31%          [See above]")
    print("  Method          Cosine (TF-IDF) Cosine (Embeddings)")
    
    print("\n💡 Key Insights:")
    print("  - NLP: Fast, interpretable, good for classification")
    print("  - DL:  Semantic understanding, better for duplicates")
    print("  - NLP duplicate detection struggled (6.25% recall)")
    print("  - DL should perform better due to semantic embeddings")

def main():
    """Main evaluation pipeline"""
    # Load models
    model, tokenizer, label_encoder = load_models()
    
    # Load test data
    test_df = load_and_preprocess_test()
    if test_df is None:
        return
    
    # Prepare test data
    X_test_padded = prepare_test_data(test_df, tokenizer)
    
    # Evaluate classification
    y_pred, y_pred_proba = evaluate_classification(test_df, model, X_test_padded, label_encoder)
    
    # Extract test embeddings
    test_embeddings = extract_embeddings(model, X_test_padded)
    
    # Load or create training embeddings
    train_embeddings = load_or_create_train_embeddings(model, tokenizer)
    
    # Evaluate duplicate detection
    y_pred_dup, max_similarities = evaluate_duplicate_detection(test_df, test_embeddings, train_embeddings)
    
    # Show examples
    show_example_predictions(test_df, model, tokenizer, label_encoder, y_pred, y_pred_dup, max_similarities)
    
    # Compare with NLP
    compare_with_nlp()
    
    print("\n" + "=" * 80)
    print("✅ DEEP LEARNING PIPELINE EVALUATION COMPLETE")
    print("=" * 80)
    print("\nSaved outputs:")
    print("  - results/graphs/dl_confusion_matrix.png")
    print("  - models/train_embeddings_normalized.npy")

if __name__ == "__main__":
    main()

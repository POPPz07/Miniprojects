"""
NLP Pipeline Training Script
- Loads train.csv
- Applies preprocessing from text_cleaner.py
- Trains TF-IDF vectorizer
- Trains Logistic Regression classifier
- Saves models and precomputed vectors
"""

import pandas as pd
import numpy as np
import pickle
import sys
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Add parent directory to path
sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seed for reproducibility
SEED = 42
np.random.seed(SEED)

# Configuration
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 2

def load_and_preprocess_data():
    """Load train.csv and apply preprocessing"""
    print("=" * 60)
    print("NLP PIPELINE - TRAINING")
    print("=" * 60)
    
    print("\n[1/6] Loading training data...")
    try:
        train_df = pd.read_csv('data/train.csv')
        print(f"✓ Loaded {len(train_df)} training samples")
    except FileNotFoundError:
        print("❌ train.csv not found. Please run data/prepare_dataset.py first.")
        return None, None, None
    
    print("\n[2/6] Preprocessing text...")
    processed_texts = []
    failed_count = 0
    
    for idx, text in enumerate(train_df['text']):
        try:
            processed, _ = preprocess_pipeline(text, return_string=True)
            processed_texts.append(processed)
        except PreprocessingError:
            # Use empty string for failed preprocessing
            processed_texts.append("")
            failed_count += 1
    
    train_df['processed_text'] = processed_texts
    
    # Remove rows with empty processed text
    train_df = train_df[train_df['processed_text'] != ""].reset_index(drop=True)
    
    print(f"✓ Preprocessed {len(train_df)} samples")
    if failed_count > 0:
        print(f"⚠ Skipped {failed_count} samples due to preprocessing errors")
    
    # Prepare features and labels
    X_train = train_df['processed_text'].values
    y_train = train_df['category'].values
    
    return train_df, X_train, y_train

def train_tfidf_vectorizer(X_train):
    """Train TF-IDF vectorizer"""
    print("\n[3/6] Training TF-IDF vectorizer...")
    
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        min_df=TFIDF_MIN_DF,
        sublinear_tf=True
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    print(f"✓ TF-IDF vectorizer trained")
    print(f"  Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"  Feature matrix shape: {X_train_tfidf.shape}")
    print(f"  Matrix sparsity: {(1 - X_train_tfidf.nnz / (X_train_tfidf.shape[0] * X_train_tfidf.shape[1])) * 100:.2f}%")
    
    return vectorizer, X_train_tfidf

def train_classifier(X_train_tfidf, y_train):
    """Train Logistic Regression classifier"""
    print("\n[4/6] Training Logistic Regression classifier...")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    
    # Train classifier
    classifier = LogisticRegression(
        max_iter=1000,
        random_state=SEED,
        C=1.0,
        solver='lbfgs'
    )
    
    classifier.fit(X_train_tfidf, y_train_encoded)
    
    # Training accuracy
    y_train_pred = classifier.predict(X_train_tfidf)
    train_accuracy = accuracy_score(y_train_encoded, y_train_pred)
    
    print(f"✓ Classifier trained")
    print(f"  Training accuracy: {train_accuracy * 100:.2f}%")
    print(f"  Classes: {list(label_encoder.classes_)}")
    
    return classifier, label_encoder

def save_models(vectorizer, classifier, label_encoder, X_train_tfidf):
    """Save trained models and precomputed vectors"""
    print("\n[5/6] Saving models...")
    
    import os
    os.makedirs('models', exist_ok=True)
    
    # Save TF-IDF vectorizer
    with open('models/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    print("✓ Saved tfidf_vectorizer.pkl")
    
    # Save classifier
    with open('models/nlp_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    print("✓ Saved nlp_classifier.pkl")
    
    # Save label encoder
    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    print("✓ Saved label_encoder.pkl")
    
    # Save precomputed TF-IDF vectors (for duplicate detection)
    save_npz('models/train_tfidf_vectors.npz', X_train_tfidf)
    print("✓ Saved train_tfidf_vectors.npz")

def demonstrate_predictions(train_df, vectorizer, classifier, label_encoder):
    """Show sample predictions"""
    print("\n[6/6] Sample predictions...")
    
    # Select 5 random samples
    samples = train_df.sample(n=5, random_state=SEED)
    
    print("\n" + "=" * 80)
    print("SAMPLE PREDICTIONS")
    print("=" * 80)
    
    for idx, (i, row) in enumerate(samples.iterrows(), 1):
        print(f"\nSample {idx}:")
        print(f"  Raw text: {row['text'][:80]}...")
        print(f"  Processed: {row['processed_text'][:80]}...")
        print(f"  True category: {row['category']}")
        
        # Predict
        X_sample = vectorizer.transform([row['processed_text']])
        y_pred_encoded = classifier.predict(X_sample)[0]
        y_pred_proba = classifier.predict_proba(X_sample)[0]
        y_pred = label_encoder.inverse_transform([y_pred_encoded])[0]
        
        print(f"  Predicted category: {y_pred}")
        print(f"  Confidence: {y_pred_proba[y_pred_encoded] * 100:.2f}%")
        
        # Show all probabilities
        print(f"  All probabilities:")
        for class_idx, prob in enumerate(y_pred_proba):
            class_name = label_encoder.inverse_transform([class_idx])[0]
            print(f"    {class_name}: {prob * 100:.2f}%")

def demonstrate_similarity(train_df, vectorizer, X_train_tfidf):
    """Demonstrate duplicate detection using cosine similarity"""
    print("\n" + "=" * 80)
    print("DUPLICATE DETECTION - SIMILARITY EXAMPLE")
    print("=" * 80)
    
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Select a sample with duplicate
    duplicate_samples = train_df[train_df['is_duplicate'] == 1]
    if len(duplicate_samples) == 0:
        print("⚠ No duplicate samples found in training data")
        return
    
    sample = duplicate_samples.sample(n=1, random_state=SEED).iloc[0]
    sample_idx = duplicate_samples.sample(n=1, random_state=SEED).index[0]
    
    print(f"\nQuery ticket:")
    print(f"  Text: {sample['text'][:100]}...")
    print(f"  Category: {sample['category']}")
    print(f"  Is duplicate: {sample['is_duplicate']}")
    
    # Get TF-IDF vector for this sample
    query_vector = X_train_tfidf[sample_idx]
    
    # Compute cosine similarity with all training samples
    similarities = cosine_similarity(query_vector, X_train_tfidf).flatten()
    
    # Get top 3 most similar (excluding itself)
    top_indices = np.argsort(similarities)[::-1][1:4]  # Skip first (itself)
    
    print(f"\n🔍 Top 3 most similar tickets:")
    for rank, idx in enumerate(top_indices, 1):
        similar_ticket = train_df.iloc[idx]
        similarity_score = similarities[idx]
        
        print(f"\n  Rank {rank} (Similarity: {similarity_score:.4f}):")
        print(f"    Text: {similar_ticket['text'][:100]}...")
        print(f"    Category: {similar_ticket['category']}")
        print(f"    Is duplicate: {similar_ticket['is_duplicate']}")
    
    # Duplicate threshold
    threshold = 0.8
    is_duplicate = similarities[top_indices[0]] > threshold
    print(f"\n  Duplicate threshold: {threshold}")
    print(f"  Is duplicate? {'YES' if is_duplicate else 'NO'}")

def main():
    """Main training pipeline"""
    # Load and preprocess
    train_df, X_train, y_train = load_and_preprocess_data()
    if train_df is None:
        return
    
    # Train TF-IDF
    vectorizer, X_train_tfidf = train_tfidf_vectorizer(X_train)
    
    # Train classifier
    classifier, label_encoder = train_classifier(X_train_tfidf, y_train)
    
    # Save models
    save_models(vectorizer, classifier, label_encoder, X_train_tfidf)
    
    # Demonstrate predictions
    demonstrate_predictions(train_df, vectorizer, classifier, label_encoder)
    
    # Demonstrate similarity
    demonstrate_similarity(train_df, vectorizer, X_train_tfidf)
    
    print("\n" + "=" * 60)
    print("✅ NLP PIPELINE TRAINING COMPLETE")
    print("=" * 60)
    print("\nSaved models:")
    print("  - models/tfidf_vectorizer.pkl")
    print("  - models/nlp_classifier.pkl")
    print("  - models/label_encoder.pkl")
    print("  - models/train_tfidf_vectors.npz")

if __name__ == "__main__":
    main()

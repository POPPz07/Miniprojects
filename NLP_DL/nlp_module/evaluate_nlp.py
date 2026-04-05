"""
NLP Pipeline Evaluation Script
- Evaluates on test.csv
- Classification performance metrics
- Duplicate detection performance
- Confusion matrix visualization
"""

import pandas as pd
import numpy as np
import pickle
import sys
from scipy.sparse import load_npz
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

# Duplicate detection threshold
DUPLICATE_THRESHOLD = 0.8

def load_models():
    """Load all trained models"""
    print("=" * 80)
    print("NLP PIPELINE EVALUATION ON TEST SET")
    print("=" * 80)
    
    print("\n[1/5] Loading models...")
    
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open('models/nlp_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    
    print("✓ All models loaded")
    
    return vectorizer, classifier, label_encoder, train_vectors

def load_and_preprocess_test():
    """Load test.csv and preprocess"""
    print("\n[2/5] Loading and preprocessing test data...")
    
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

def evaluate_classification(test_df, vectorizer, classifier, label_encoder):
    """Evaluate classification performance"""
    print("\n[3/5] Evaluating classification performance...")
    
    # Prepare data
    X_test = test_df['processed_text'].values
    y_test = test_df['category'].values
    
    # Transform and predict
    X_test_tfidf = vectorizer.transform(X_test)
    y_test_encoded = label_encoder.transform(y_test)
    y_pred_encoded = classifier.predict(X_test_tfidf)
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
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    plt.title('NLP Pipeline - Confusion Matrix (Test Set)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    import os
    os.makedirs('results/graphs', exist_ok=True)
    plt.savefig('results/graphs/nlp_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\n✓ Confusion matrix saved to results/graphs/nlp_confusion_matrix.png")
    plt.close()
    
    return y_pred, X_test_tfidf

def evaluate_duplicate_detection(test_df, vectorizer, train_vectors, X_test_tfidf):
    """Evaluate duplicate detection performance"""
    print("\n[4/5] Evaluating duplicate detection...")
    
    y_true_dup = test_df['is_duplicate'].values
    y_pred_dup = []
    
    # For each test sample, find most similar training sample
    n_test_samples = X_test_tfidf.shape[0]
    for i in range(n_test_samples):
        query_vector = X_test_tfidf[i]
        similarities = cosine_similarity(query_vector, train_vectors).flatten()
        max_similarity = similarities.max()
        
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
    print("DUPLICATE DETECTION PERFORMANCE")
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
    print(f"  Method: Cosine similarity on TF-IDF vectors")
    
    return y_pred_dup

def show_example_predictions(test_df, vectorizer, classifier, label_encoder, y_pred, y_pred_dup):
    """Show example predictions from test set"""
    print("\n[5/5] Example predictions from test set...")
    
    # Select 5 random samples
    samples = test_df.sample(n=5, random_state=SEED)
    sample_indices = samples.index.tolist()
    
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
        X_sample = vectorizer.transform([row['processed_text']])
        y_proba = classifier.predict_proba(X_sample)[0]
        pred_idx = classifier.predict(X_sample)[0]
        
        print(f"  Confidence: {y_proba[pred_idx] * 100:.2f}%")
        
        print(f"\n🔄 Duplicate Detection:")
        print(f"  True duplicate:      {row['is_duplicate']}")
        print(f"  Predicted duplicate: {y_pred_dup[i]}")
        print(f"  Correct: {'✓' if row['is_duplicate'] == y_pred_dup[i] else '✗'}")

def main():
    """Main evaluation pipeline"""
    # Load models
    vectorizer, classifier, label_encoder, train_vectors = load_models()
    
    # Load test data
    test_df = load_and_preprocess_test()
    if test_df is None:
        return
    
    # Evaluate classification
    y_pred, X_test_tfidf = evaluate_classification(test_df, vectorizer, classifier, label_encoder)
    
    # Evaluate duplicate detection
    y_pred_dup = evaluate_duplicate_detection(test_df, vectorizer, train_vectors, X_test_tfidf)
    
    # Show examples
    show_example_predictions(test_df, vectorizer, classifier, label_encoder, y_pred, y_pred_dup)
    
    print("\n" + "=" * 80)
    print("✅ NLP PIPELINE EVALUATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

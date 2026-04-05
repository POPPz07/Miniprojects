"""
Threshold Tuning for Duplicate Detection
- Tests different thresholds: 0.6, 0.7, 0.8
- Shows precision/recall tradeoff
- No model retraining required
"""

import pandas as pd
import numpy as np
import pickle
import sys
from scipy.sparse import load_npz
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seed
SEED = 42
np.random.seed(SEED)

def load_models_and_data():
    """Load models and test data"""
    print("=" * 80)
    print("DUPLICATE DETECTION - THRESHOLD TUNING")
    print("=" * 80)
    
    print("\n[1/3] Loading models and data...")
    
    # Load models
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    
    # Load test data
    test_df = pd.read_csv('data/test.csv')
    
    # Preprocess
    processed_texts = []
    for text in test_df['text']:
        try:
            processed, _ = preprocess_pipeline(text, return_string=True)
            processed_texts.append(processed)
        except PreprocessingError:
            processed_texts.append("")
    
    test_df['processed_text'] = processed_texts
    test_df = test_df[test_df['processed_text'] != ""].reset_index(drop=True)
    
    # Transform to TF-IDF
    X_test_tfidf = vectorizer.transform(test_df['processed_text'].values)
    
    print(f"✓ Loaded {len(test_df)} test samples")
    print(f"✓ Training vectors: {train_vectors.shape}")
    
    return test_df, X_test_tfidf, train_vectors

def compute_similarities(X_test_tfidf, train_vectors):
    """Compute all similarities (do this once)"""
    print("\n[2/3] Computing similarities...")
    
    n_test_samples = X_test_tfidf.shape[0]
    max_similarities = []
    
    for i in range(n_test_samples):
        query_vector = X_test_tfidf[i]
        similarities = cosine_similarity(query_vector, train_vectors).flatten()
        max_similarity = similarities.max()
        max_similarities.append(max_similarity)
    
    max_similarities = np.array(max_similarities)
    
    print(f"✓ Computed similarities for {n_test_samples} samples")
    print(f"  Min similarity: {max_similarities.min():.4f}")
    print(f"  Max similarity: {max_similarities.max():.4f}")
    print(f"  Mean similarity: {max_similarities.mean():.4f}")
    print(f"  Median similarity: {np.median(max_similarities):.4f}")
    
    return max_similarities

def evaluate_threshold(y_true, max_similarities, threshold):
    """Evaluate duplicate detection at given threshold"""
    y_pred = (max_similarities > threshold).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    # True positives, false positives, false negatives
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'threshold': threshold,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn
    }

def tune_thresholds(test_df, max_similarities):
    """Test different thresholds"""
    print("\n[3/3] Testing different thresholds...")
    
    y_true = test_df['is_duplicate'].values
    thresholds = [0.6, 0.7, 0.8]
    
    results = []
    
    print("\n" + "=" * 80)
    print("THRESHOLD TUNING RESULTS")
    print("=" * 80)
    
    for threshold in thresholds:
        result = evaluate_threshold(y_true, max_similarities, threshold)
        results.append(result)
        
        print(f"\n📊 Threshold: {threshold}")
        print(f"  Accuracy:  {result['accuracy'] * 100:.2f}%")
        print(f"  Precision: {result['precision'] * 100:.2f}%")
        print(f"  Recall:    {result['recall'] * 100:.2f}%")
        print(f"  F1-Score:  {result['f1'] * 100:.2f}%")
        print(f"\n  Confusion Matrix:")
        print(f"    TP: {result['tp']:4d}  FP: {result['fp']:4d}")
        print(f"    FN: {result['fn']:4d}  TN: {result['tn']:4d}")
    
    return results

def visualize_results(results):
    """Visualize threshold tuning results"""
    print("\n" + "=" * 80)
    print("VISUALIZATION")
    print("=" * 80)
    
    thresholds = [r['threshold'] for r in results]
    precisions = [r['precision'] for r in results]
    recalls = [r['recall'] for r in results]
    f1_scores = [r['f1'] for r in results]
    accuracies = [r['accuracy'] for r in results]
    
    # Create comparison table
    print("\n📋 Comparison Table:")
    print(f"{'Threshold':<12} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 60)
    for r in results:
        print(f"{r['threshold']:<12.1f} {r['accuracy']*100:<11.2f}% {r['precision']*100:<11.2f}% {r['recall']*100:<11.2f}% {r['f1']*100:<11.2f}%")
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Precision vs Recall
    ax1.plot(thresholds, precisions, 'o-', label='Precision', linewidth=2, markersize=8)
    ax1.plot(thresholds, recalls, 's-', label='Recall', linewidth=2, markersize=8)
    ax1.plot(thresholds, f1_scores, '^-', label='F1-Score', linewidth=2, markersize=8)
    ax1.set_xlabel('Threshold', fontsize=12)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.set_title('Precision-Recall Tradeoff', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1])
    
    # Plot 2: Accuracy
    ax2.plot(thresholds, accuracies, 'o-', color='green', linewidth=2, markersize=8)
    ax2.set_xlabel('Threshold', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12)
    ax2.set_title('Accuracy vs Threshold', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1])
    
    plt.tight_layout()
    
    import os
    os.makedirs('results/graphs', exist_ok=True)
    plt.savefig('results/graphs/threshold_tuning.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualization saved to results/graphs/threshold_tuning.png")
    plt.close()

def recommend_threshold(results):
    """Recommend best threshold"""
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    # Find best F1
    best_f1 = max(results, key=lambda x: x['f1'])
    
    # Find best recall
    best_recall = max(results, key=lambda x: x['recall'])
    
    # Find best precision
    best_precision = max(results, key=lambda x: x['precision'])
    
    print(f"\n🎯 Best F1-Score: Threshold = {best_f1['threshold']} (F1 = {best_f1['f1']*100:.2f}%)")
    print(f"   - Precision: {best_f1['precision']*100:.2f}%")
    print(f"   - Recall: {best_f1['recall']*100:.2f}%")
    
    print(f"\n🎯 Best Recall: Threshold = {best_recall['threshold']} (Recall = {best_recall['recall']*100:.2f}%)")
    print(f"   - Precision: {best_recall['precision']*100:.2f}%")
    print(f"   - F1: {best_recall['f1']*100:.2f}%")
    
    print(f"\n🎯 Best Precision: Threshold = {best_precision['threshold']} (Precision = {best_precision['precision']*100:.2f}%)")
    print(f"   - Recall: {best_precision['recall']*100:.2f}%")
    print(f"   - F1: {best_precision['f1']*100:.2f}%")
    
    print("\n💡 Analysis:")
    print("  - Lower threshold (0.6): Higher recall, lower precision")
    print("  - Higher threshold (0.8): Higher precision, lower recall")
    print("  - Tradeoff: Choose based on use case")
    print("    • If false negatives are costly → use lower threshold (0.6)")
    print("    • If false positives are costly → use higher threshold (0.8)")
    
    print("\n⚠️ Note:")
    print("  TF-IDF has fundamental limitations for semantic similarity.")
    print("  Deep Learning with embeddings (Module 4) should perform better.")

def main():
    """Main threshold tuning pipeline"""
    # Load data
    test_df, X_test_tfidf, train_vectors = load_models_and_data()
    
    # Compute similarities once
    max_similarities = compute_similarities(X_test_tfidf, train_vectors)
    
    # Test different thresholds
    results = tune_thresholds(test_df, max_similarities)
    
    # Visualize
    visualize_results(results)
    
    # Recommend
    recommend_threshold(results)
    
    print("\n" + "=" * 80)
    print("✅ THRESHOLD TUNING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

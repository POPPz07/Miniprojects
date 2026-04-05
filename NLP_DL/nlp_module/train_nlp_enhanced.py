"""
ENHANCED NLP Pipeline Training Script
- Word TF-IDF (enhanced parameters)
- Character n-grams TF-IDF
- Word2Vec embeddings (trained from scratch)
- Text statistics features
- XGBoost classifier
- Saves all models for production use
"""

import pandas as pd
import numpy as np
import pickle
import sys
import os
from scipy.sparse import hstack, save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seed
SEED = 42
np.random.seed(SEED)

# Configuration
WORD_TFIDF_MAX_FEATURES = 10000
WORD_TFIDF_NGRAM_RANGE = (1, 3)
CHAR_TFIDF_MAX_FEATURES = 2000
CHAR_TFIDF_NGRAM_RANGE = (3, 5)
WORD2VEC_VECTOR_SIZE = 100
WORD2VEC_WINDOW = 5
WORD2VEC_MIN_COUNT = 2
WORD2VEC_EPOCHS = 10

def load_and_preprocess_data():
    """Load train.csv and apply preprocessing"""
    print("=" * 80)
    print("ENHANCED NLP PIPELINE - TRAINING")
    print("=" * 80)
    
    print("\n[1/10] Loading training data...")
    try:
        train_df = pd.read_csv('data/train.csv')
        print(f"✓ Loaded {len(train_df)} training samples")
    except FileNotFoundError:
        print("❌ train.csv not found. Please run data/prepare_dataset.py first.")
        return None, None, None
    
    print("\n[2/10] Preprocessing text...")
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

def train_word_tfidf(X_train):
    """Train enhanced Word TF-IDF vectorizer"""
    print("\n[3/10] Training Word TF-IDF vectorizer (enhanced)...")
    
    word_vectorizer = TfidfVectorizer(
        max_features=WORD_TFIDF_MAX_FEATURES,
        ngram_range=WORD_TFIDF_NGRAM_RANGE,
        min_df=2,
        sublinear_tf=True,
        analyzer='word'
    )
    
    X_word_tfidf = word_vectorizer.fit_transform(X_train)
    
    print(f"✓ Word TF-IDF vectorizer trained")
    print(f"  Vocabulary size: {len(word_vectorizer.vocabulary_)}")
    print(f"  Feature matrix shape: {X_word_tfidf.shape}")
    print(f"  N-gram range: {WORD_TFIDF_NGRAM_RANGE}")
    print(f"  Max features: {WORD_TFIDF_MAX_FEATURES}")
    
    return word_vectorizer, X_word_tfidf

def train_char_tfidf(X_train):
    """Train Character n-grams TF-IDF vectorizer"""
    print("\n[4/10] Training Character TF-IDF vectorizer...")
    
    char_vectorizer = TfidfVectorizer(
        max_features=CHAR_TFIDF_MAX_FEATURES,
        ngram_range=CHAR_TFIDF_NGRAM_RANGE,
        analyzer='char',
        min_df=2,
        sublinear_tf=True
    )
    
    X_char_tfidf = char_vectorizer.fit_transform(X_train)
    
    print(f"✓ Character TF-IDF vectorizer trained")
    print(f"  Vocabulary size: {len(char_vectorizer.vocabulary_)}")
    print(f"  Feature matrix shape: {X_char_tfidf.shape}")
    print(f"  N-gram range: {CHAR_TFIDF_NGRAM_RANGE}")
    print(f"  Max features: {CHAR_TFIDF_MAX_FEATURES}")
    
    return char_vectorizer, X_char_tfidf

def train_word2vec(X_train):
    """Train Word2Vec model from scratch"""
    print("\n[5/10] Training Word2Vec model...")
    
    # Tokenize texts for Word2Vec
    sentences = [text.split() for text in X_train]
    
    # Train Word2Vec
    word2vec_model = Word2Vec(
        sentences=sentences,
        vector_size=WORD2VEC_VECTOR_SIZE,
        window=WORD2VEC_WINDOW,
        min_count=WORD2VEC_MIN_COUNT,
        workers=4,
        epochs=WORD2VEC_EPOCHS,
        seed=SEED
    )
    
    print(f"✓ Word2Vec model trained")
    print(f"  Vocabulary size: {len(word2vec_model.wv)}")
    print(f"  Vector size: {WORD2VEC_VECTOR_SIZE}")
    print(f"  Window: {WORD2VEC_WINDOW}")
    print(f"  Epochs: {WORD2VEC_EPOCHS}")
    
    # Extract Word2Vec features (average word vectors)
    X_word2vec = []
    for text in X_train:
        tokens = text.split()
        word_vectors = [word2vec_model.wv[token] for token in tokens if token in word2vec_model.wv]
        
        if word_vectors:
            avg_vector = np.mean(word_vectors, axis=0)
        else:
            avg_vector = np.zeros(WORD2VEC_VECTOR_SIZE)
        
        X_word2vec.append(avg_vector)
    
    X_word2vec = np.array(X_word2vec)
    
    print(f"  Word2Vec features shape: {X_word2vec.shape}")
    
    return word2vec_model, X_word2vec

def extract_text_statistics(texts):
    """Extract 10 text statistics features"""
    print("\n[6/10] Extracting text statistics features...")
    
    features = []
    
    for text in texts:
        # 1. Text length (characters)
        text_length = len(text)
        
        # 2. Word count
        words = text.split()
        word_count = len(words)
        
        # 3. Average word length
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        
        # 4. Number of uppercase letters
        uppercase_count = sum(1 for c in text if c.isupper())
        
        # 5. Number of digits
        digit_count = sum(1 for c in text if c.isdigit())
        
        # 6. Number of special characters
        special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        
        # 7. Number of spaces
        space_count = text.count(' ')
        
        # 8. Uppercase ratio
        uppercase_ratio = uppercase_count / len(text) if len(text) > 0 else 0
        
        # 9. Digit ratio
        digit_ratio = digit_count / len(text) if len(text) > 0 else 0
        
        # 10. Special character ratio
        special_ratio = special_count / len(text) if len(text) > 0 else 0
        
        features.append([
            text_length, word_count, avg_word_length,
            uppercase_count, digit_count, special_count, space_count,
            uppercase_ratio, digit_ratio, special_ratio
        ])
    
    X_stats = np.array(features)
    
    print(f"✓ Extracted text statistics")
    print(f"  Features shape: {X_stats.shape}")
    print(f"  Features: length, word_count, avg_word_length, uppercase, digits, special, spaces, ratios")
    
    # Normalize statistics
    scaler = StandardScaler()
    X_stats_scaled = scaler.fit_transform(X_stats)
    
    print(f"  ✓ Normalized using StandardScaler")
    
    return X_stats_scaled, scaler

def combine_features(X_word_tfidf, X_char_tfidf, X_word2vec, X_stats):
    """Combine all features into single feature matrix"""
    print("\n[7/10] Combining all features...")
    
    # Convert dense arrays to sparse for efficient concatenation
    from scipy.sparse import csr_matrix
    X_word2vec_sparse = csr_matrix(X_word2vec)
    X_stats_sparse = csr_matrix(X_stats)
    
    # Combine all features
    X_combined = hstack([
        X_word_tfidf,      # Word TF-IDF (10,000 features)
        X_char_tfidf,      # Char TF-IDF (2,000 features)
        X_word2vec_sparse, # Word2Vec (100 features)
        X_stats_sparse     # Text stats (10 features)
    ])
    
    print(f"✓ Combined features")
    print(f"  Word TF-IDF: {X_word_tfidf.shape[1]} features")
    print(f"  Char TF-IDF: {X_char_tfidf.shape[1]} features")
    print(f"  Word2Vec: {X_word2vec.shape[1]} features")
    print(f"  Text stats: {X_stats.shape[1]} features")
    print(f"  Total: {X_combined.shape[1]} features")
    print(f"  Combined shape: {X_combined.shape}")
    
    return X_combined

def train_xgboost_classifier(X_combined, y_train):
    """Train XGBoost classifier"""
    print("\n[8/10] Training XGBoost classifier...")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_train)
    
    # Train XGBoost
    classifier = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=SEED,
        n_jobs=-1,
        eval_metric='mlogloss'
    )
    
    classifier.fit(X_combined, y_encoded)
    
    # Training accuracy
    y_pred = classifier.predict(X_combined)
    train_accuracy = accuracy_score(y_encoded, y_pred)
    
    print(f"✓ XGBoost classifier trained")
    print(f"  Training accuracy: {train_accuracy * 100:.2f}%")
    print(f"  Classes: {list(label_encoder.classes_)}")
    print(f"  N estimators: 100")
    print(f"  Max depth: 6")
    
    return classifier, label_encoder

def save_all_models(word_vectorizer, char_vectorizer, word2vec_model, stats_scaler, 
                    classifier, label_encoder, X_word_tfidf):
    """Save all trained models"""
    print("\n[9/10] Saving all models...")
    
    os.makedirs('models', exist_ok=True)
    
    # 1. Word TF-IDF vectorizer
    with open('models/word_tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(word_vectorizer, f)
    print("✓ Saved word_tfidf_vectorizer.pkl")
    
    # 2. Character TF-IDF vectorizer
    with open('models/char_tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(char_vectorizer, f)
    print("✓ Saved char_tfidf_vectorizer.pkl")
    
    # 3. Word2Vec model
    with open('models/word2vec_model.pkl', 'wb') as f:
        pickle.dump(word2vec_model, f)
    print("✓ Saved word2vec_model.pkl")
    
    # 4. Text statistics scaler
    with open('models/text_stats_scaler.pkl', 'wb') as f:
        pickle.dump(stats_scaler, f)
    print("✓ Saved text_stats_scaler.pkl")
    
    # 5. XGBoost classifier
    with open('models/nlp_classifier_enhanced.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    print("✓ Saved nlp_classifier_enhanced.pkl")
    
    # 6. Label encoder
    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    print("✓ Saved label_encoder.pkl")
    
    # 7. Training word TF-IDF vectors (for duplicate detection)
    save_npz('models/train_word_tfidf_vectors.npz', X_word_tfidf)
    print("✓ Saved train_word_tfidf_vectors.npz")
    
    print(f"\n✓ All 7 models saved to models/ directory")

def demonstrate_predictions(train_df, word_vectorizer, char_vectorizer, word2vec_model, 
                           stats_scaler, classifier, label_encoder):
    """Show sample predictions"""
    print("\n[10/10] Sample predictions...")
    
    samples = train_df.sample(n=5, random_state=SEED)
    
    print("\n" + "=" * 80)
    print("SAMPLE PREDICTIONS")
    print("=" * 80)
    
    for idx, (i, row) in enumerate(samples.iterrows(), 1):
        print(f"\nSample {idx}:")
        print(f"  Raw text: {row['text'][:80]}...")
        print(f"  Processed: {row['processed_text'][:80]}...")
        print(f"  True category: {row['category']}")
        
        # Extract features
        X_word = word_vectorizer.transform([row['processed_text']])
        X_char = char_vectorizer.transform([row['processed_text']])
        
        # Word2Vec
        tokens = row['processed_text'].split()
        word_vectors = [word2vec_model.wv[token] for token in tokens if token in word2vec_model.wv]
        if word_vectors:
            X_w2v = np.mean(word_vectors, axis=0).reshape(1, -1)
        else:
            X_w2v = np.zeros((1, WORD2VEC_VECTOR_SIZE))
        
        # Text stats
        X_stats = extract_text_statistics([row['text']])[0]
        X_stats_scaled = stats_scaler.transform(X_stats)
        
        # Combine
        from scipy.sparse import csr_matrix
        X_combined = hstack([X_word, X_char, csr_matrix(X_w2v), csr_matrix(X_stats_scaled)])
        
        # Predict
        y_pred_encoded = classifier.predict(X_combined)[0]
        y_pred_proba = classifier.predict_proba(X_combined)[0]
        y_pred = label_encoder.inverse_transform([y_pred_encoded])[0]
        
        print(f"  Predicted category: {y_pred}")
        print(f"  Confidence: {y_pred_proba[y_pred_encoded] * 100:.2f}%")
        
        print(f"  All probabilities:")
        for class_idx, prob in enumerate(y_pred_proba):
            class_name = label_encoder.inverse_transform([class_idx])[0]
            print(f"    {class_name}: {prob * 100:.2f}%")

def main():
    """Main enhanced NLP training pipeline"""
    # Load and preprocess
    train_df, X_train, y_train = load_and_preprocess_data()
    if train_df is None:
        return
    
    # Train Word TF-IDF
    word_vectorizer, X_word_tfidf = train_word_tfidf(X_train)
    
    # Train Character TF-IDF
    char_vectorizer, X_char_tfidf = train_char_tfidf(X_train)
    
    # Train Word2Vec
    word2vec_model, X_word2vec = train_word2vec(X_train)
    
    # Extract text statistics
    X_stats, stats_scaler = extract_text_statistics(train_df['text'].values)
    
    # Combine all features
    X_combined = combine_features(X_word_tfidf, X_char_tfidf, X_word2vec, X_stats)
    
    # Train XGBoost classifier
    classifier, label_encoder = train_xgboost_classifier(X_combined, y_train)
    
    # Save all models
    save_all_models(word_vectorizer, char_vectorizer, word2vec_model, stats_scaler,
                    classifier, label_encoder, X_word_tfidf)
    
    # Demonstrate predictions
    demonstrate_predictions(train_df, word_vectorizer, char_vectorizer, word2vec_model,
                           stats_scaler, classifier, label_encoder)
    
    print("\n" + "=" * 80)
    print("✅ ENHANCED NLP PIPELINE TRAINING COMPLETE")
    print("=" * 80)
    print("\nSaved models (7 files):")
    print("  1. models/word_tfidf_vectorizer.pkl")
    print("  2. models/char_tfidf_vectorizer.pkl")
    print("  3. models/word2vec_model.pkl")
    print("  4. models/text_stats_scaler.pkl")
    print("  5. models/nlp_classifier_enhanced.pkl")
    print("  6. models/label_encoder.pkl")
    print("  7. models/train_word_tfidf_vectors.npz")
    print("\n📊 Feature Summary:")
    print("  - Word TF-IDF: 10,000 features (1-3 grams)")
    print("  - Char TF-IDF: 2,000 features (3-5 grams)")
    print("  - Word2Vec: 100 features (trained from scratch)")
    print("  - Text Stats: 10 features (length, counts, ratios)")
    print("  - Total: 12,110 features")
    print("\n🎯 Classifier: XGBoost (100 estimators, max_depth=6)")

if __name__ == "__main__":
    main()

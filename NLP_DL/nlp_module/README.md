# NLP Pipeline Module

## Overview
Traditional NLP approach using TF-IDF feature extraction and Logistic Regression for ticket classification and duplicate detection.

## Components

### 1. Training Script (`train_nlp.py`)
Trains the NLP pipeline on `data/train.csv`:
- Applies preprocessing from `preprocessing/text_cleaner.py`
- Trains TF-IDF vectorizer
- Trains Logistic Regression classifier
- Saves all models

### 2. Verification Script (`verify_nlp.py`)
Verifies all models are working correctly:
- Loads saved models
- Tests predictions on sample texts
- Tests duplicate detection

## Saved Models

### `models/tfidf_vectorizer.pkl`
- TF-IDF vectorizer with 5,000 features
- Configuration: max_features=5000, ngram_range=(1,2), min_df=2
- Vocabulary size: 5,000 terms
- Matrix sparsity: 99.77%

### `models/nlp_classifier.pkl`
- Logistic Regression classifier
- 4 classes: account, billing, delivery, technical
- Training accuracy: 98.37%
- Coefficient shape: (4, 5000)

### `models/label_encoder.pkl`
- Label encoder for category mapping
- Classes: ['account', 'billing', 'delivery', 'technical']

### `models/train_tfidf_vectors.npz`
- Precomputed TF-IDF vectors for all training samples
- Shape: (4675, 5000)
- Used for efficient duplicate detection via cosine similarity

## Usage

### Training
```bash
python nlp_module/train_nlp.py
```

### Verification
```bash
python nlp_module/verify_nlp.py
```

### Prediction Example
```python
import pickle
from preprocessing.text_cleaner import preprocess_pipeline

# Load models
vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))
classifier = pickle.load(open('models/nlp_classifier.pkl', 'rb'))
label_encoder = pickle.load(open('models/label_encoder.pkl', 'rb'))

# Predict
text = "My payment failed"
processed, _ = preprocess_pipeline(text)
X = vectorizer.transform([processed])
y_pred = classifier.predict(X)[0]
category = label_encoder.inverse_transform([y_pred])[0]
print(f"Category: {category}")
```

### Duplicate Detection Example
```python
import pickle
import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.text_cleaner import preprocess_pipeline

# Load models
vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))
train_vectors = load_npz('models/train_tfidf_vectors.npz')

# Find duplicates
text = "My payment didn't go through"
processed, _ = preprocess_pipeline(text)
query_vector = vectorizer.transform([processed])
similarities = cosine_similarity(query_vector, train_vectors).flatten()

# Get top 3 most similar
top_indices = np.argsort(similarities)[::-1][:3]
for idx in top_indices:
    print(f"Similarity: {similarities[idx]:.4f}")

# Check if duplicate (threshold = 0.8)
is_duplicate = similarities[top_indices[0]] > 0.8
```

## Performance

### Classification
- Training accuracy: 98.37%
- All 4 categories correctly classified in test samples

### Duplicate Detection
- Uses cosine similarity on TF-IDF vectors
- Threshold: 0.8
- Successfully detects near-duplicate tickets (similarity > 0.98)

## Features

✅ Shared preprocessing pipeline
✅ Efficient TF-IDF vectorization
✅ High classification accuracy
✅ Fast duplicate detection with precomputed vectors
✅ Returns top 3 similar tickets
✅ All models saved and reusable

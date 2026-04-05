# App.py Update Guide for Enhanced NLP Models

## 🎯 Changes Required

The app.py needs to be updated to load and use the new enhanced NLP models:
- Character TF-IDF vectorizer
- Word2Vec model  
- XGBoost classifier (instead of Logistic Regression)

## 📝 Step-by-Step Updates

### 1. Update Imports (Add at top)

```python
from scipy.sparse import hstack, csr_matrix
from gensim.models import Word2Vec
```

### 2. Replace `load_nlp_models()` function

**OLD CODE (lines ~151-166):**
```python
@st.cache_resource
def load_nlp_models():
    """Load NLP models"""
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open('models/nlp_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    
    return vectorizer, classifier, label_encoder, train_vectors
```

**NEW CODE:**
```python
@st.cache_resource
def load_nlp_models():
    """Load Enhanced NLP models"""
    # Load vectorizers
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        word_tfidf = pickle.load(f)
    
    with open('models/char_vectorizer.pkl', 'rb') as f:
        char_tfidf = pickle.load(f)
    
    # Load Word2Vec model
    with open('models/word2vec_model.pkl', 'rb') as f:
        w2v_model = pickle.load(f)
    
    # Load XGBoost classifier
    with open('models/nlp_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    
    # Load label encoder
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Load training TF-IDF vectors (for duplicate detection)
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    
    return word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors
```

### 3. Add Helper Function for Word2Vec Embeddings

**ADD THIS NEW FUNCTION (after load_nlp_models):**
```python
def get_document_embedding(tokens, w2v_model):
    """Get document embedding by averaging word vectors"""
    vectors = []
    for token in tokens:
        if token in w2v_model.wv:
            vectors.append(w2v_model.wv[token])
    
    if len(vectors) == 0:
        return np.zeros(w2v_model.wv.vector_size)
    
    return np.mean(vectors, axis=0)

def extract_text_statistics(text):
    """Extract 10 statistical features from text"""
    if not text or text.strip() == '':
        return np.zeros(10)
    
    char_count = len(text)
    word_count = len(text.split())
    unique_word_count = len(set(text.split()))
    avg_word_length = np.mean([len(word) for word in text.split()]) if word_count > 0 else 0
    exclamation_count = text.count('!')
    question_count = text.count('?')
    uppercase_ratio = sum(1 for c in text if c.isupper()) / char_count if char_count > 0 else 0
    digit_ratio = sum(1 for c in text if c.isdigit()) / char_count if char_count > 0 else 0
    lexical_diversity = unique_word_count / word_count if word_count > 0 else 0
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    return np.array([
        char_count, word_count, unique_word_count, avg_word_length,
        exclamation_count, question_count, uppercase_ratio, digit_ratio,
        lexical_diversity, sentence_count
    ])
```

### 4. Replace `predict_nlp()` function

**OLD CODE (lines ~205-230):**
```python
def predict_nlp(text, vectorizer, classifier, label_encoder, train_vectors):
    """Predict using NLP pipeline"""
    processed, error = preprocess_text(text)
    if error:
        return None, error
    
    # Classification
    X_tfidf = vectorizer.transform([processed])
    y_pred = classifier.predict(X_tfidf)[0]
    y_proba = classifier.predict_proba(X_tfidf)[0]
    category = label_encoder.inverse_transform([y_pred])[0]
    confidence = y_proba[y_pred] * 100
    
    # Duplicate detection
    similarities = cosine_similarity(X_tfidf, train_vectors).flatten()
    top_3_indices = np.argsort(similarities)[-3:][::-1]
    top_3_similarities = similarities[top_3_indices]
    max_similarity = similarities.max()
    is_duplicate = 1 if max_similarity > NLP_THRESHOLD else 0
    
    return {
        'category': category,
        'confidence': confidence,
        'is_duplicate': is_duplicate,
        'max_similarity': max_similarity,
        'top_3_similarities': top_3_similarities.tolist(),
        'all_probabilities': {label_encoder.classes_[i]: y_proba[i] * 100 for i in range(len(y_proba))}
    }, None
```

**NEW CODE:**
```python
def predict_nlp(text, word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors):
    """Predict using Enhanced NLP pipeline"""
    processed, error = preprocess_text(text)
    if error:
        return None, error
    
    # Extract all features
    # 1. Word TF-IDF
    X_word_tfidf = word_tfidf.transform([processed])
    
    # 2. Character TF-IDF
    X_char_tfidf = char_tfidf.transform([processed])
    
    # 3. Word2Vec embeddings
    from preprocessing.text_cleaner import preprocess_pipeline
    tokens = preprocess_pipeline(processed, return_string=False)
    X_word2vec = get_document_embedding(tokens, w2v_model).reshape(1, -1)
    
    # 4. Text statistics
    X_stats = extract_text_statistics(text).reshape(1, -1)
    
    # Combine all features
    X_combined = hstack([
        X_word_tfidf,
        X_char_tfidf,
        csr_matrix(X_word2vec),
        csr_matrix(X_stats)
    ])
    
    # Classification
    y_pred = classifier.predict(X_combined)[0]
    y_proba = classifier.predict_proba(X_combined)[0]
    category = label_encoder.inverse_transform([y_pred])[0]
    confidence = y_proba[y_pred] * 100
    
    # Duplicate detection (using Word TF-IDF only for consistency)
    similarities = cosine_similarity(X_word_tfidf, train_vectors).flatten()
    top_3_indices = np.argsort(similarities)[-3:][::-1]
    top_3_similarities = similarities[top_3_indices]
    max_similarity = similarities.max()
    is_duplicate = 1 if max_similarity > NLP_THRESHOLD else 0
    
    return {
        'category': category,
        'confidence': confidence,
        'is_duplicate': is_duplicate,
        'max_similarity': max_similarity,
        'top_3_similarities': top_3_similarities.tolist(),
        'all_probabilities': {label_encoder.classes_[i]: y_proba[i] * 100 for i in range(len(y_proba))}
    }, None
```

### 5. Update Model Loading Calls

**Find all places where models are loaded and update:**

**OLD:**
```python
vectorizer, classifier, label_encoder, train_vectors = load_nlp_models()
```

**NEW:**
```python
word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors = load_nlp_models()
```

**OLD:**
```python
nlp_result, error = predict_nlp(text, vectorizer, classifier, label_encoder, train_vectors)
```

**NEW:**
```python
nlp_result, error = predict_nlp(text, word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors)
```

### 6. Update UI Text

Find and replace:
- "Logistic Regression" → "XGBoost"
- "TF-IDF" → "Enhanced TF-IDF + Word2Vec"

**Example locations:**
- Model Comparison page
- About page
- Any metric displays

### 7. Update Batch Processing

In the batch processing function, update the model unpacking:

**OLD:**
```python
vectorizer, classifier, label_encoder, train_vectors = load_nlp_models()
```

**NEW:**
```python
word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors = load_nlp_models()
```

And update the prediction call similarly.

## ✅ Testing Checklist

After making changes:

1. ✅ App starts without errors
2. ✅ Models load successfully
3. ✅ Single ticket prediction works (NLP)
4. ✅ Single ticket prediction works (DL)
5. ✅ Batch processing works
6. ✅ Model comparison page displays correctly
7. ✅ All metrics show proper values

## 🔍 Quick Find & Replace

Use these find/replace operations in your editor:

1. Find: `def load_nlp_models():`
   - Replace with the new function (see above)

2. Find: `vectorizer, classifier, label_encoder, train_vectors = load_nlp_models()`
   - Replace: `word_tfidf, char_tfidf, w2v_model, classifier, label_encoder, train_vectors = load_nlp_models()`

3. Find: `predict_nlp(text, vectorizer, classifier`
   - Replace: `predict_nlp(text, word_tfidf, char_tfidf, w2v_model, classifier`

4. Find: `"Logistic Regression"`
   - Replace: `"XGBoost"`

## 📦 Required New Model Files

Make sure these files exist in `models/` directory:
- ✅ `char_vectorizer.pkl` (NEW)
- ✅ `word2vec_model.pkl` (NEW)
- ✅ `nlp_classifier.pkl` (XGBoost, not LogReg)
- ✅ `tfidf_vectorizer.pkl` (enhanced parameters)
- ✅ `train_tfidf_vectors.npz`
- ✅ `label_encoder.pkl`
- ✅ `dl_model.h5`
- ✅ `tokenizer.pkl`
- ✅ `train_embeddings_normalized.npy`

## 🚀 Deployment Notes

When deploying to Streamlit Cloud:
- Ensure all model files are committed to Git (if under 100MB each)
- Or use Git LFS for large files
- Update requirements.txt with: `gensim`, `xgboost`
- Test locally first with `streamlit run app.py`

## ⚠️ Important Notes

1. The function signature changes from 4 parameters to 6 parameters
2. All calling code must be updated
3. The preprocessing pipeline is reused (no changes needed)
4. Duplicate detection still uses Word TF-IDF for consistency
5. XGBoost may have slightly different probability outputs than LogReg

## 🎯 Expected Performance

After updates:
- Classification accuracy: 93-95% (up from 91%)
- Duplicate detection F1: 35-45% (up from 10%)
- Response time: Similar (XGBoost is fast)
- Memory usage: Slightly higher (more models loaded)

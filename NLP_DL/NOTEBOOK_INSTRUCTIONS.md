# Complete Training Pipeline Notebook - Instructions

## 📋 Overview

The `complete_training_pipeline.ipynb` currently contains the DL (LSTM) training pipeline. You need to add the Enhanced NLP training sections BEFORE the DL sections.

## 🎯 Required Structure

The final notebook should have this structure:

```
Part 1: Setup & Data Loading (Cells 1-5) ✅ DONE
Part 2: Enhanced NLP Training (Cells 6-20) ⚠️ ADD THIS
Part 3: Deep Learning Training (Cells 21-32) ✅ DONE (currently cells 1-12)
Part 4: Evaluation & Comparison (Cells 33-43) ✅ DONE (currently cells 13-21)
Part 5: Model Download (Cells 44-46) ✅ DONE (currently cell 21)
```

## 📝 Cells to ADD (Part 2: Enhanced NLP Training)

Insert these cells AFTER Cell 5 (data loading) and BEFORE the current DL training cells:

### Cell 6: Word TF-IDF Features (Enhanced)

```python
print('='*80)
print('FEATURE 1: WORD TF-IDF (ENHANCED)')
print('='*80)

# Enhanced parameters
word_tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
    sublinear_tf=True,
    min_df=2,
    max_df=0.95
)

print('\\nFitting Word TF-IDF vectorizer...')
X_word_tfidf = word_tfidf.fit_transform(train_df['processed_text'])

print(f'✓ Word TF-IDF shape: {X_word_tfidf.shape}')
print(f'  Actual features: {len(word_tfidf.get_feature_names_out())}')
```

### Cell 7: Character TF-IDF Features (NEW)

```python
print('='*80)
print('FEATURE 2: CHARACTER TF-IDF (NEW)')
print('='*80)

char_tfidf = TfidfVectorizer(
    analyzer='char',
    ngram_range=(3, 5),
    max_features=2000,
    sublinear_tf=True,
    min_df=2
)

print('\\nFitting Character TF-IDF vectorizer...')
X_char_tfidf = char_tfidf.fit_transform(train_df['processed_text'])

print(f'✓ Character TF-IDF shape: {X_char_tfidf.shape}')
```

### Cell 8: Word2Vec Embeddings (NEW)

```python
print('='*80)
print('FEATURE 3: WORD2VEC EMBEDDINGS (TRAINED FROM SCRATCH)')
print('='*80)

# Prepare tokenized sentences
print('\\nPreparing tokenized sentences...')
tokenized_sentences = train_df['processed_text'].apply(
    lambda x: preprocess_pipeline(x, return_string=False)
).tolist()
tokenized_sentences = [sent for sent in tokenized_sentences if len(sent) > 0]

# Train Word2Vec
print('\\nTraining Word2Vec model...')
w2v_model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=100,
    window=5,
    min_count=2,
    workers=4,
    epochs=10,
    seed=SEED
)

print(f'✓ Vocabulary size: {len(w2v_model.wv)}')

# Create document embeddings
def get_document_embedding(tokens, model):
    vectors = [model.wv[token] for token in tokens if token in model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.wv.vector_size)

X_word2vec = np.array([
    get_document_embedding(tokens, w2v_model)
    for tokens in tokenized_sentences
])

print(f'✓ Word2Vec embeddings shape: {X_word2vec.shape}')
```

### Cell 9: Text Statistics Features (NEW)

```python
print('='*80)
print('FEATURE 4: TEXT STATISTICS (NEW)')
print('='*80)

def extract_text_statistics(text):
    if not text or text.strip() == '':
        return np.zeros(10)
    
    char_count = len(text)
    word_count = len(text.split())
    unique_word_count = len(set(text.split()))
    avg_word_length = np.mean([len(w) for w in text.split()]) if word_count > 0 else 0
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

X_stats = np.array([extract_text_statistics(text) for text in train_df['text']])
print(f'✓ Text statistics shape: {X_stats.shape}')
```

### Cell 10: Combine All Features

```python
print('='*80)
print('COMBINING ALL FEATURES')
print('='*80)

X_combined = hstack([
    X_word_tfidf,
    X_char_tfidf,
    csr_matrix(X_word2vec),
    csr_matrix(X_stats)
])

print(f'✓ Combined features shape: {X_combined.shape}')
```

### Cell 11: Encode Labels

```python
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(train_df['category'])

print(f'✓ Labels encoded')
print(f'  Classes: {list(label_encoder.classes_)}')
```

### Cell 12: Train XGBoost Classifier

```python
print('='*80)
print('TRAINING XGBOOST CLASSIFIER')
print('='*80)

nlp_classifier = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=len(label_encoder.classes_),
    max_depth=6,
    learning_rate=0.1,
    n_estimators=200,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=SEED,
    n_jobs=-1
)

print('\\nTraining XGBoost classifier...')
nlp_classifier.fit(X_combined, y_train, verbose=False)
print('✓ XGBoost classifier trained!')
```

### Cell 13-15: Save NLP Models

```python
# Cell 13: Save classifiers and vectorizers
with open('nlp_classifier.pkl', 'wb') as f:
    pickle.dump(nlp_classifier, f)
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(word_tfidf, f)
with open('char_vectorizer.pkl', 'wb') as f:
    pickle.dump(char_tfidf, f)
with open('word2vec_model.pkl', 'wb') as f:
    pickle.dump(w2v_model, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print('✓ All NLP models saved!')

# Cell 14: Save training vectors
save_npz('train_tfidf_vectors.npz', X_word_tfidf)
print('✓ Training TF-IDF vectors saved!')

# Cell 15: NLP Training Evaluation
y_train_pred = nlp_classifier.predict(X_combined)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f'\\nNLP Training Accuracy: {train_accuracy * 100:.2f}%')
```

## ✅ What's Already Done

The current notebook already has:
- ✅ DL training (LSTM)
- ✅ DL evaluation on test set
- ✅ Duplicate detection with LSTM embeddings
- ✅ Model download sections

## 🔄 What You Need to Do

1. Open `notebooks/complete_training_pipeline.ipynb` in Jupyter/Colab
2. Insert the NLP cells (6-15) AFTER the data loading section
3. Renumber all subsequent cells appropriately
4. Add a comparison section at the end that compares NLP vs DL metrics

## 📊 Expected Final Structure

```
Cells 1-5:   Setup & Data Loading
Cells 6-20:  Enhanced NLP Training (ADD THESE)
Cells 21-32: Deep Learning Training (EXISTING, renumber)
Cells 33-43: Evaluation & Comparison (EXISTING, renumber + enhance)
Cells 44-46: Model Download (EXISTING, renumber)
```

## 🎯 Alternative: Use Existing Notebook

If you prefer, you can:
1. Keep the current `complete_training_pipeline.ipynb` for DL only
2. Create a separate `nlp_training_enhanced.ipynb` for NLP training
3. Run both notebooks separately
4. Compare results manually

This approach is simpler and avoids potential conflicts.

## 📝 Notes

- The current notebook is fully functional for DL training
- All preprocessing functions are already defined
- The label_encoder will be shared between NLP and DL
- Make sure to upload both train.csv and test.csv when running

## ⚡ Quick Start

For fastest results:
1. Use the current notebook AS-IS for DL training
2. Create NLP models using the code snippets above in a separate notebook
3. Download all models
4. Update app.py to load both sets of models

This modular approach is cleaner and less error-prone!

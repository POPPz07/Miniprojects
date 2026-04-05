# Design Document: Project Restructuring for Production-Ready Deployment

## Overview

This design document specifies the technical architecture and implementation details for restructuring a customer support ticket classification system to be production-ready. The system employs dual AI approaches: a traditional NLP pipeline (TF-IDF + XGBoost) and a Deep Learning pipeline (LSTM neural networks) for ticket classification and duplicate detection.

### System Goals

1. **Unified Training**: Consolidate all model training into a single, comprehensive Jupyter/Colab notebook
2. **Enhanced Performance**: Improve model accuracy and duplicate detection through feature engineering
3. **Production Readiness**: Clean up codebase, consolidate documentation, and prepare for cloud deployment
4. **Maintainability**: Simplify project structure and eliminate redundant files

### Key Design Principles

- **Consistency**: Use shared preprocessing pipeline across all components
- **Modularity**: Separate concerns between training, inference, and UI
- **Reproducibility**: Fixed random seeds and deterministic operations
- **Scalability**: Efficient feature extraction and model serving
- **Usability**: Clear documentation and intuitive interfaces

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRAINING PHASE (Colab)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │  train.csv   │                                              │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ├──────────────────┬────────────────────┐             │
│         │                  │                    │             │
│         ▼                  ▼                    ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │Preprocessing│    │Preprocessing│    │Preprocessing│      │
│  │   Pipeline  │    │   Pipeline  │    │   Pipeline  │      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│         │                  │                    │             │
│         ▼                  ▼                    ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Enhanced   │    │     LSTM    │    │  Evaluation │      │
│  │     NLP     │    │   Training  │    │ & Comparison│      │
│  │  Training   │    │             │    │             │      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│         │                  │                    │             │
│         └──────────────────┴────────────────────┘             │
│                            │                                   │
│                            ▼                                   │
│                  ┌──────────────────┐                         │
│                  │  Model Artifacts │                         │
│                  │   (7 NLP files)  │                         │
│                  │   (4 DL files)   │                         │
│                  └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   INFERENCE PHASE (Streamlit)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │  User Input  │                                              │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐                                              │
│  │Preprocessing│                                              │
│  │   Pipeline  │                                              │
│  └──────┬──────┘                                              │
│         │                                                       │
│         ├──────────────────┬────────────────────┐             │
│         │                  │                    │             │
│         ▼                  ▼                    ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │     NLP     │    │      DL     │    │  Duplicate  │      │
│  │Classifica-  │    │Classifica-  │    │  Detection  │      │
│  │    tion     │    │    tion     │    │  (Both)     │      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│         │                  │                    │             │
│         └──────────────────┴────────────────────┘             │
│                            │                                   │
│                            ▼                                   │
│                  ┌──────────────────┐                         │
│                  │  Streamlit UI    │                         │
│                  │  (Side-by-side   │                         │
│                  │   Comparison)    │                         │
│                  └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Training Flow**:
   - Raw CSV → Preprocessing → Feature Extraction → Model Training → Model Artifacts
   - Separate pipelines for NLP and DL with shared preprocessing
   - Evaluation on test set with metrics comparison

2. **Inference Flow**:
   - User Input → Preprocessing → Parallel Prediction (NLP + DL) → UI Display
   - Duplicate detection using cosine similarity on embeddings
   - Real-time comparison of both approaches

## Components and Interfaces

### 1. Unified Training Notebook

**File**: `notebooks/complete_training_pipeline.ipynb`

**Purpose**: Single notebook for training all models in Google Colab environment

**Structure** (5 Parts):

#### Part 1: Setup & Data Loading
- Install dependencies
- Import libraries
- Download NLTK data
- Upload train.csv
- Define preprocessing functions

#### Part 2: Enhanced NLP Training
- Word TF-IDF vectorizer (10,000 features, 1-3 grams)
- Character TF-IDF vectorizer (2,000 features, 3-5 grams)
- Word2Vec embeddings (100 dimensions)
- Text statistics features (10 features)
- XGBoost classifier (200 estimators)
- Save 7 model artifacts

#### Part 3: Deep Learning Training
- Tokenization and padding (max_length=100)
- LSTM architecture:
  - Embedding(vocab_size, 128, mask_zero=True)
  - LSTM(64)
  - Dropout(0.2)
  - Dense(32, relu)
  - Dense(4, softmax)
- Train for 10 epochs
- Extract LSTM embeddings for duplicate detection
- Save 4 model artifacts

#### Part 4: Evaluation & Comparison
- Load test.csv
- Evaluate classification accuracy
- Evaluate duplicate detection F1-score
- Generate confusion matrices
- Compare NLP vs DL performance
- Threshold tuning for duplicate detection

#### Part 5: Model Download
- Download all trained artifacts
- Provide instructions for deployment

**Key Interfaces**:

```python
# Preprocessing Interface (shared across all parts)
def preprocess_pipeline(text: str, return_string: bool = True) -> Tuple[Union[str, List[str]], Dict]:
    """
    Complete preprocessing pipeline
    
    Args:
        text: Raw input text
        return_string: If True, return joined string; if False, return token list
        
    Returns:
        processed: Processed text (string or tokens)
        metadata: Dict with warnings and statistics
    """
    pass

# NLP Feature Extraction Interface
def extract_nlp_features(texts: List[str]) -> scipy.sparse.csr_matrix:
    """
    Extract combined NLP features
    
    Args:
        texts: List of preprocessed texts
        
    Returns:
        X_combined: Combined feature matrix (12,110 features)
            - Word TF-IDF: 10,000 features
            - Char TF-IDF: 2,000 features
            - Word2Vec: 100 features
            - Text stats: 10 features
    """
    pass

# DL Sequence Preparation Interface
def prepare_dl_sequences(texts: List[str], tokenizer, max_length: int = 100) -> np.ndarray:
    """
    Convert texts to padded sequences
    
    Args:
        texts: List of preprocessed texts
        tokenizer: Fitted tokenizer
        max_length: Maximum sequence length
        
    Returns:
        X_padded: Padded sequences (n_samples, max_length)
    """
    pass

# Embedding Extraction Interface
def extract_lstm_embeddings(sequences: np.ndarray, embedding_model) -> np.ndarray:
    """
    Extract LSTM layer embeddings
    
    Args:
        sequences: Padded sequences
        embedding_model: Model that outputs LSTM layer
        
    Returns:
        embeddings_normalized: L2-normalized embeddings (n_samples, 64)
    """
    pass
```

### 2. Enhanced NLP Pipeline

**Components**:

1. **Word TF-IDF Vectorizer**
   - Configuration:
     - max_features: 10,000
     - ngram_range: (1, 3)
     - min_df: 2
     - sublinear_tf: True
     - analyzer: 'word'
   - Purpose: Capture word-level patterns and phrases

2. **Character TF-IDF Vectorizer**
   - Configuration:
     - max_features: 2,000
     - ngram_range: (3, 5)
     - analyzer: 'char'
     - min_df: 2
     - sublinear_tf: True
   - Purpose: Handle typos and misspellings

3. **Word2Vec Embeddings**
   - Configuration:
     - vector_size: 100
     - window: 5
     - min_count: 2
     - epochs: 10
     - seed: 42
   - Purpose: Capture semantic relationships

4. **Text Statistics Features**
   - Features (10 total):
     1. Text length (characters)
     2. Word count
     3. Average word length
     4. Uppercase count
     5. Digit count
     6. Special character count
     7. Space count
     8. Uppercase ratio
     9. Digit ratio
     10. Special character ratio
   - Normalization: StandardScaler

5. **XGBoost Classifier**
   - Configuration:
     - n_estimators: 200
     - max_depth: 6
     - learning_rate: 0.1
     - random_state: 42
     - eval_metric: 'mlogloss'
   - Purpose: Multi-class classification

**Feature Combination Strategy**:
```python
X_combined = hstack([
    X_word_tfidf,      # (n_samples, 10000)
    X_char_tfidf,      # (n_samples, 2000)
    X_word2vec_sparse, # (n_samples, 100)
    X_stats_sparse     # (n_samples, 10)
])
# Total: (n_samples, 12110)
```

**Model Artifacts** (7 files):
1. `word_tfidf_vectorizer.pkl` - Word TF-IDF vectorizer
2. `char_tfidf_vectorizer.pkl` - Character TF-IDF vectorizer
3. `word2vec_model.pkl` - Word2Vec model
4. `text_stats_scaler.pkl` - StandardScaler for text statistics
5. `nlp_classifier_enhanced.pkl` - XGBoost classifier
6. `label_encoder.pkl` - Label encoder
7. `train_word_tfidf_vectors.npz` - Training vectors for duplicate detection

### 3. Deep Learning Pipeline

**Architecture**:

```
Input (batch_size, 100)
    ↓
Embedding Layer (vocab_size, 128, mask_zero=True)
    ↓
LSTM Layer (64 units, return_sequences=False)
    ↓
Dropout Layer (0.2)
    ↓
Dense Layer (32 units, relu activation)
    ↓
Output Layer (4 units, softmax activation)
```

**Configuration**:
- MAX_LENGTH: 100
- EMBEDDING_DIM: 128
- LSTM_UNITS: 64
- DROPOUT_RATE: 0.2
- DENSE_UNITS: 32
- EPOCHS: 10
- BATCH_SIZE: 32
- VALIDATION_SPLIT: 0.2
- OPTIMIZER: Adam
- LOSS: categorical_crossentropy

**Tokenization Strategy**:
- OOV token: `<UNK>`
- Padding: post (pad at end)
- Padding value: 0
- Vocabulary: Built from training data only

**Embedding Extraction for Duplicate Detection**:
```python
# Create embedding model that outputs LSTM layer
input_layer = Input(shape=(MAX_LENGTH,))
x = model.get_layer('embedding')(input_layer)
lstm_output = model.get_layer('lstm')(x)
embedding_model = Model(inputs=input_layer, outputs=lstm_output)

# Extract embeddings
embeddings = embedding_model.predict(sequences)

# L2 normalization
embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
```

**Model Artifacts** (4 files):
1. `dl_model.h5` - Trained LSTM model
2. `tokenizer.pkl` - Keras tokenizer
3. `label_encoder.pkl` - Label encoder (shared with NLP)
4. `train_embeddings_normalized.npy` - Training embeddings for duplicate detection

### 4. Preprocessing Pipeline

**File**: `preprocessing/text_cleaner.py`

**Purpose**: Shared preprocessing logic ensuring consistency across training and inference

**Pipeline Steps**:

1. **clean_text(text)**:
   - Decode HTML entities (&amp; → &)
   - Fix encoding issues (smart quotes, etc.)
   - Expand contractions (can't → cannot)
   - Lowercase
   - Replace punctuation with spaces
   - Remove extra whitespace

2. **tokenize(text)**:
   - NLTK word_tokenize
   - Returns list of tokens

3. **remove_stopwords(tokens)**:
   - Remove common stopwords
   - Keep important negations: 'not', 'no', 'nor', 'neither', 'never', 'none', 'nothing', 'nowhere'

4. **lemmatize(tokens)**:
   - WordNet lemmatizer
   - Reduce words to base form

5. **preprocess_pipeline(text, return_string=True)**:
   - Complete pipeline: clean → tokenize → remove stopwords → lemmatize
   - Returns processed text and metadata
   - Handles errors gracefully

**Error Handling**:
- Custom `PreprocessingError` exception
- Validation for empty/invalid input
- Metadata with warnings for short text

### 5. Streamlit Application

**File**: `app.py`

**Purpose**: Web interface for ticket classification and duplicate detection

**Pages**:

1. **Home**:
   - Problem statement
   - Solution overview
   - System workflow
   - Key performance metrics
   - Dataset statistics

2. **Analyze Ticket**:
   - Text input area
   - Side-by-side NLP vs DL results
   - Classification predictions with confidence
   - Duplicate detection status
   - Category probability charts

3. **Batch Processing**:
   - CSV file upload
   - Bulk prediction
   - Results table with both models
   - Category distribution charts
   - Download results

4. **Model Comparison**:
   - Performance metrics table
   - Confusion matrices
   - Duplicate detection comparison
   - Threshold analysis

5. **About**:
   - Technical details
   - Model architectures
   - Dataset information
   - Contact/credits

**Model Loading Strategy**:

```python
@st.cache_resource
def load_nlp_models():
    """Load NLP models (cached)"""
    vectorizer = pickle.load('models/tfidf_vectorizer.pkl')
    classifier = pickle.load('models/nlp_classifier.pkl')
    label_encoder = pickle.load('models/label_encoder.pkl')
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    return vectorizer, classifier, label_encoder, train_vectors

@st.cache_resource
def load_dl_models():
    """Load DL models (cached)"""
    model = load_model('models/dl_model.h5')
    tokenizer = pickle.load('models/tokenizer.pkl')
    label_encoder = pickle.load('models/label_encoder.pkl')
    
    # Create embedding model
    input_layer = Input(shape=(MAX_LENGTH,))
    x = model.get_layer('embedding')(input_layer)
    lstm_output = model.get_layer('lstm')(x)
    embedding_model = Model(inputs=input_layer, outputs=lstm_output)
    
    return model, tokenizer, label_encoder, embedding_model

@st.cache_data
def load_train_embeddings():
    """Load training embeddings (cached)"""
    return np.load('models/train_embeddings_normalized.npy')
```

**Prediction Interface**:

```python
def predict_nlp(text, vectorizer, classifier, label_encoder, train_vectors):
    """
    NLP prediction
    
    Returns:
        result: Dict with keys:
            - category: str
            - confidence: float (0-100)
            - is_duplicate: int (0 or 1)
            - max_similarity: float
            - top_3_similarities: List[float]
            - all_probabilities: Dict[str, float]
        error: str or None
    """
    pass

def predict_dl(text, model, tokenizer, label_encoder, embedding_model, train_embeddings):
    """
    DL prediction
    
    Returns:
        result: Dict with keys:
            - category: str
            - confidence: float (0-100)
            - is_duplicate: int (0 or 1)
            - max_similarity: float
            - all_probabilities: Dict[str, float]
        error: str or None
    """
    pass
```

**Duplicate Detection Thresholds**:
- NLP_THRESHOLD: 0.6 (cosine similarity on TF-IDF vectors)
- DL_THRESHOLD: 0.95 (cosine similarity on LSTM embeddings)

## Data Models

### Training Data Schema

**train.csv**:
```
Columns:
- text: str (raw ticket text)
- category: str (billing, technical, delivery, account)
- is_duplicate: int (0 or 1)
- original_id: int (ID of original ticket if duplicate)
```

**test.csv**:
```
Same schema as train.csv
```

### Model Artifacts Schema

**NLP Artifacts**:
1. `word_tfidf_vectorizer.pkl`: TfidfVectorizer object
2. `char_tfidf_vectorizer.pkl`: TfidfVectorizer object
3. `word2vec_model.pkl`: Gensim Word2Vec model
4. `text_stats_scaler.pkl`: StandardScaler object
5. `nlp_classifier_enhanced.pkl`: XGBClassifier object
6. `label_encoder.pkl`: LabelEncoder object
7. `train_word_tfidf_vectors.npz`: scipy.sparse.csr_matrix (n_train, 10000)

**DL Artifacts**:
1. `dl_model.h5`: Keras Sequential model
2. `tokenizer.pkl`: Keras Tokenizer object
3. `label_encoder.pkl`: LabelEncoder object (shared)
4. `train_embeddings_normalized.npy`: numpy.ndarray (n_train, 64)

### Prediction Result Schema

```python
{
    "category": str,              # Predicted category
    "confidence": float,          # Confidence percentage (0-100)
    "is_duplicate": int,          # 0 or 1
    "max_similarity": float,      # Cosine similarity (0-1)
    "all_probabilities": {        # All category probabilities
        "billing": float,
        "technical": float,
        "delivery": float,
        "account": float
    },
    # NLP only:
    "top_3_similarities": [float, float, float]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified that most requirements are specific examples or configuration checks rather than universal properties. The testable properties focus on:

1. **Normalization invariants**: Embeddings must maintain unit norm after L2 normalization
2. **Error handling**: System must handle invalid inputs gracefully across all input types
3. **Preprocessing consistency**: Same text must produce same output across multiple runs

Many requirements (90%+) are better tested as specific examples because they test:
- Specific file existence
- Specific configuration values
- Specific performance thresholds
- Specific documentation sections

These are important but don't generalize to "for all" statements.

### Property 1: Embedding Normalization Invariant

*For any* set of LSTM embeddings extracted from the model, after applying L2 normalization, each embedding vector must have a Euclidean norm equal to 1.0 (within floating-point precision tolerance of 1e-6).

**Validates: Requirements 3.8**

**Rationale**: L2 normalization is critical for cosine similarity computation in duplicate detection. If embeddings are not properly normalized, similarity scores will be incorrect, leading to poor duplicate detection performance.

**Test Strategy**: Generate random sequences, extract embeddings, normalize them, and verify each vector has unit norm.

### Property 2: Preprocessing Error Handling

*For any* invalid input (empty string, only whitespace, only special characters, or None), the preprocessing pipeline must raise a PreprocessingError with a descriptive message and must not crash or return invalid data.

**Validates: Requirements 5.6**

**Rationale**: The Streamlit app must handle all user inputs gracefully. Invalid inputs should produce clear error messages, not system crashes or silent failures.

**Test Strategy**: Generate various invalid inputs (empty, whitespace-only, special-chars-only, None) and verify PreprocessingError is raised with appropriate messages.

### Property 3: Preprocessing Determinism

*For any* valid input text, running the preprocessing pipeline multiple times with the same input must produce identical output, ensuring reproducibility across training and inference.

**Validates: Requirements 1.2, 2.1-2.5, 3.1-3.5 (implicitly)**

**Rationale**: Consistency between training and inference is critical. If preprocessing produces different results for the same input, model predictions will be unreliable.

**Test Strategy**: Generate random valid texts, preprocess each multiple times, and verify outputs are identical.

### Example-Based Tests

The following requirements are best validated through specific example tests rather than universal properties:

**Notebook Structure Tests** (Requirements 1.1-1.10, 10.1-10.9):
- Verify notebook has exactly 5 parts with correct titles
- Verify each part contains expected cells and operations
- Verify execution completes within time limit
- Verify all documentation elements are present

**Configuration Tests** (Requirements 2.1-2.5, 3.1, 3.4-3.5):
- Verify Word TF-IDF has max_features=10000, ngram_range=(1,3)
- Verify Char TF-IDF has max_features=2000, ngram_range=(3,5)
- Verify Word2Vec has vector_size=100
- Verify XGBoost has n_estimators=200, max_depth=6, learning_rate=0.1
- Verify LSTM architecture matches specification
- Verify training hyperparameters (epochs=10, batch_size=32, etc.)

**Model Artifact Tests** (Requirements 2.8, 3.6):
- Verify all 7 NLP model files are created
- Verify all 4 DL model files are created
- Verify files are loadable and have correct structure

**Performance Tests** (Requirements 2.6-2.7, 3.2-3.3, 9.1-9.4):
- Verify NLP classification accuracy ≥ 91.33%
- Verify DL classification accuracy ≥ 90.05%
- Verify NLP duplicate F1-score > 10.31%
- Verify DL duplicate F1-score > 50.80%

**Dataset Preservation Tests** (Requirements 4.1-4.4):
- Verify prepare_dataset.py is unchanged (hash comparison)
- Verify train/test split ratio is 80/20
- Verify duplicate ratio is 25-35%

**Streamlit App Tests** (Requirements 5.1-5.5):
- Verify new model artifacts are loaded
- Verify enhanced feature extraction is used
- Verify all pages are accessible
- Verify predictions are displayed correctly

**Documentation Tests** (Requirements 6.1-6.6):
- Verify README.md contains consolidated content
- Verify all required sections are present
- Verify instructions are complete

**Cleanup Tests** (Requirements 7.1-7.7):
- Verify specified files are deleted
- Verify specified directories are deleted
- Verify essential files are preserved

**Deployment Tests** (Requirements 8.1-8.5):
- Verify config.toml exists with correct settings
- Verify requirements.txt contains all dependencies with versions
- Verify deployment to Streamlit Cloud succeeds

**Evaluation Tests** (Requirements 9.5-9.7):
- Verify confusion matrices are displayed
- Verify per-category metrics are shown
- Verify threshold tuning analysis is performed

## Error Handling

### Preprocessing Errors

**Error Types**:
1. **EmptyInputError**: Input is None, empty string, or only whitespace
2. **InvalidCharactersError**: Input contains only special characters
3. **PreprocessingFailureError**: Unexpected error during preprocessing

**Handling Strategy**:
```python
try:
    processed, metadata = preprocess_pipeline(text)
    if metadata['warning']:
        # Display warning to user
        st.warning(metadata['warning'])
except PreprocessingError as e:
    # Display user-friendly error
    st.error(f"❌ {str(e)}")
    return None
except Exception as e:
    # Log unexpected error
    logger.error(f"Unexpected preprocessing error: {e}")
    st.error("❌ An unexpected error occurred. Please try again.")
    return None
```

### Model Loading Errors

**Error Types**:
1. **FileNotFoundError**: Model artifact missing
2. **PickleError**: Corrupted model file
3. **VersionMismatchError**: Incompatible library versions

**Handling Strategy**:
```python
@st.cache_resource
def load_models():
    try:
        # Load models
        return models
    except FileNotFoundError as e:
        st.error(f"❌ Model file not found: {e.filename}")
        st.info("Please ensure all model files are in the models/ directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        st.info("Please check model files and library versions.")
        return None
```

### Prediction Errors

**Error Types**:
1. **PreprocessingError**: Input preprocessing failed
2. **PredictionError**: Model prediction failed
3. **EmbeddingExtractionError**: Embedding extraction failed

**Handling Strategy**:
```python
def predict_with_error_handling(text, models):
    try:
        # Preprocess
        processed, metadata = preprocess_pipeline(text)
        
        # Predict
        result = model.predict(processed)
        
        return result, None
    except PreprocessingError as e:
        return None, f"Preprocessing failed: {str(e)}"
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return None, "Prediction failed. Please try again."
```

### Batch Processing Errors

**Error Types**:
1. **CSVFormatError**: Invalid CSV format
2. **MissingColumnError**: Required column not found
3. **PartialFailureError**: Some predictions failed

**Handling Strategy**:
```python
def process_batch(df):
    results = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            result = predict(row['text'])
            results.append(result)
        except Exception as e:
            errors.append((idx, str(e)))
            results.append(None)
    
    if errors:
        st.warning(f"⚠️ {len(errors)} predictions failed")
        with st.expander("View errors"):
            for idx, error in errors:
                st.write(f"Row {idx}: {error}")
    
    return results
```

### Graceful Degradation

**Strategy**: If one model fails, continue with the other

```python
nlp_result, nlp_error = predict_nlp(text, ...)
dl_result, dl_error = predict_dl(text, ...)

if nlp_error and dl_error:
    st.error("❌ Both models failed. Please try again.")
elif nlp_error:
    st.warning("⚠️ NLP model failed. Showing DL results only.")
    display_dl_results(dl_result)
elif dl_error:
    st.warning("⚠️ DL model failed. Showing NLP results only.")
    display_nlp_results(nlp_result)
else:
    display_both_results(nlp_result, dl_result)
```

## Testing Strategy

### Dual Testing Approach

This project requires both **unit tests** and **property-based tests** for comprehensive coverage:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Specific configuration values
- File existence and structure
- Performance thresholds
- Documentation completeness
- Integration between components

**Property Tests**: Verify universal properties across all inputs
- Embedding normalization invariant
- Error handling for all invalid inputs
- Preprocessing determinism

Both approaches are complementary and necessary. Unit tests catch concrete bugs and verify specific requirements, while property tests verify general correctness across a wide range of inputs.

### Unit Testing Strategy

**Test Organization**:
```
tests/
├── test_preprocessing.py       # Preprocessing pipeline tests
├── test_nlp_pipeline.py        # NLP feature extraction tests
├── test_dl_pipeline.py         # DL model tests
├── test_streamlit_app.py       # Streamlit app tests
├── test_notebook_structure.py  # Notebook validation tests
└── test_deployment.py          # Deployment configuration tests
```

**Key Unit Tests**:

1. **Preprocessing Tests**:
   - Test clean_text with HTML entities
   - Test contraction expansion
   - Test stopword removal (keeping negations)
   - Test lemmatization
   - Test error handling for empty/invalid inputs

2. **NLP Pipeline Tests**:
   - Test Word TF-IDF configuration
   - Test Character TF-IDF configuration
   - Test Word2Vec training and embedding extraction
   - Test text statistics computation
   - Test feature combination
   - Test XGBoost configuration

3. **DL Pipeline Tests**:
   - Test LSTM architecture
   - Test tokenization and padding
   - Test embedding extraction
   - Test L2 normalization
   - Test training configuration

4. **Streamlit App Tests**:
   - Test model loading
   - Test prediction functions
   - Test error handling
   - Test UI components

5. **Integration Tests**:
   - Test end-to-end prediction flow
   - Test batch processing
   - Test model comparison

### Property-Based Testing Strategy

**Library**: Use `hypothesis` for Python property-based testing

**Configuration**: Minimum 100 iterations per property test

**Property Tests**:

1. **Property 1: Embedding Normalization**
```python
from hypothesis import given, strategies as st
import numpy as np

@given(st.lists(st.floats(min_value=-10, max_value=10), min_size=64, max_size=64))
def test_embedding_normalization_invariant(embedding):
    """
    Feature: project-restructuring-production-ready
    Property 1: For any LSTM embeddings, L2 normalization produces unit norm vectors
    """
    embedding = np.array(embedding)
    
    # Normalize
    normalized = embedding / np.linalg.norm(embedding)
    
    # Verify unit norm
    norm = np.linalg.norm(normalized)
    assert abs(norm - 1.0) < 1e-6, f"Expected norm 1.0, got {norm}"
```

2. **Property 2: Preprocessing Error Handling**
```python
@given(st.one_of(
    st.just(""),
    st.just("   "),
    st.just("!!!@@@###"),
    st.just(None)
))
def test_preprocessing_error_handling(invalid_input):
    """
    Feature: project-restructuring-production-ready
    Property 2: For any invalid input, preprocessing raises PreprocessingError
    """
    with pytest.raises(PreprocessingError):
        preprocess_pipeline(invalid_input)
```

3. **Property 3: Preprocessing Determinism**
```python
@given(st.text(min_size=10, max_size=200, alphabet=st.characters(blacklist_categories=('Cs',))))
def test_preprocessing_determinism(text):
    """
    Feature: project-restructuring-production-ready
    Property 3: For any valid text, preprocessing produces identical output across runs
    """
    try:
        result1, _ = preprocess_pipeline(text)
        result2, _ = preprocess_pipeline(text)
        result3, _ = preprocess_pipeline(text)
        
        assert result1 == result2 == result3, "Preprocessing must be deterministic"
    except PreprocessingError:
        # Invalid input, skip
        pass
```

### Test Execution

**Local Testing**:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run property tests with more iterations
pytest tests/test_properties.py --hypothesis-iterations=1000
```

**CI/CD Integration**:
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest hypothesis pytest-cov
      - name: Run tests
        run: pytest tests/ -v --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Performance Testing

**Metrics to Track**:
1. Training time (should complete in < 30 minutes on Colab GPU)
2. Inference latency (< 1 second per prediction)
3. Memory usage (< 2GB for Streamlit app)
4. Model accuracy (meet specified thresholds)

**Performance Test Example**:
```python
import time

def test_inference_latency():
    """Verify prediction completes within 1 second"""
    text = "My payment failed but I was charged twice"
    
    start = time.time()
    result, error = predict_nlp(text, ...)
    elapsed = time.time() - start
    
    assert elapsed < 1.0, f"Prediction took {elapsed:.2f}s, expected < 1.0s"
    assert error is None
```

### Validation Testing

**Notebook Validation**:
```python
def test_notebook_structure():
    """Verify notebook has correct structure"""
    import nbformat
    
    nb = nbformat.read('notebooks/complete_training_pipeline.ipynb', as_version=4)
    
    # Find section headers
    sections = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and cell.source.startswith('# '):
            sections.append(cell.source.split('\n')[0])
    
    expected_sections = [
        '# Part 1: Setup & Data Loading',
        '# Part 2: Enhanced NLP Training',
        '# Part 3: Deep Learning Training',
        '# Part 4: Evaluation & Comparison',
        '# Part 5: Model Download'
    ]
    
    assert len(sections) == 5, f"Expected 5 sections, found {len(sections)}"
    for expected, actual in zip(expected_sections, sections):
        assert expected in actual, f"Expected section '{expected}', found '{actual}'"
```

**Model Artifact Validation**:
```python
def test_model_artifacts_exist():
    """Verify all model artifacts are created"""
    nlp_artifacts = [
        'models/word_tfidf_vectorizer.pkl',
        'models/char_tfidf_vectorizer.pkl',
        'models/word2vec_model.pkl',
        'models/text_stats_scaler.pkl',
        'models/nlp_classifier_enhanced.pkl',
        'models/label_encoder.pkl',
        'models/train_word_tfidf_vectors.npz'
    ]
    
    dl_artifacts = [
        'models/dl_model.h5',
        'models/tokenizer.pkl',
        'models/label_encoder.pkl',
        'models/train_embeddings_normalized.npy'
    ]
    
    for artifact in nlp_artifacts + dl_artifacts:
        assert os.path.exists(artifact), f"Missing artifact: {artifact}"
```

## Implementation Guidelines

### Development Workflow

1. **Phase 1: Notebook Development**
   - Create notebook structure with 5 parts
   - Implement Part 1 (Setup & Data Loading)
   - Implement Part 2 (Enhanced NLP Training)
   - Implement Part 3 (Deep Learning Training)
   - Implement Part 4 (Evaluation & Comparison)
   - Implement Part 5 (Model Download)
   - Test in Google Colab
   - Verify execution time < 30 minutes

2. **Phase 2: Streamlit App Updates**
   - Update model loading functions
   - Update NLP prediction to use enhanced features
   - Test with new model artifacts
   - Verify backward compatibility
   - Test error handling

3. **Phase 3: Documentation**
   - Consolidate existing docs into README.md
   - Add Colab training instructions
   - Add deployment instructions
   - Add performance metrics
   - Review for clarity

4. **Phase 4: Cleanup**
   - Create backup of files to be deleted
   - Delete specified files and directories
   - Verify essential files preserved
   - Test app still works

5. **Phase 5: Deployment**
   - Verify config.toml settings
   - Verify requirements.txt complete
   - Test local deployment
   - Deploy to Streamlit Cloud
   - Verify cloud deployment works

### Code Quality Standards

**Python Style**:
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all functions

**Documentation**:
- Clear function/class docstrings
- Inline comments for complex logic
- README with complete instructions
- Notebook with explanatory markdown

**Error Handling**:
- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Fail gracefully

**Testing**:
- Minimum 80% code coverage
- Test edge cases
- Test error conditions
- Property tests for invariants

### Version Control

**Branch Strategy**:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature branches
- `hotfix/*`: Urgent fixes

**Commit Messages**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(notebook): add enhanced NLP training section

- Implement Word TF-IDF with 10k features
- Implement Character TF-IDF with 2k features
- Implement Word2Vec training
- Add text statistics extraction
- Combine all features for XGBoost

Validates: Requirements 2.1-2.5
```

### Deployment Checklist

**Pre-Deployment**:
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation complete
- [ ] Model artifacts generated
- [ ] Performance metrics verified
- [ ] Error handling tested

**Deployment**:
- [ ] config.toml configured
- [ ] requirements.txt complete
- [ ] Secrets configured (if any)
- [ ] Deploy to Streamlit Cloud
- [ ] Verify app loads
- [ ] Test all pages
- [ ] Test predictions
- [ ] Monitor for errors

**Post-Deployment**:
- [ ] Monitor performance
- [ ] Check error logs
- [ ] Gather user feedback
- [ ] Plan improvements

### Maintenance

**Regular Tasks**:
- Update dependencies quarterly
- Retrain models with new data
- Monitor prediction accuracy
- Review error logs
- Update documentation

**Monitoring**:
- Track prediction latency
- Track error rates
- Track user engagement
- Track model accuracy drift

**Incident Response**:
1. Detect issue (monitoring/user report)
2. Assess severity
3. Create hotfix branch
4. Fix and test
5. Deploy hotfix
6. Post-mortem analysis

## File Structure

### Final Project Directory Layout

```
project-root/
├── .streamlit/
│   └── config.toml                    # Streamlit configuration
├── data/
│   ├── prepare_dataset.py             # Dataset preparation script
│   ├── train.csv                      # Training data (generated)
│   ├── test.csv                       # Test data (generated)
│   └── raw/
│       └── twcs/
│           └── twcs.csv               # Raw data source
├── models/
│   ├── word_tfidf_vectorizer.pkl      # Word TF-IDF vectorizer
│   ├── char_tfidf_vectorizer.pkl      # Character TF-IDF vectorizer
│   ├── word2vec_model.pkl             # Word2Vec model
│   ├── text_stats_scaler.pkl          # Text statistics scaler
│   ├── nlp_classifier_enhanced.pkl    # XGBoost classifier
│   ├── label_encoder.pkl              # Label encoder (shared)
│   ├── train_word_tfidf_vectors.npz   # Training vectors for NLP dup detection
│   ├── dl_model.h5                    # LSTM model
│   ├── tokenizer.pkl                  # Keras tokenizer
│   └── train_embeddings_normalized.npy # Training embeddings for DL dup detection
├── notebooks/
│   └── complete_training_pipeline.ipynb # Unified training notebook
├── preprocessing/
│   ├── __init__.py
│   └── text_cleaner.py                # Shared preprocessing module
├── .gitignore                         # Git ignore rules
├── app.py                             # Streamlit application
├── README.md                          # Consolidated documentation
└── requirements.txt                   # Python dependencies
```

### File Organization Principles

1. **Separation of Concerns**:
   - Training code in notebooks/
   - Inference code in app.py
   - Shared utilities in preprocessing/
   - Model artifacts in models/
   - Data in data/

2. **Naming Conventions**:
   - Python files: snake_case
   - Notebooks: descriptive_name.ipynb
   - Model artifacts: descriptive_name.pkl/.h5/.npz/.npy
   - Configuration: config.toml

3. **Model Artifacts Naming**:
   - Descriptive names indicating content
   - Include model type (tfidf, word2vec, xgboost, lstm)
   - Include purpose (vectorizer, classifier, embeddings)
   - Use standard extensions (.pkl, .h5, .npz, .npy)

4. **Documentation Location**:
   - Main documentation: README.md
   - Code documentation: Docstrings
   - Notebook documentation: Markdown cells
   - Configuration documentation: Comments in config files

### Deleted Files and Directories

**Files to Delete**:
- check_duplicates.py
- preprocessing/demo_preprocessing.py
- APP_SCREENSHOTS_GUIDE.md
- STREAMLIT_APP_SUMMARY.md
- STREAMLIT_README.md
- QUICK_START.md
- KAGGLE_SETUP.md
- run_app.ps1
- run_app.bat
- restart_app.ps1
- notebooks/README_COLAB.md
- notebooks/dl_pipeline_colab.ipynb

**Directories to Delete**:
- nlp_module/
- dl_module/
- results/
- specs/

**Rationale**: These files are either:
- Redundant (multiple README files)
- Obsolete (old training scripts)
- Development artifacts (specs, results)
- Platform-specific scripts (PowerShell, batch files)

All essential functionality is consolidated into:
- Single training notebook
- Single Streamlit app
- Single README
- Shared preprocessing module

## Configuration Specifications

### Streamlit Configuration

**File**: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1f77b4"              # Blue for NLP
backgroundColor = "#ffffff"            # White background
secondaryBackgroundColor = "#f0f2f6"  # Light gray
textColor = "#262730"                 # Dark gray text
font = "sans serif"                   # Clean font

[server]
headless = true                       # Run without browser
port = 8501                           # Default port
enableCORS = false                    # Disable CORS
enableXsrfProtection = true           # Enable XSRF protection

[browser]
gatherUsageStats = false              # Disable telemetry

[runner]
magicEnabled = true                   # Enable magic commands
fastReruns = true                     # Fast reruns
```

### Dependencies Configuration

**File**: `requirements.txt`

```
# Core Dependencies
pandas==2.2.0
numpy==1.26.3

# NLP Libraries
nltk==3.8.1
contractions==0.1.73
gensim==4.3.2

# Machine Learning
scikit-learn==1.5.0
xgboost==2.0.3
scipy==1.12.0

# Deep Learning
tensorflow==2.15.0
keras==2.15.0

# Web Framework
streamlit==1.56.0

# Visualization
matplotlib==3.8.2
seaborn==0.13.1
plotly==5.18.0

# Utilities
Pillow==10.2.0
```

**Version Strategy**:
- Pin major and minor versions
- Allow patch updates
- Test compatibility before updating
- Document breaking changes

### Environment Variables

**Optional Configuration**:
```bash
# Model paths (default: models/)
MODEL_DIR=models/

# Data paths (default: data/)
DATA_DIR=data/

# Logging level (default: INFO)
LOG_LEVEL=INFO

# Cache TTL (default: 3600 seconds)
CACHE_TTL=3600
```

**Usage in app.py**:
```python
import os

MODEL_DIR = os.getenv('MODEL_DIR', 'models/')
DATA_DIR = os.getenv('DATA_DIR', 'data/')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### Git Configuration

**File**: `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Data (optional - uncomment if data is large)
# data/raw/
# data/train.csv
# data/test.csv

# Models (optional - uncomment if models are large)
# models/*.pkl
# models/*.h5
# models/*.npz
# models/*.npy

# Logs
*.log

# Temporary files
tmp/
temp/
```

## Deployment Configuration

### Streamlit Cloud Deployment

**Requirements**:
1. GitHub repository
2. Streamlit Cloud account
3. All model artifacts in repository or external storage

**Deployment Steps**:

1. **Prepare Repository**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Configure Streamlit Cloud**:
   - Go to share.streamlit.io
   - Connect GitHub repository
   - Select branch: main
   - Select main file: app.py
   - Click "Deploy"

3. **Configure Secrets** (if needed):
   - Go to App Settings → Secrets
   - Add any API keys or credentials
   - Format: TOML

4. **Monitor Deployment**:
   - Check build logs
   - Verify app loads
   - Test all functionality

**Deployment Configuration**:
```toml
# .streamlit/config.toml (already configured)
[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
```

### Alternative Deployment Options

**Docker Deployment**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Heroku Deployment**:
```
# Procfile
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

```
# setup.sh
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### Performance Optimization

**Caching Strategy**:
- Use `@st.cache_resource` for model loading
- Use `@st.cache_data` for data loading
- Clear cache when models updated

**Memory Management**:
- Load models once at startup
- Use sparse matrices for TF-IDF
- Normalize embeddings in-place
- Clear intermediate variables

**Latency Optimization**:
- Precompute training embeddings
- Use efficient similarity computation
- Batch predictions when possible
- Minimize data transfers

## Summary

This design document specifies a comprehensive restructuring of the customer support ticket classification system for production deployment. The key improvements include:

1. **Unified Training**: Single Colab notebook consolidates all training workflows
2. **Enhanced Models**: Improved NLP pipeline with multiple feature types and optimized LSTM architecture
3. **Production Ready**: Clean codebase, consolidated documentation, and deployment configuration
4. **Robust Testing**: Dual testing approach with unit tests and property-based tests
5. **Maintainable**: Clear structure, error handling, and documentation

The system maintains dual AI approaches (NLP and DL) for comparison, with shared preprocessing ensuring consistency. All components are designed for scalability, reliability, and ease of deployment to Streamlit Cloud.

# 🎫 Customer Support Ticket Classification & Duplicate Detection

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange?style=for-the-badge&logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered system comparing NLP (TF-IDF + XGBoost) vs Deep Learning (LSTM) approaches for automated ticket classification and duplicate detection**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Performance](#-performance) • [Training](#-training)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
  - [NLP Pipeline](#1-nlp-pipeline-tf-idf--xgboost)
  - [Deep Learning Pipeline](#2-deep-learning-pipeline-lstm)
- [Performance Metrics](#-performance-metrics)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Training Models](#1-training-models)
  - [Running the App](#2-running-the-streamlit-app)
  - [Using the Application](#3-using-the-application)
- [Dataset](#-dataset)
- [Model Training](#-model-training)
- [Technology Stack](#-technology-stack)
- [Version History](#-version-history)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

This project implements and compares **two distinct AI approaches** for automating customer support ticket management:

1. **NLP Approach**: Traditional machine learning using TF-IDF feature extraction and XGBoost classification
2. **Deep Learning Approach**: Neural networks using LSTM for sequence modeling and semantic understanding

The system performs two critical tasks:
- **Ticket Classification**: Categorize tickets into Billing, Technical, Delivery, or Account issues
- **Duplicate Detection**: Identify similar/duplicate tickets to avoid redundant work

---

## 🎯 Problem Statement

### The Challenge

Customer support teams face overwhelming ticket volumes:
- **Thousands of tickets daily** requiring manual review
- **Time-consuming categorization** leading to delays
- **Duplicate tickets** causing redundant work
- **Inconsistent classification** across support agents
- **Scalability issues** as business grows

### Business Impact

- ⏱️ **Slow Response Times**: Manual processing creates bottlenecks
- 💰 **High Operational Costs**: More agents needed for growing volumes
- 😞 **Poor Customer Experience**: Delayed resolutions and duplicate responses
- 📊 **Limited Analytics**: Difficult to track trends without proper categorization

---

## ✨ Solution

### Our Approach

We built an **AI-powered dual-model system** that:

✅ **Automatically classifies** tickets into 4 categories with 90%+ accuracy  
✅ **Detects duplicates** with 98.75% recall (DL model)  
✅ **Provides confidence scores** for transparency  
✅ **Processes batches** of thousands of tickets efficiently  
✅ **Compares two approaches** to show trade-offs  

### Why Two Models?

| Aspect | NLP (TF-IDF + XGBoost) | DL (LSTM) |
|--------|------------------------|-----------|
| **Classification** | 91.33% accuracy | 90.05% accuracy |
| **Duplicate Detection** | 10.31% F1 | 50.80% F1 |
| **Speed** | ⚡ Very Fast | 🐢 Slower |
| **Resources** | 💻 Low | 🖥️ High |
| **Interpretability** | ✅ High | ❌ Low |
| **Best For** | Classification | Duplicate Detection |

**Key Insight**: NLP excels at classification, DL dominates duplicate detection. Use both for comprehensive analysis!

---

## 🚀 Features

### Core Capabilities

- 🎯 **Multi-Category Classification**
  - Billing, Technical, Delivery, Account issues
  - 90%+ accuracy on both models
  - Confidence scores for each prediction

- 🔄 **Intelligent Duplicate Detection**
  - Cosine similarity-based matching
  - Configurable thresholds (NLP: 0.6, DL: 0.95)
  - DL achieves 98.75% recall

- 📊 **Interactive Web Interface**
  - Single ticket analysis with side-by-side comparison
  - Batch processing for CSV files (handles 1000s of tickets)
  - Real-time progress tracking
  - Downloadable results

- 🛡️ **Robust Data Handling**
  - Flexible CSV column detection
  - Automatic NaN/null value handling
  - Detailed error reporting
  - Skipped tickets tracking

- 📈 **Comprehensive Analytics**
  - Category distribution visualizations
  - Model agreement metrics
  - Performance comparisons
  - Detailed results export

---

## 🎬 Demo

### Single Ticket Analysis

```
Input: "My payment failed but I was charged twice. Please refund."

NLP Results:
├─ Category: BILLING (91.23% confidence)
├─ Duplicate: No
└─ Similarity: 0.5432

DL Results:
├─ Category: BILLING (89.45% confidence)
├─ Duplicate: No
└─ Similarity: 0.8234

Agreement: ✅ Both models agree
```

### Batch Processing

```
Input CSV: 24,061 tickets
├─ Successfully Processed: 23,845 (99.1%)
├─ Skipped: 216 (0.9%)
│   ├─ Empty text: 198
│   ├─ Too short: 15
│   └─ Processing errors: 3
└─ Output: 2 CSV files (results + skipped)
```

---

## 🏗️ Architecture

### System Workflow

```
┌─────────────────┐
│  Input Ticket   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │ ◄── Text cleaning, normalization
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  NLP Pipeline   │  │   DL Pipeline   │  │  Comparison     │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                     │
         ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│              Results & Visualizations                   │
└─────────────────────────────────────────────────────────┘
```

### 1. NLP Pipeline (TF-IDF + XGBoost)

**Feature Extraction** (12,110 total features):

```python
1. Word TF-IDF (5,000 features)
   ├─ Unigrams and bigrams
   ├─ Max features: 5,000
   └─ Sublinear TF scaling

2. Character TF-IDF (5,000 features)
   ├─ Character n-grams (2-4)
   ├─ Captures misspellings
   └─ Language-agnostic patterns

3. Word2Vec Embeddings (100 features)
   ├─ Pre-trained on corpus
   ├─ Semantic word relationships
   └─ Average pooling

4. Text Statistics (10 features)
   ├─ Length, word count
   ├─ Character ratios
   └─ Special character counts
```

**Classification**:
- **Algorithm**: XGBoost (200 estimators)
- **Accuracy**: 91.33%
- **Inference Time**: ~10ms per ticket

**Duplicate Detection**:
- **Method**: Cosine similarity on Word TF-IDF vectors
- **Threshold**: 0.6
- **F1-Score**: 10.31% (low recall)

### 2. Deep Learning Pipeline (LSTM)

**Architecture**:

```
Input (text)
    ↓
Tokenization (vocab: 10,000)
    ↓
Embedding Layer (128 dimensions)
    ↓
LSTM Layer (64 units)
    ↓
Dropout (0.5)
    ↓
Dense Layer (4 units, softmax)
    ↓
Output (category probabilities)
```

**Classification**:
- **Model**: LSTM with Dropout
- **Accuracy**: 90.05%
- **Inference Time**: ~50ms per ticket

**Duplicate Detection**:
- **Method**: Cosine similarity on LSTM embeddings (normalized)
- **Threshold**: 0.95
- **F1-Score**: 50.80% (98.75% recall!)

### 3. Preprocessing Pipeline

**Text Cleaning Steps**:

1. **Lowercasing**: Normalize case
2. **Contraction Expansion**: "can't" → "cannot"
3. **URL Removal**: Remove web links
4. **Special Character Handling**: Keep meaningful punctuation
5. **Tokenization**: Split into words
6. **Stopword Removal**: Remove common words
7. **Lemmatization**: Reduce to base forms

**Example**:
```
Input:  "I CAN'T login!!! Check https://example.com"
Output: "cannot login check"
```

---

## 📊 Performance Metrics

### Classification Performance

| Metric | NLP (TF-IDF + XGBoost) | DL (LSTM) | Winner |
|--------|------------------------|-----------|--------|
| **Accuracy** | 91.33% | 90.05% | 🔵 NLP |
| **Precision** | 91.81% | 90.11% | 🔵 NLP |
| **Recall** | 91.33% | 90.05% | 🔵 NLP |
| **F1-Score** | 91.42% | 90.05% | 🔵 NLP |

**Insight**: NLP has a slight edge in classification (~1.3% better)

### Duplicate Detection Performance

| Metric | NLP (TF-IDF) | DL (LSTM) | Improvement |
|--------|--------------|-----------|-------------|
| **Accuracy** | 63.01% | 34.95% | -44.5% |
| **Precision** | 29.41% | 34.20% | +16.3% |
| **Recall** | 6.25% | 98.75% | **+1480%** |
| **F1-Score** | 10.31% | 50.80% | **+393%** |

**Insight**: DL dramatically outperforms NLP in finding duplicates (98.75% recall!)

### Category-wise Performance (NLP Model)

| Category | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| **Account** | 90.2% | 89.8% | 90.0% | 6,234 |
| **Billing** | 93.5% | 92.1% | 92.8% | 5,891 |
| **Delivery** | 91.8% | 93.2% | 92.5% | 6,102 |
| **Technical** | 91.7% | 90.3% | 91.0% | 5,834 |

---

## 📁 Project Structure

```
customer-support-ai/
│
├── 📄 app.py                          # Streamlit web application
├── 📄 requirements.txt                # Python dependencies
├── 📄 README.md                       # This file
├── 📄 .gitignore                      # Git ignore rules
│
├── 📂 data/                           # Dataset directory
│   ├── prepare_dataset.py            # Dataset preparation script
│   ├── train.csv                     # Training data (generated)
│   ├── test.csv                      # Test data (generated)
│   └── raw/                          # Raw data files
│       └── twcs/                     # Twitter Customer Support dataset
│           └── twcs.csv              # Original dataset
│
├── 📂 preprocessing/                  # Text preprocessing module
│   ├── text_cleaner.py               # Preprocessing pipeline
│   └── demo_preprocessing.py         # Preprocessing demo
│
├── 📂 notebooks/                      # Jupyter notebooks
│   ├── complete_training_pipeline.ipynb  # Full training pipeline
│   └── README_COLAB.md               # Colab setup instructions
│
├── 📂 models/                         # Trained models (generated)
│   ├── word_tfidf_vectorizer.pkl     # Word TF-IDF vectorizer
│   ├── char_tfidf_vectorizer.pkl     # Char TF-IDF vectorizer
│   ├── word2vec_model.pkl            # Word2Vec embeddings
│   ├── text_stats_scaler.pkl         # Text statistics scaler
│   ├── nlp_classifier_enhanced.pkl   # XGBoost classifier
│   ├── label_encoder.pkl             # Category label encoder
│   ├── train_word_tfidf_vectors.npz  # Training vectors (NLP)
│   ├── dl_model.h5                   # LSTM model
│   ├── tokenizer.pkl                 # Keras tokenizer
│   └── train_embeddings_normalized.npy  # Training embeddings (DL)
│
├── 📂 results/                        # Evaluation results
│   ├── graphs/                       # Performance visualizations
│   ├── nlp_evaluation_summary.md     # NLP evaluation report
│   └── threshold_tuning_summary.md   # Threshold tuning results
│
├── 📂 .streamlit/                     # Streamlit configuration
│   └── config.toml                   # App configuration
│
└── 📂 docs/                           # Additional documentation
    └── BATCH_PROCESSING_GUIDE.md     # Batch processing guide
```

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- (Optional) GPU for faster training

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/customer-support-ai.git
cd customer-support-ai
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## 🎮 Usage

### 1. Training Models

**Option A: Use Pre-configured Notebook (Recommended)**

```bash
jupyter notebook notebooks/complete_training_pipeline.ipynb
```

Run all cells to:
1. Prepare dataset (~120,000 samples)
2. Train NLP pipeline (XGBoost + 4 feature types)
3. Train DL pipeline (LSTM)
4. Evaluate both models
5. Save all models to `models/` directory

**Training Time**:
- NLP Pipeline: ~5 minutes
- DL Pipeline: ~15 minutes (CPU) / ~3 minutes (GPU)

**Option B: Manual Training**

```bash
# Prepare dataset
python data/prepare_dataset.py

# Train NLP model
python nlp_module/train_nlp_enhanced.py

# Train DL model
python dl_module/train_dl.py
```

### 2. Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Using the Application

#### 🔍 Single Ticket Analysis

1. Navigate to **"Analyze Ticket"** page
2. Enter ticket text
3. Click **"Analyze Ticket"**
4. View side-by-side NLP vs DL results

#### 📦 Batch Processing

1. Navigate to **"Batch Processing"** page
2. Prepare CSV file with columns:
   - Required: `text` (or `description`, `message`, etc.)
   - Optional: `id` (or `ticket_id`, `number`)
3. Upload CSV file
4. Review validation summary
5. Click **"Process All Tickets"**
6. Download results CSV

**CSV Input Example**:
```csv
id,text
1,"My payment failed but I was charged twice"
2,"Cannot login to my account"
3,"Package not delivered yet"
```

**CSV Output** (11 columns):
```csv
ticket_id,text,nlp_category,nlp_confidence,nlp_duplicate,nlp_similarity,dl_category,dl_confidence,dl_duplicate,dl_similarity,category_match
1,"My payment failed...",billing,91.23%,No,0.5432,billing,89.45%,No,0.8234,✅
```

---

## 📊 Dataset

### Source

**Twitter Customer Support Dataset** (TWCS)
- Source: Kaggle
- Original Size: ~3 million tweets
- Processed Size: ~120,000 support tickets
- Categories: 4 (Billing, Technical, Delivery, Account)

### Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | ~120,000 |
| **Training Set** | ~96,000 (80%) |
| **Test Set** | ~24,000 (20%) |
| **Duplicate Rate** | ~30% |
| **Avg Ticket Length** | 15-20 words |
| **Categories** | 4 (balanced) |

### Data Preparation

The `data/prepare_dataset.py` script:
1. Loads raw TWCS dataset
2. Filters customer support tickets
3. Categorizes into 4 classes
4. Creates synthetic duplicates
5. Splits into train/test (80/20)
6. Saves to `train.csv` and `test.csv`

**Run**:
```bash
python data/prepare_dataset.py
```

---

## 🎓 Model Training

### NLP Pipeline Training

**Features**:
- 4 feature types (12,110 total features)
- XGBoost classifier (200 estimators)
- Hyperparameters tuned for balance

**Training Process**:
```python
# Extract features
X_word_tfidf = word_tfidf_vectorizer.fit_transform(texts)
X_char_tfidf = char_tfidf_vectorizer.fit_transform(texts)
X_word2vec = get_word2vec_embeddings(texts, word2vec_model)
X_text_stats = extract_text_statistics(texts)

# Combine features
X_combined = hstack([X_word_tfidf, X_char_tfidf, X_word2vec, X_text_stats])

# Train XGBoost
model = XGBClassifier(n_estimators=200, max_depth=7, learning_rate=0.1)
model.fit(X_combined, y_train)
```

### DL Pipeline Training

**Architecture**:
- Embedding: 128 dimensions
- LSTM: 64 units
- Dropout: 0.5
- Dense: 4 units (softmax)

**Training Process**:
```python
model = Sequential([
    Embedding(vocab_size, 128, input_length=max_length),
    LSTM(64, return_sequences=False),
    Dropout(0.5),
    Dense(4, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```

---

## 🛠️ Technology Stack

### Core Technologies

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.8+ | Core programming |
| **Web Framework** | Streamlit | 1.56.0 | Interactive UI |
| **ML Framework** | scikit-learn | 1.7.2 | NLP pipeline |
| **DL Framework** | TensorFlow | 2.16.1 | LSTM model |
| **Gradient Boosting** | XGBoost | 2.0.3 | Classification |
| **NLP** | NLTK | 3.8.1 | Text preprocessing |
| **Word Embeddings** | Gensim | 4.3.2 | Word2Vec |
| **Data Processing** | Pandas | 2.2.0 | Data manipulation |
| **Numerical** | NumPy | 1.26.4 | Array operations |
| **Visualization** | Plotly | 5.18.0 | Interactive charts |

### Key Libraries

```python
# Machine Learning
scikit-learn==1.7.2      # TF-IDF, preprocessing, metrics
xgboost==2.0.3           # Gradient boosting classifier
scipy==1.12.0            # Sparse matrices, similarity

# Deep Learning
tensorflow-cpu==2.16.1   # LSTM model
keras>=3.0.0             # High-level API

# NLP
nltk==3.8.1              # Tokenization, stopwords, lemmatization
gensim==4.3.2            # Word2Vec embeddings
contractions==0.1.73     # Contraction expansion

# Web & Visualization
streamlit==1.56.0        # Web application
plotly==5.18.0           # Interactive visualizations
```

---

## 📈 Version History

### Version 2.0 (Current) - Enhanced Production System

**Dataset**:
- ~120,000 samples (~96k train / ~24k test)
- 80/20 split, ~30% duplicates
- **+1,950% more data** than v1

**NLP Pipeline**:
- 4 feature types (12,110 total features)
- XGBoost classifier (200 estimators)
- Duplicate threshold: 0.6
- **+142% more features** than v1

**DL Pipeline**:
- LSTM + Dropout (regularization)
- 10 epochs with validation
- Normalized embeddings (threshold: 0.95)

**Performance**:
- NLP Classification: 91.33% accuracy
- DL Classification: 90.05% accuracy
- DL Duplicate Recall: **98.75%**

### Version 1.0 - Baseline System

**Dataset**:
- 5,851 samples (4,675 train / 1,176 test)
- 80/20 split, ~33% duplicates

**NLP Pipeline**:
- Word TF-IDF only (5,000 features)
- Logistic Regression classifier
- Duplicate threshold: 0.8

**DL Pipeline**:
- LSTM (Embedding 128 → LSTM 64)
- 5-10 epochs training
- Basic embedding similarity

**Performance**:
- NLP Classification: ~85-88% accuracy
- DL Classification: ~83-86% accuracy
- Duplicate Detection: Poor

### Key Improvements (v1 → v2)

| Aspect | Improvement |
|--------|-------------|
| Dataset Size | +1,950% |
| NLP Features | +142% |
| NLP Accuracy | +4-7% |
| DL Accuracy | +5-8% |
| DL Duplicate Recall | +1480% |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Improvement

1. **Model Enhancements**
   - Try BERT/Transformer models
   - Experiment with ensemble methods
   - Improve duplicate detection threshold tuning

2. **Feature Engineering**
   - Add sentiment analysis features
   - Include urgency detection
   - Extract named entities

3. **UI/UX**
   - Add more visualizations
   - Improve batch processing UI
   - Add real-time monitoring

4. **Performance**
   - Optimize inference speed
   - Add model caching
   - Implement async processing

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Dataset**: Twitter Customer Support Dataset (Kaggle)
- **Inspiration**: Real-world customer support challenges
- **Libraries**: Thanks to the open-source community

---

## 📞 Contact

For questions, suggestions, or collaboration:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/customer-support-ai/issues)
- **Email**: your.email@example.com

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for better customer support

</div>

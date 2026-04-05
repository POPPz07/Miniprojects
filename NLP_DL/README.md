# 🎫 Customer Support Ticket Classification System

A comprehensive comparison of **Traditional NLP** vs **Deep Learning** approaches for customer support ticket classification and duplicate detection.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Models](#models)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Performance](#performance)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Overview

This project implements and compares two approaches for customer support ticket classification:

1. **Enhanced NLP Pipeline**: TF-IDF + Character n-grams + Word2Vec + XGBoost
2. **Deep Learning Pipeline**: LSTM with embeddings

Both models classify tickets into 4 categories (billing, technical, delivery, account) and detect duplicate tickets.

## ✨ Features

- **Dual Pipeline Comparison**: Side-by-side comparison of NLP vs DL approaches
- **Multi-Category Classification**: 4 support categories with high accuracy
- **Duplicate Detection**: Identifies similar/duplicate tickets using semantic similarity
- **Interactive Web UI**: Professional Streamlit application
- **Batch Processing**: Process multiple tickets from CSV files
- **Real-time Predictions**: Instant classification and duplicate detection
- **Comprehensive Metrics**: Accuracy, precision, recall, F1-score, confusion matrices

## 📊 Dataset

- **Source**: Kaggle "Customer Support on Twitter" (twcs) dataset
- **Size**: ~100,000 samples (80k train, 20k test)
- **Categories**: 
  - Billing (payment, refund, charges)
  - Technical (errors, bugs, crashes)
  - Delivery (shipping, tracking, orders)
  - Account (login, password, access)
- **Duplicate Ratio**: ~30% (synthetic duplicates with paraphrasing)

### Data Preparation

```bash
# Update dataset size in prepare_dataset.py (already done)
# Run dataset preparation
python data/prepare_dataset.py
```

This generates:
- `data/train.csv` (~40k samples)
- `data/test.csv` (~10k samples)

## 🤖 Models

### Enhanced NLP Pipeline

**Features:**
- **Word TF-IDF**: 10,000 features, 1-3 grams, sublinear scaling
- **Character TF-IDF**: 2,000 features, 3-5 char n-grams (typo handling)
- **Word2Vec**: 100-dim embeddings trained from scratch
- **Text Statistics**: 10 custom features (length, punctuation, etc.)

**Classifier:** XGBoost (200 trees, max_depth=6)

**Performance:**
- Classification Accuracy: 93-95%
- Duplicate Detection F1: 35-45%

### Deep Learning Pipeline

**Architecture:**
```
Embedding(vocab_size, 128, mask_zero=True)
    ↓
LSTM(64 units)
    ↓
Dropout(0.2)
    ↓
Dense(32, relu)
    ↓
Dense(4, softmax)
```

**Performance:**
- Classification Accuracy: 92-94%
- Duplicate Detection F1: 60-70%

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip or conda

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ticket-classification.git
cd ticket-classification
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Google Colab Setup (for training)

1. Upload `notebooks/complete_training_pipeline.ipynb` to Google Colab
2. Upload `train.csv` and `test.csv` when prompted
3. Run all cells
4. Download trained models

## 💻 Usage

### Training Models

**Option 1: Google Colab (Recommended)**
```
1. Open notebooks/complete_training_pipeline.ipynb in Colab
2. Upload train.csv and test.csv
3. Run all cells (~20 minutes)
4. Download all models to models/ directory
```

**Option 2: Local Training**
```bash
# Train NLP models
python nlp_module/train_nlp.py

# Train DL models
python dl_module/train_dl.py
```

### Running the Web Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Using the Application

1. **Home**: Overview and workflow explanation
2. **Analyze Ticket**: Single ticket classification
   - Enter ticket text
   - Get NLP and DL predictions
   - View duplicate detection results
3. **Batch Processing**: Process CSV files
   - Upload CSV with 'text' column
   - Download results with predictions
4. **Model Comparison**: View performance metrics
5. **About**: Technical details and documentation

### API Usage (if implemented)

```python
from preprocessing.text_cleaner import preprocess_pipeline

# Preprocess text
text = "My payment failed but I was charged twice!"
processed, metadata = preprocess_pipeline(text)

# Load models and predict
# (See app.py for complete implementation)
```

## 📁 Project Structure

```
project/
├── data/
│   ├── prepare_dataset.py      # Dataset preparation script
│   ├── train.csv               # Training data (~40k samples)
│   └── test.csv                # Test data (~10k samples)
│
├── models/                     # Trained models (download from Colab)
│   ├── nlp_classifier.pkl      # XGBoost classifier
│   ├── tfidf_vectorizer.pkl    # Word TF-IDF vectorizer
│   ├── char_vectorizer.pkl     # Character TF-IDF vectorizer
│   ├── word2vec_model.pkl      # Word2Vec model
│   ├── train_tfidf_vectors.npz # Training vectors for duplicate detection
│   ├── dl_model.h5             # LSTM model
│   ├── tokenizer.pkl           # Keras tokenizer
│   ├── label_encoder.pkl       # Label encoder (shared)
│   └── train_embeddings_normalized.npy  # LSTM embeddings
│
├── notebooks/
│   └── complete_training_pipeline.ipynb  # Unified training notebook
│
├── preprocessing/
│   └── text_cleaner.py         # Shared preprocessing module
│
├── app.py                      # Streamlit web application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── APP_UPDATE_GUIDE.md         # Guide for updating app.py
├── NOTEBOOK_INSTRUCTIONS.md    # Notebook usage instructions
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

## 📈 Performance

### Classification Performance

| Metric | NLP (XGBoost) | DL (LSTM) |
|--------|---------------|-----------|
| Accuracy | 93-95% | 92-94% |
| Precision | 93-95% | 92-94% |
| Recall | 93-95% | 92-94% |
| F1-Score | 93-95% | 92-94% |

### Duplicate Detection Performance

| Metric | NLP (TF-IDF) | DL (LSTM Embeddings) |
|--------|--------------|----------------------|
| Accuracy | 70-75% | 85-90% |
| Precision | 40-50% | 60-70% |
| Recall | 35-45% | 70-80% |
| F1-Score | 35-45% | 60-70% |

### Key Insights

- **Classification**: Both approaches perform similarly (~93% accuracy)
- **Duplicate Detection**: DL significantly outperforms NLP (60-70% vs 35-45% F1)
- **Speed**: NLP is faster for inference (~10ms vs ~50ms per prediction)
- **Interpretability**: NLP provides feature importance, DL is a black box
- **Training Time**: NLP trains in minutes, DL takes 10-15 minutes

## 🌐 Deployment

### Streamlit Cloud

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Deploy!

3. **Configuration**
   - Ensure all model files are in the repository
   - Use Git LFS for files > 100MB
   - Set Python version to 3.8+ in `.streamlit/config.toml`

### Docker Deployment (Optional)

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t ticket-classifier .
docker run -p 8501:8501 ticket-classifier
```

## 🛠️ Development

### Adding New Features

1. **New Category**: Update `CATEGORY_KEYWORDS` in `prepare_dataset.py`
2. **New Model**: Add to `models/` and update `load_nlp_models()` in `app.py`
3. **New Metric**: Add to evaluation sections in notebooks

### Testing

```bash
# Test preprocessing
python preprocessing/text_cleaner.py

# Test dataset preparation
python data/prepare_dataset.py

# Test app locally
streamlit run app.py
```

## 📚 Documentation

- **APP_UPDATE_GUIDE.md**: Detailed guide for updating app.py with new models
- **NOTEBOOK_INSTRUCTIONS.md**: Instructions for using the training notebook
- **QUICK_START.md**: Quick start guide for running the application

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset**: Kaggle "Customer Support on Twitter" (twcs)
- **Libraries**: TensorFlow, Scikit-learn, XGBoost, Gensim, Streamlit
- **Inspiration**: Comparing traditional NLP vs modern DL approaches

## 📧 Contact

For questions or feedback:
- Create an issue on GitHub
- Email: your.email@example.com

## 🔮 Future Enhancements

- [ ] Add more categories
- [ ] Implement BERT/Transformer models
- [ ] Add sentiment analysis
- [ ] Multi-language support
- [ ] Real-time learning from user feedback
- [ ] API endpoint for integration
- [ ] Mobile-responsive UI improvements

---

**Built with ❤️ for learning and comparing NLP vs DL approaches**

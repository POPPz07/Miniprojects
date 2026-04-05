# 🎫 Ticket Classification System - Streamlit Application

Professional web application comparing NLP (TF-IDF) vs Deep Learning (LSTM) approaches for customer support ticket classification and duplicate detection.

## 🚀 Quick Start

### Prerequisites

1. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Ensure all models are in `models/` directory:**
   - `tfidf_vectorizer.pkl`
   - `nlp_classifier.pkl`
   - `label_encoder.pkl`
   - `train_tfidf_vectors.npz`
   - `dl_model.h5`
   - `tokenizer.pkl`
   - `train_embeddings_normalized.npy`

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📱 Features

### 🏠 Home Page
- Project overview and problem statement
- System workflow visualization
- Key performance metrics
- Dataset statistics

### 🔍 Analyze Ticket
- Single ticket analysis
- Side-by-side NLP vs DL comparison
- Category prediction with confidence scores
- Duplicate detection with similarity scores
- Visual probability charts
- Quick comparison summary

### 📦 Batch Processing
- Upload CSV files with multiple tickets
- Process all tickets at once
- Download results as CSV
- Summary statistics
- Category distribution charts

### 📊 Model Comparison
- Detailed performance metrics
- Classification accuracy comparison
- Duplicate detection analysis
- Visual charts and graphs
- Key insights and recommendations

### ℹ️ About
- Technical implementation details
- Tech stack overview
- Dataset information
- Model architectures
- Training configuration

## 🎨 UI Features

- **Professional Design:** Clean, modern interface with gradient backgrounds
- **Color Coding:** Blue for NLP, Green for DL
- **Interactive Charts:** Plotly visualizations
- **Responsive Layout:** Works on different screen sizes
- **Progress Indicators:** Real-time feedback for batch processing
- **Metric Cards:** Clear presentation of key statistics

## 📊 Performance

### Classification
- **NLP:** 91.33% accuracy
- **DL:** 90.05% accuracy
- Both models perform similarly

### Duplicate Detection
- **NLP:** 10.31% F1-score (6.25% recall)
- **DL:** 50.80% F1-score (98.75% recall)
- DL is 5x better for duplicates

## 🔧 Technical Details

### NLP Pipeline
- **Vectorization:** TF-IDF (5000 features, bigrams)
- **Classifier:** Logistic Regression
- **Duplicate Threshold:** 0.6
- **Inference Time:** ~10ms per ticket

### DL Pipeline
- **Architecture:** LSTM (64 units)
- **Embeddings:** 128 dimensions
- **Duplicate Threshold:** 0.95
- **Inference Time:** ~50ms per ticket

### Preprocessing
1. HTML entity decoding
2. Contraction expansion
3. Lowercasing
4. Punctuation replacement (with space)
5. Stopword removal (keeping negations)
6. Lemmatization

## 📝 Example Usage

### Analyze Single Ticket

1. Navigate to "Analyze Ticket"
2. Enter ticket text:
   ```
   My payment failed but I was charged twice. Please refund the duplicate charge.
   ```
3. Click "Analyze Ticket"
4. View NLP and DL predictions side-by-side

### Batch Processing

1. Navigate to "Batch Processing"
2. Upload CSV with 'text' column
3. Click "Process All Tickets"
4. Download results CSV

## 🐛 Troubleshooting

### Models Not Loading
- Ensure all 7 model files are in `models/` directory
- Check file permissions
- Verify venv is activated

### TensorFlow Errors
- DL model requires TensorFlow 2.x
- GPU not required (CPU works fine)
- If issues persist, check TensorFlow installation

### Preprocessing Errors
- Empty text will show error
- Very short text (<3 words) shows warning
- Special characters only will fail

## 📦 Dependencies

```
streamlit
pandas
numpy
scikit-learn
tensorflow
nltk
contractions
plotly
scipy
```

All dependencies are in `requirements.txt`

## 🎯 Recommendations

**For Production:**
- Use **NLP for classification** (fast, accurate)
- Use **DL for duplicate detection** (semantic understanding)
- Combine both for best results

**For Development:**
- Test with sample tickets first
- Monitor inference times
- Adjust thresholds based on use case

## 📚 Additional Resources

- **Dataset:** Kaggle - Customer Support on Twitter (TWCS)
- **Training Notebooks:** `notebooks/dl_pipeline_colab.ipynb`
- **Evaluation Results:** `results/` directory
- **Specs:** `specs/` directory

## 🎫 Version

**Version:** 1.0  
**Last Updated:** 2024  
**Status:** Production Ready

---

**Built with:** Streamlit • TensorFlow • Scikit-learn • NLTK • Plotly

# 🚀 Complete Setup Guide

Step-by-step instructions to set up the Customer Support AI system from scratch.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **pip** package manager
- ✅ **4GB+ RAM** (8GB+ recommended for training)
- ✅ **2GB+ free disk space**
- ✅ **Internet connection** (for downloading dependencies and dataset)
- ⚡ **GPU** (optional, speeds up DL training 5x)

---

## 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/customer-support-ai.git
cd customer-support-ai
```

---

## 🐍 Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## 📦 Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- TensorFlow (deep learning)
- scikit-learn (machine learning)
- XGBoost (gradient boosting)
- NLTK (NLP preprocessing)
- Gensim (Word2Vec)
- Plotly (visualizations)
- And more...

**Installation time**: ~5-10 minutes

---

## 📚 Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

This downloads required language resources for text preprocessing.

---

## 📊 Step 5: Prepare Dataset

### Option A: Use Provided Script (Recommended)

```bash
python data/prepare_dataset.py
```

This will:
1. Load the Twitter Customer Support dataset
2. Process and categorize tickets
3. Create synthetic duplicates
4. Split into train/test (80/20)
5. Save to `data/train.csv` and `data/test.csv`

**Processing time**: ~2-3 minutes  
**Output**: ~120,000 samples

### Option B: Use Your Own Dataset

If you have your own dataset:

1. Place your CSV in `data/raw/`
2. Modify `data/prepare_dataset.py` to load your data
3. Ensure columns: `text` (ticket text) and `category` (label)
4. Run the script

---

## 🎓 Step 6: Train Models

### Option A: Use Jupyter Notebook (Recommended)

```bash
jupyter notebook notebooks/complete_training_pipeline.ipynb
```

Then:
1. Open the notebook in your browser
2. Run all cells (Cell → Run All)
3. Wait for training to complete

**Training time**:
- NLP Pipeline: ~5 minutes
- DL Pipeline: ~15 minutes (CPU) / ~3 minutes (GPU)
- **Total**: ~20 minutes

### Option B: Train Separately (Advanced)

```bash
# Train NLP model
python nlp_module/train_nlp_enhanced.py

# Train DL model
python dl_module/train_dl.py
```

### What Gets Created

After training, you'll have 10 model files in `models/`:

**NLP Models** (7 files):
- `word_tfidf_vectorizer.pkl` - Word TF-IDF vectorizer
- `char_tfidf_vectorizer.pkl` - Character TF-IDF vectorizer
- `word2vec_model.pkl` - Word2Vec embeddings
- `text_stats_scaler.pkl` - Text statistics scaler
- `nlp_classifier_enhanced.pkl` - XGBoost classifier
- `label_encoder.pkl` - Category encoder
- `train_word_tfidf_vectors.npz` - Training vectors

**DL Models** (3 files):
- `dl_model.h5` - LSTM model
- `tokenizer.pkl` - Keras tokenizer
- `train_embeddings_normalized.npy` - Training embeddings

---

## 🎬 Step 7: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ✅ Step 8: Verify Installation

### Test Single Ticket Analysis

1. Go to **"Analyze Ticket"** page
2. Enter: `"My payment failed but I was charged twice"`
3. Click **"Analyze Ticket"**
4. You should see predictions from both models

### Test Batch Processing

1. Create a test CSV:
```csv
id,text
1,"Payment issue with my order"
2,"Cannot login to account"
3,"Package not delivered"
```

2. Go to **"Batch Processing"** page
3. Upload the CSV
4. Click **"Process All Tickets"**
5. Download results

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
pip install -r requirements.txt
```

### Issue: "NLTK data not found"

**Solution**: Download NLTK data
```bash
python -c "import nltk; nltk.download('all')"
```

### Issue: "TensorFlow DLL load failed" (Windows)

**Solution**: Install Visual C++ Redistributable
- Download from: https://aka.ms/vs/16/release/vc_redist.x64.exe
- Or use tensorflow-cpu instead

### Issue: "Out of memory" during training

**Solution**: Reduce batch size or dataset size
- Edit notebook: Change `batch_size=32` to `batch_size=16`
- Or use smaller dataset

### Issue: Streamlit app won't start

**Solution**: Check port availability
```bash
streamlit run app.py --server.port 8502
```

### Issue: Models not loading

**Solution**: Ensure all 10 model files exist in `models/` directory
```bash
ls models/  # Linux/Mac
dir models\  # Windows
```

---

## 🔄 Updating the Project

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🗑️ Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf customer-support-ai  # Linux/Mac
rmdir /s customer-support-ai  # Windows
```

---

## 📞 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [GitHub Issues](https://github.com/yourusername/customer-support-ai/issues)
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

---

## 🎉 Next Steps

Once setup is complete:

1. **Explore the App**: Try different ticket examples
2. **Read the Docs**: Check `docs/BATCH_PROCESSING_GUIDE.md`
3. **Experiment**: Modify models, try different parameters
4. **Contribute**: See `CONTRIBUTING.md` for guidelines

---

**Setup complete! You're ready to classify tickets! 🚀**

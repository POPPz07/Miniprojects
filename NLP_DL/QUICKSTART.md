# ⚡ Quick Start (5 Minutes)

Get up and running in 5 minutes!

---

## 🚀 Fast Track Setup

```bash
# 1. Clone & Navigate
git clone https://github.com/yourusername/customer-support-ai.git
cd customer-support-ai

# 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Download NLTK Data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 5. Prepare Dataset
python data/prepare_dataset.py

# 6. Train Models (open Jupyter)
jupyter notebook notebooks/complete_training_pipeline.ipynb
# Run all cells, wait ~20 minutes

# 7. Run App
streamlit run app.py
```

---

## 📝 What You Get

After setup:
- ✅ Web app at `http://localhost:8501`
- ✅ Single ticket analysis
- ✅ Batch CSV processing
- ✅ Model comparison
- ✅ Performance metrics

---

## 🎯 First Test

1. Go to **"Analyze Ticket"**
2. Enter: `"My payment failed but I was charged twice"`
3. Click **"Analyze Ticket"**
4. See NLP vs DL predictions!

---

## 📚 Full Documentation

- **Complete Guide**: See `README.md`
- **Detailed Setup**: See `SETUP.md`
- **Batch Processing**: See `docs/BATCH_PROCESSING_GUIDE.md`

---

**That's it! You're ready to go! 🎉**

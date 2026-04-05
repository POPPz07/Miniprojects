# 🚀 Quick Start Guide

Get the Streamlit app running in 3 simple steps!

---

## ⚡ 3-Step Launch

### Step 1: Verify Models ✅
Check that all 7 model files exist in `models/` directory:

```
models/
├── tfidf_vectorizer.pkl ✓
├── nlp_classifier.pkl ✓
├── label_encoder.pkl ✓
├── train_tfidf_vectors.npz ✓
├── dl_model.h5 ✓
├── tokenizer.pkl ✓
└── train_embeddings_normalized.npy ✓
```

### Step 2: Launch App 🚀

**Option A: Double-click launcher**
```
run_app.bat
```

**Option B: PowerShell**
```powershell
.\run_app.ps1
```

**Option C: Manual**
```bash
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

### Step 3: Open Browser 🌐
The app will automatically open at:
```
http://localhost:8501
```

---

## 🎯 First Test

### Test 1: Analyze a Ticket

1. Click **"Analyze Ticket"** in sidebar
2. Enter this text:
   ```
   My payment failed but I was charged twice. Please refund the duplicate charge.
   ```
3. Click **"🚀 Analyze Ticket"**
4. See results:
   - **Category:** Billing
   - **Confidence:** ~95%
   - **Duplicate:** No

### Test 2: Batch Processing

1. Click **"Batch Processing"** in sidebar
2. Create a test CSV:
   ```csv
   text
   "My payment failed"
   "App keeps crashing"
   "Order hasn't arrived"
   ```
3. Upload the CSV
4. Click **"🚀 Process All Tickets"**
5. Download results

---

## 📊 What to Explore

### 🏠 Home Page
- See project overview
- View key metrics
- Understand workflow

### 🔍 Analyze Ticket
- Test single tickets
- Compare NLP vs DL
- See confidence scores

### 📦 Batch Processing
- Upload CSV files
- Process multiple tickets
- Download results

### 📊 Model Comparison
- View performance metrics
- Understand differences
- See visualizations

### ℹ️ About
- Technical details
- Implementation info
- Dataset statistics

---

## 🎨 Sample Tickets to Try

### Billing Issues
```
My credit card was charged twice for the same order
I need a refund for the duplicate payment
The payment went through but order was cancelled
```

### Technical Issues
```
The app crashes every time I try to login
Getting error 500 when submitting form
Cannot upload files, keeps timing out
```

### Delivery Issues
```
My order hasn't arrived yet, been 2 weeks
Tracking shows delivered but I didn't receive it
Wrong item was shipped to my address
```

### Account Issues
```
Cannot reset my password, not receiving email
Account was locked after failed login attempts
Need to update my email address in profile
```

---

## 🔧 Troubleshooting

### App Won't Start
```bash
# Check if venv is activated
.\venv\Scripts\Activate.ps1

# Check if streamlit is installed
pip list | findstr streamlit

# Reinstall if needed
pip install streamlit
```

### Models Not Loading
```bash
# Check if all files exist
dir models\

# Should see 7 files
# If missing, download from Google Colab
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Browser Doesn't Open
```
Manually open: http://localhost:8501
```

---

## 💡 Tips

### Performance
- First load takes ~5 seconds (loading models)
- Subsequent predictions are instant (cached)
- Batch processing: ~100ms per ticket

### Best Practices
- Use clear, descriptive ticket text
- Avoid very short text (<3 words)
- For batch: CSV must have 'text' column

### Keyboard Shortcuts
- `Ctrl + C` - Stop server
- `R` - Rerun app
- `C` - Clear cache

---

## 📚 Documentation

- **Full Guide:** `STREAMLIT_README.md`
- **Summary:** `STREAMLIT_APP_SUMMARY.md`
- **Visual Guide:** `APP_SCREENSHOTS_GUIDE.md`

---

## ✅ Success Checklist

- [ ] Models loaded without errors
- [ ] Home page displays correctly
- [ ] Can analyze single ticket
- [ ] Can upload CSV for batch
- [ ] Charts render properly
- [ ] Download CSV works

---

## 🎉 You're Ready!

The app is now running and ready to use. Explore the different pages and test with your own tickets!

**Need Help?**
- Check `STREAMLIT_README.md` for detailed docs
- Review `APP_SCREENSHOTS_GUIDE.md` for visual reference
- See `STREAMLIT_APP_SUMMARY.md` for complete overview

---

**Happy Analyzing! 🎫**

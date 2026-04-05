# 🚀 Deployment Checklist

Complete checklist for deploying the Ticket Classification System to production.

## 📋 Pre-Deployment Tasks

### 1. Dataset Preparation ✅ DONE
- [x] Updated `prepare_dataset.py` to use 200k rows (generates ~100k samples)
- [ ] Run `python data/prepare_dataset.py` locally
- [ ] Verify `data/train.csv` has ~80k samples
- [ ] Verify `data/test.csv` has ~20k samples
- [ ] Verify `data/test.csv` has ~10k samples
- [ ] Upload train.csv and test.csv to Google Drive (for Colab)

### 2. Model Training
- [ ] Open `notebooks/complete_training_pipeline.ipynb` in Google Colab
- [ ] Upload train.csv when prompted
- [ ] Run all cells (estimated time: ~20 minutes)
- [ ] Verify training completes without errors
- [ ] Check final metrics:
  - NLP Classification Accuracy: 93-95%
  - DL Classification Accuracy: 92-94%
  - NLP Duplicate F1: 35-45%
  - DL Duplicate F1: 60-70%

### 3. Model Download
- [ ] Download all NLP models:
  - `nlp_classifier.pkl` (XGBoost)
  - `tfidf_vectorizer.pkl`
  - `char_vectorizer.pkl`
  - `word2vec_model.pkl`
  - `label_encoder.pkl`
  - `train_tfidf_vectors.npz`
- [ ] Download all DL models:
  - `dl_model.h5`
  - `tokenizer.pkl`
  - `train_embeddings_normalized.npy`
- [ ] Place all models in `models/` directory
- [ ] Verify all 9 model files exist

### 4. Application Updates
- [ ] Read `APP_UPDATE_GUIDE.md` carefully
- [ ] Update `app.py` imports (add scipy.sparse, gensim)
- [ ] Replace `load_nlp_models()` function
- [ ] Add helper functions (get_document_embedding, extract_text_statistics)
- [ ] Replace `predict_nlp()` function
- [ ] Update all model loading calls (6 parameters instead of 4)
- [ ] Update UI text: "Logistic Regression" → "XGBoost"
- [ ] Update batch processing function

### 5. Local Testing
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Download NLTK data
- [ ] Run app locally: `streamlit run app.py`
- [ ] Test single ticket prediction (NLP)
- [ ] Test single ticket prediction (DL)
- [ ] Test batch processing with sample CSV
- [ ] Check Model Comparison page
- [ ] Verify all metrics display correctly
- [ ] Test with various ticket types
- [ ] Check for any errors in console

### 6. Project Cleanup
- [ ] Review `cleanup_project.py`
- [ ] Run cleanup script: `python cleanup_project.py`
- [ ] Verify unused files are removed
- [ ] Check project structure is clean

### 7. Documentation
- [x] README.md created
- [x] APP_UPDATE_GUIDE.md created
- [x] NOTEBOOK_INSTRUCTIONS.md created
- [x] requirements.txt updated
- [x] .streamlit/config.toml created
- [ ] Update any project-specific details in README.md

## 🌐 Deployment to Streamlit Cloud

### 8. Git Repository Setup
- [ ] Initialize git (if not already): `git init`
- [ ] Create .gitignore:
  ```
  venv/
  __pycache__/
  *.pyc
  .DS_Store
  .env
  data/raw/
  *.log
  ```
- [ ] Add all files: `git add .`
- [ ] Commit: `git commit -m "Initial commit - Ready for deployment"`
- [ ] Create GitHub repository
- [ ] Push to GitHub: `git push origin main`

### 9. Model Files (Large Files)
- [ ] Check model file sizes
- [ ] If any file > 100MB:
  - [ ] Install Git LFS: `git lfs install`
  - [ ] Track large files: `git lfs track "*.h5" "*.npy" "*.npz"`
  - [ ] Commit .gitattributes
  - [ ] Push with LFS
- [ ] Alternative: Use external storage (Google Drive, S3) and download on startup

### 10. Streamlit Cloud Deployment
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Sign in with GitHub
- [ ] Click "New app"
- [ ] Select your repository
- [ ] Set main file: `app.py`
- [ ] Set Python version: 3.8 or higher
- [ ] Click "Deploy"
- [ ] Wait for deployment (~5-10 minutes)

### 11. Post-Deployment Verification
- [ ] App loads without errors
- [ ] All pages accessible
- [ ] Models load successfully
- [ ] Single prediction works
- [ ] Batch processing works
- [ ] Metrics display correctly
- [ ] No console errors
- [ ] Performance is acceptable

### 12. Monitoring & Maintenance
- [ ] Check Streamlit Cloud logs for errors
- [ ] Monitor app performance
- [ ] Set up error notifications (if available)
- [ ] Plan for model updates
- [ ] Document any issues

## 📊 Performance Benchmarks

Expected performance after deployment:

| Metric | Target | Status |
|--------|--------|--------|
| App Load Time | < 10s | ⏳ |
| Model Load Time | < 5s | ⏳ |
| Single Prediction | < 1s | ⏳ |
| Batch Processing (100 tickets) | < 30s | ⏳ |
| Memory Usage | < 2GB | ⏳ |
| NLP Classification Accuracy | 93-95% | ⏳ |
| DL Classification Accuracy | 92-94% | ⏳ |
| NLP Duplicate F1 | 35-45% | ⏳ |
| DL Duplicate F1 | 60-70% | ⏳ |

## 🐛 Troubleshooting

### Common Issues

**Issue: Models not loading**
- Solution: Check file paths, ensure all 9 model files exist
- Verify file permissions

**Issue: Import errors**
- Solution: Check requirements.txt, ensure all dependencies installed
- Run `pip install -r requirements.txt --upgrade`

**Issue: NLTK data not found**
- Solution: Add NLTK download to app startup:
  ```python
  import nltk
  nltk.download('punkt', quiet=True)
  nltk.download('stopwords', quiet=True)
  nltk.download('wordnet', quiet=True)
  ```

**Issue: Out of memory**
- Solution: Reduce batch size, optimize model loading
- Use Streamlit Cloud's higher tier

**Issue: Slow predictions**
- Solution: Check model caching (@st.cache_resource)
- Optimize preprocessing pipeline

**Issue: Git LFS quota exceeded**
- Solution: Use external storage for models
- Download models on app startup from Google Drive/S3

## ✅ Final Checklist

Before going live:

- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Models are trained and downloaded
- [ ] App.py is updated
- [ ] Local testing successful
- [ ] Git repository is clean
- [ ] Deployment successful
- [ ] Post-deployment verification complete
- [ ] Performance meets benchmarks
- [ ] Error handling is robust

## 🎉 Success Criteria

Your deployment is successful when:

✅ App loads without errors
✅ All features work as expected
✅ Performance meets targets
✅ Models predict accurately
✅ UI is responsive and professional
✅ No critical bugs or errors

## 📞 Support

If you encounter issues:

1. Check Streamlit Cloud logs
2. Review error messages carefully
3. Consult documentation (README.md, guides)
4. Check GitHub issues
5. Contact support or create an issue

## 🔄 Update Process

For future updates:

1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub
4. Streamlit Cloud auto-deploys
5. Verify deployment
6. Monitor for issues

---

**Good luck with your deployment! 🚀**

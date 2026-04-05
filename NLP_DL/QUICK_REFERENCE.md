# 🚀 Quick Reference Card

## 📋 Essential Commands

### Dataset Generation
```bash
python data/prepare_dataset.py
```
**Output**: `data/train.csv` (~40k), `data/test.csv` (~10k)

### Local Testing
```bash
pip install -r requirements.txt
streamlit run app.py
```
**URL**: http://localhost:8501

### Cleanup
```bash
python cleanup_project.py
```

### Git Commands
```bash
git add .
git commit -m "Your message"
git push origin main
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `data/prepare_dataset.py` | Generate train/test data |
| `preprocessing/text_cleaner.py` | Text preprocessing |
| `requirements.txt` | Python dependencies |
| `README.md` | Main documentation |

## 🤖 Model Files (9 total)

### NLP Models (6 files)
1. `nlp_classifier.pkl` - XGBoost classifier
2. `tfidf_vectorizer.pkl` - Word TF-IDF
3. `char_vectorizer.pkl` - Character TF-IDF
4. `word2vec_model.pkl` - Word2Vec embeddings
5. `label_encoder.pkl` - Label encoder
6. `train_tfidf_vectors.npz` - Training vectors

### DL Models (3 files)
7. `dl_model.h5` - LSTM model
8. `tokenizer.pkl` - Keras tokenizer
9. `train_embeddings_normalized.npy` - LSTM embeddings

## 📊 Expected Performance

| Metric | NLP | DL |
|--------|-----|-----|
| Classification Accuracy | 93-95% | 92-94% |
| Duplicate Detection F1 | 35-45% | 60-70% |
| Inference Speed | ~10ms | ~50ms |

## 🔧 Troubleshooting

### Models not loading
```python
# Check file exists
import os
print(os.path.exists('models/nlp_classifier.pkl'))
```

### NLTK data missing
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Import errors
```bash
pip install -r requirements.txt --upgrade
```

### Memory issues
- Reduce batch size in app.py
- Use Streamlit Cloud higher tier
- Optimize model loading

## 📝 Workflow Steps

1. ✅ Generate dataset → `python data/prepare_dataset.py`
2. ✅ Train models → Upload notebook to Colab, run all cells
3. ✅ Download models → Save to `models/` directory
4. ✅ Update app.py → Follow `APP_UPDATE_GUIDE.md`
5. ✅ Test locally → `streamlit run app.py`
6. ✅ Cleanup → `python cleanup_project.py`
7. ✅ Deploy → Push to GitHub, deploy on Streamlit Cloud

## 🌐 Deployment URLs

- **Streamlit Cloud**: https://share.streamlit.io
- **GitHub**: https://github.com/yourusername/your-repo
- **Your App**: https://your-app.streamlit.app

## 📚 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Complete project documentation |
| `APP_UPDATE_GUIDE.md` | How to update app.py |
| `NOTEBOOK_INSTRUCTIONS.md` | Training notebook guide |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |
| `PROJECT_COMPLETION_SUMMARY.md` | What's done, what's next |
| `QUICK_REFERENCE.md` | This file |

## 🎯 Quick Checks

### Before Training
- [ ] Dataset generated (~100k samples)
- [ ] train.csv and test.csv exist
- [ ] Notebook ready in Colab

### After Training
- [ ] All 9 model files downloaded
- [ ] Models in `models/` directory
- [ ] File sizes reasonable

### Before Deployment
- [ ] app.py updated
- [ ] Local testing successful
- [ ] All features working
- [ ] Cleanup complete

### After Deployment
- [ ] App loads without errors
- [ ] Predictions work
- [ ] Performance acceptable
- [ ] No console errors

## 💡 Pro Tips

1. **Use Git LFS** for files > 100MB
2. **Test incrementally** - don't change everything at once
3. **Keep backups** of working versions
4. **Monitor logs** on Streamlit Cloud
5. **Document changes** in commit messages

## 🆘 Emergency Contacts

- **Streamlit Docs**: https://docs.streamlit.io
- **TensorFlow Docs**: https://tensorflow.org
- **Scikit-learn Docs**: https://scikit-learn.org
- **XGBoost Docs**: https://xgboost.readthedocs.io

## 📞 Support Resources

1. Check documentation files
2. Review error messages
3. Search GitHub issues
4. Check Streamlit Community
5. Stack Overflow

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Dataset generation | 5 min |
| Model training (Colab) | 20 min |
| Model download | 2 min |
| App.py updates | 15 min |
| Local testing | 10 min |
| Cleanup | 2 min |
| Deployment | 10 min |
| **Total** | **~1 hour** |

## 🎉 Success Checklist

- [ ] Dataset: ~100k samples
- [ ] Models: All 9 files present
- [ ] App: Runs locally
- [ ] Tests: All passing
- [ ] Deploy: Successful
- [ ] Verify: Online and working

---

**Keep this file handy for quick reference! 📌**

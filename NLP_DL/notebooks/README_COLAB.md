# Deep Learning Pipeline - Google Colab Instructions

## Overview
Due to DLL compatibility issues on the local Windows system, the Deep Learning module is implemented as a Google Colab notebook.

## Files
- `dl_pipeline_colab.ipynb` - Complete Jupyter notebook for training LSTM model

## How to Use

### Step 1: Upload to Google Colab
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click "File" → "Upload notebook"
3. Upload `dl_pipeline_colab.ipynb`

### Step 2: Prepare train.csv
1. Locate your local `data/train.csv` file
2. Keep it ready for upload

### Step 3: Run the Notebook
1. In Colab, go to "Runtime" → "Change runtime type"
2. Select "GPU" as Hardware accelerator (optional but recommended)
3. Click "Save"
4. Run all cells sequentially (Runtime → Run all)
5. When prompted, upload `train.csv`

### Step 4: Download Trained Models
After training completes, the notebook will automatically download:
- `dl_model.h5` - Trained LSTM model
- `tokenizer.pkl` - Tokenizer with vocabulary
- `label_encoder.pkl` - Label encoder

### Step 5: Place Models Locally
1. Move downloaded files to your local `models/` directory:
   ```
   models/
   ├── dl_model.h5
   ├── tokenizer.pkl
   └── label_encoder.pkl
   ```

## What the Notebook Does

### 1. Setup
- Installs required packages (TensorFlow, NLTK, etc.)
- Downloads NLTK data
- Imports libraries

### 2. Preprocessing
- Uses SAME preprocessing logic as NLP pipeline
- Cleans text (HTML decoding, contraction expansion)
- Tokenizes and lemmatizes
- Removes stopwords (keeping negations)

### 3. Tokenization
- Creates Keras Tokenizer with `oov_token="<UNK>"`
- Fits ONLY on training data
- Pads sequences to max_length=100

### 4. Model Architecture
```
Embedding(vocab_size, 128, mask_zero=True)
LSTM(64)
Dropout(0.2)
Dense(32, relu)
Dense(4, softmax)
```

### 5. Training
- Epochs: 10
- Batch size: 32
- Validation split: 0.2
- Optimizer: Adam
- Loss: Categorical crossentropy

### 6. Outputs
- Training/validation accuracy curves
- Training/validation loss curves
- Sample predictions (5 examples)
- Final metrics

## Expected Results

### Training Metrics
- Training accuracy: ~95-98%
- Validation accuracy: ~90-93%
- Training time: ~5-10 minutes (with GPU)

### Sample Output
```
Final Metrics:
  Training Accuracy:   97.45%
  Validation Accuracy: 92.18%
  Training Loss:       0.0823
  Validation Loss:     0.2456
```

## Troubleshooting

### Issue: "train.csv not found"
**Solution**: Make sure to upload train.csv when prompted

### Issue: "Out of memory"
**Solution**: 
- Reduce batch size to 16
- Use GPU runtime (Runtime → Change runtime type → GPU)

### Issue: "Slow training"
**Solution**: Enable GPU acceleration in runtime settings

### Issue: "Download not working"
**Solution**: Manually download files from Colab's file browser (left sidebar)

## Alternative: Manual Download
If automatic download doesn't work:
1. Click the folder icon in left sidebar
2. Right-click on each file (dl_model.h5, tokenizer.pkl, label_encoder.pkl)
3. Select "Download"

## Next Steps
After downloading models:
1. Place them in local `models/` directory
2. Proceed with evaluation or Streamlit UI
3. Models are ready for inference

## Notes
- The notebook is self-contained and includes all necessary code
- No need to modify the notebook unless changing hyperparameters
- All preprocessing matches the NLP pipeline exactly
- Models are compatible with local inference scripts

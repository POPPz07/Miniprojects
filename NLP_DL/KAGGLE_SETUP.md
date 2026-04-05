# Kaggle API Setup Guide

## Step 1: Get Kaggle API Credentials

1. Go to [Kaggle Account Settings](https://www.kaggle.com/settings/account)
2. Scroll down to "API" section
3. Click "Create New API Token"
4. This will download `kaggle.json` file

## Step 2: Install Kaggle Credentials

### Windows:
```bash
# Create .kaggle directory in your home folder
mkdir %USERPROFILE%\.kaggle

# Move kaggle.json to .kaggle directory
move Downloads\kaggle.json %USERPROFILE%\.kaggle\

# Verify
dir %USERPROFILE%\.kaggle
```

### Linux/Mac:
```bash
# Create .kaggle directory
mkdir ~/.kaggle

# Move kaggle.json
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set permissions
chmod 600 ~/.kaggle/kaggle.json

# Verify
ls -la ~/.kaggle
```

## Step 3: Test Kaggle API

```bash
# Activate venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Test
kaggle datasets list
```

## Step 4: Run Dataset Preparation

```bash
python data/prepare_dataset.py
```

## Dataset Information

- **Name**: Customer Support on Twitter (twcs)
- **Kaggle URL**: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter
- **Size**: ~3 million tweets
- **Columns**: tweet_id, author_id, text, in_response_to_tweet_id, created_at, etc.

## Troubleshooting

### Error: "401 - Unauthorized"
- Check if kaggle.json is in the correct location
- Verify the file contains valid credentials

### Error: "403 - Forbidden"
- Accept the dataset's terms on Kaggle website first
- Visit: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter

### Error: "Dataset not found"
- Check internet connection
- Verify dataset name is correct

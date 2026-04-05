"""
Dataset Preparation Script
- Downloads Twitter customer support dataset from Kaggle (twcs)
- Cleans text
- Applies semi-supervised labeling
- Generates duplicates
- Splits into train/test with no duplicate leakage
"""

import pandas as pd
import numpy as np
import re
import random
import os
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# Configuration
KAGGLE_DATASET = "thoughtvector/customer-support-on-twitter"
DUPLICATE_RATIO = 0.25  # 25% duplicates (will result in ~33% when counting both original and duplicate)
TRAIN_TEST_SPLIT = 0.8

# Category keywords
CATEGORY_KEYWORDS = {
    'billing': ['payment', 'refund', 'charge', 'invoice', 'bill', 'paid', 'money', 'cost', 'price', 'fee'],
    'technical': ['error', 'issue', 'bug', 'crash', 'not working', 'broken', 'problem', 'fix', 'help', 'support'],
    'delivery': ['delivery', 'late', 'shipping', 'package', 'tracking', 'shipped', 'arrive', 'order', 'received'],
    'account': ['login', 'password', 'account', 'access', 'sign in', 'username', 'register', 'profile', 'email']
}

def clean_text(text):
    """Clean text by removing URLs, mentions, and extra spaces"""
    if pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove @mentions
    text = re.sub(r'@\w+', '', text)
    
    # Lowercase
    text = text.lower()
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def assign_category(text):
    """Assign category based on keyword matching"""
    text_lower = text.lower()
    
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[category] = score
    
    # Return category with highest score, or 'technical' as default
    max_category = max(scores, key=scores.get)
    return max_category if scores[max_category] > 0 else 'technical'

def generate_duplicate(text):
    """Generate a duplicate by applying simple transformations"""
    # Synonym replacements
    synonyms = {
        'payment': 'transaction',
        'failed': 'did not go through',
        'error': 'issue',
        'not working': 'broken',
        'help': 'assist',
        'fix': 'resolve',
        'late': 'delayed',
        'package': 'parcel',
        'account': 'profile',
        'login': 'sign in'
    }
    
    duplicate = text
    for original, replacement in synonyms.items():
        if original in duplicate:
            duplicate = duplicate.replace(original, replacement)
            break  # Only one replacement per duplicate
    
    # If no synonym replacement, try rephrasing
    if duplicate == text:
        rephrase_patterns = [
            (r'my (.+) is (.+)', r'the \1 is \2'),
            (r'i have (.+)', r'there is \1'),
            (r'can you (.+)', r'please \1'),
            (r'(.+) not working', r'\1 broken')
        ]
        
        for pattern, replacement in rephrase_patterns:
            if re.search(pattern, duplicate):
                duplicate = re.sub(pattern, replacement, duplicate)
                break
    
    return duplicate

def download_kaggle_dataset():
    """Download dataset from Kaggle using API (only if not already downloaded)"""
    print("\n[1/7] Checking dataset...")
    
    # Check if dataset already exists
    if os.path.exists('data/raw/twcs/twcs.csv') or os.path.exists('data/raw/twcs.csv'):
        print("✓ Dataset already exists, skipping download")
        return True
    
    print("Dataset not found, downloading from Kaggle...")
    
    # Check if Kaggle credentials exist
    kaggle_dir = os.path.expanduser("~/.kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    
    if not os.path.exists(kaggle_json):
        print("❌ Kaggle API credentials not found!")
        print("Please follow these steps:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Click 'Create New API Token'")
        print("3. Save kaggle.json to ~/.kaggle/")
        print("4. Run this script again")
        return None
    
    # Create raw data directory
    os.makedirs('data/raw', exist_ok=True)
    
    # Download dataset
    try:
        import kaggle
        print(f"Downloading {KAGGLE_DATASET}...")
        kaggle.api.dataset_download_files(
            KAGGLE_DATASET,
            path='data/raw',
            unzip=True
        )
        print("✓ Dataset downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

def prepare_dataset():
    """Main function to prepare the dataset"""
    print("=" * 60)
    print("DATASET PREPARATION")
    print("=" * 60)
    
    # Step 1: Download dataset
    download_result = download_kaggle_dataset()
    if download_result is None:
        print("\n⚠ Falling back to local file...")
    
    # Step 2: Load dataset
    print("\n[2/7] Loading dataset...")
    try:
        # Try to load the main twcs.csv file (check both possible locations)
        if os.path.exists('data/raw/twcs/twcs.csv'):
            df = pd.read_csv('data/raw/twcs/twcs.csv', encoding='latin-1')
        elif os.path.exists('data/raw/twcs.csv'):
            df = pd.read_csv('data/raw/twcs.csv', encoding='latin-1')
        else:
            raise FileNotFoundError("twcs.csv not found")
        
        print(f"✓ Loaded {len(df)} rows from Kaggle dataset")
        
        # Verify required columns
        required_cols = ['tweet_id', 'author_id', 'text', 'in_response_to_tweet_id']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"⚠ Missing columns: {missing_cols}")
            print(f"Available columns: {list(df.columns)}")
        else:
            print(f"✓ All required columns present: {required_cols}")
        
    except FileNotFoundError:
        print("❌ Dataset file not found!")
        print("Please ensure you have:")
        print("1. Kaggle API credentials configured")
        print("2. Internet connection")
        print("3. Or manually download from: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter")
        return
    
    # Use only 'text' column for processing
    if 'text' not in df.columns:
        print("❌ 'text' column not found in dataset!")
        return
    
    # Keep relevant columns
    df = df[['tweet_id', 'author_id', 'text', 'in_response_to_tweet_id']].copy()
    
    # Step 3: Clean and validate data
    print("\n[3/7] Cleaning and validating data...")
    
    # Remove rows with NaN or empty text
    df = df.dropna(subset=['text']).reset_index(drop=True)
    print(f"✓ Removed NaN values: {len(df)} rows remaining")
    
    # Clean text
    df['text'] = df['text'].apply(clean_text)
    
    # Remove empty texts after cleaning
    df = df[df['text'].str.len() > 0].reset_index(drop=True)
    
    # Remove very short texts (< 3 words)
    df = df[df['text'].str.split().str.len() >= 3].reset_index(drop=True)
    print(f"✓ Cleaned and validated: {len(df)} valid texts")
    
    # Limit to 500,000 samples for processing (will result in ~100k after balancing)
    # Need more initial samples because cleaning/filtering reduces the count significantly
    df = df.head(500000).reset_index(drop=True)
    
    # Step 4: Assign categories and balance
    print("\n[4/7] Assigning categories (semi-supervised)...")
    df['category'] = df['text'].apply(assign_category)
    
    # Show initial distribution
    category_counts = df['category'].value_counts()
    print("Initial category distribution:")
    for cat, count in category_counts.items():
        print(f"  {cat}: {count}")
    
    # Balance categories by undersampling
    print("\n[4/7] Balancing categories...")
    min_count = min(category_counts)
    target_count = min(min_count, 25000)  # Cap at 25000 per category (100k total)
    
    balanced_dfs = []
    for category in ['billing', 'technical', 'delivery', 'account']:
        cat_df = df[df['category'] == category]
        if len(cat_df) > target_count:
            cat_df = cat_df.sample(n=target_count, random_state=SEED)
        balanced_dfs.append(cat_df)
    
    df = pd.concat(balanced_dfs, ignore_index=True)
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)  # Shuffle
    
    print("Balanced category distribution:")
    for cat, count in df['category'].value_counts().items():
        print(f"  {cat}: {count}")
    
    # Step 5: Generate duplicates (to achieve ~25-35% final ratio)
    print(f"\n[5/7] Generating duplicates (target: 25-35% final ratio)...")
    
    # Mark all as non-duplicates initially
    df['is_duplicate'] = 0
    df['original_id'] = df.index
    
    # Select samples to duplicate (25% of current data)
    # This will result in: originals (25%) + duplicates (25%) = 50% marked as duplicate
    # But overall ratio will be: (25% + 25%) / (100% + 25%) = 40% which is still high
    # So we use 20% to get: (20% + 20%) / (100% + 20%) = 33%
    n_duplicates = int(len(df) * 0.20)
    duplicate_indices = np.random.choice(df.index, size=n_duplicates, replace=False)
    
    duplicates = []
    for idx in duplicate_indices:
        original_text = df.loc[idx, 'text']
        duplicate_text = generate_duplicate(original_text)
        
        duplicates.append({
            'tweet_id': np.nan,
            'author_id': np.nan,
            'text': duplicate_text,
            'in_response_to_tweet_id': np.nan,
            'category': df.loc[idx, 'category'],
            'is_duplicate': 1,
            'original_id': idx
        })
    
    # Mark originals as duplicates
    df.loc[duplicate_indices, 'is_duplicate'] = 1
    
    # Add duplicates to dataframe
    duplicate_df = pd.DataFrame(duplicates)
    df = pd.concat([df, duplicate_df], ignore_index=True)
    
    # Shuffle
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    
    print(f"✓ Generated {len(duplicates)} duplicates")
    print(f"✓ Total dataset size: {len(df)}")
    print(f"✓ Duplicate ratio: {df['is_duplicate'].sum() / len(df) * 100:.1f}%")
    
    # Step 6: Split with no duplicate leakage (strict 80/20)
    print("\n[6/7] Splitting into train/test (80/20)...")
    
    # Create groups: each group contains original + its duplicate (if exists)
    # Group by original_id to keep duplicate pairs together
    groups = []
    processed_ids = set()
    
    for idx in df.index:
        original_id = df.loc[idx, 'original_id']
        if original_id not in processed_ids:
            # Find all rows with this original_id (original + duplicate)
            group_indices = df[df['original_id'] == original_id].index.tolist()
            groups.append(group_indices)
            processed_ids.add(original_id)
    
    # Split groups with strict 80/20 ratio
    train_groups, test_groups = train_test_split(
        groups,
        train_size=TRAIN_TEST_SPLIT,
        random_state=SEED,
        shuffle=True
    )
    
    # Flatten indices
    train_indices = [idx for group in train_groups for idx in group]
    test_indices = [idx for group in test_groups for idx in group]
    
    train_df = df.loc[train_indices].reset_index(drop=True)
    test_df = df.loc[test_indices].reset_index(drop=True)
    
    # Remove original_id column (not needed anymore)
    train_df = train_df.drop('original_id', axis=1)
    test_df = test_df.drop('original_id', axis=1)
    
    # Add ticket_id
    train_df.insert(0, 'ticket_id', range(1, len(train_df) + 1))
    test_df.insert(0, 'ticket_id', range(1, len(test_df) + 1))
    
    print(f"✓ Train set: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)")
    print(f"✓ Test set: {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)")
    print(f"✓ Train duplicates: {train_df['is_duplicate'].sum()} ({train_df['is_duplicate'].sum()/len(train_df)*100:.1f}%)")
    print(f"✓ Test duplicates: {test_df['is_duplicate'].sum()} ({test_df['is_duplicate'].sum()/len(test_df)*100:.1f}%)")
    
    # Step 7: Save datasets
    print("\n[7/7] Saving datasets...")
    train_df.to_csv('data/train.csv', index=False)
    test_df.to_csv('data/test.csv', index=False)
    print("✓ Saved train.csv and test.csv")
    
    # Summary
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    print("\n📊 First 5 rows of train.csv:")
    print(train_df.head())
    
    print("\n📈 Category Distribution (Train):")
    print(train_df['category'].value_counts())
    
    print("\n📈 Category Distribution (Test):")
    print(test_df['category'].value_counts())
    
    print(f"\n🔄 Duplicate Ratio (Train): {train_df['is_duplicate'].sum() / len(train_df) * 100:.1f}%")
    print(f"🔄 Duplicate Ratio (Test): {test_df['is_duplicate'].sum() / len(test_df) * 100:.1f}%")
    
    print(f"\n📦 Total Dataset Size: {len(df)}")
    print(f"   - Train: {len(train_df)} ({len(train_df)/len(df)*100:.1f}%)")
    print(f"   - Test: {len(test_df)} ({len(test_df)/len(df)*100:.1f}%)")
    
    print("\n✅ Dataset preparation complete!")
    print("=" * 60)

if __name__ == "__main__":
    prepare_dataset()

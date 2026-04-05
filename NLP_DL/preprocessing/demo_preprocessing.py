"""
Demonstration of preprocessing on actual dataset samples
Shows raw vs processed text
"""

import pandas as pd
import sys
sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Set random seed
import random
import numpy as np
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

def demo_preprocessing():
    """Demonstrate preprocessing on real dataset samples"""
    print("=" * 80)
    print("PREPROCESSING DEMONSTRATION - RAW VS PROCESSED")
    print("=" * 80)
    
    # Load train dataset
    try:
        df = pd.read_csv('data/train.csv')
        print(f"\n✓ Loaded {len(df)} samples from train.csv")
    except FileNotFoundError:
        print("❌ train.csv not found. Please run data/prepare_dataset.py first.")
        return
    
    # Select 5 random samples
    samples = df.sample(n=5, random_state=SEED)
    
    print("\n" + "=" * 80)
    print("SAMPLE PREPROCESSING RESULTS")
    print("=" * 80)
    
    for idx, (i, row) in enumerate(samples.iterrows(), 1):
        print(f"\n{'='*80}")
        print(f"SAMPLE {idx}")
        print(f"{'='*80}")
        print(f"Category: {row['category']}")
        print(f"Is Duplicate: {row['is_duplicate']}")
        print(f"\n📄 RAW TEXT:")
        print(f"  {row['text']}")
        
        try:
            processed, metadata = preprocess_pipeline(row['text'])
            print(f"\n✨ PROCESSED TEXT:")
            print(f"  {processed}")
            
            if metadata['warning']:
                print(f"\n{metadata['warning']}")
            
            print(f"\n📊 STATISTICS:")
            print(f"  Original length: {metadata['original_length']} characters")
            print(f"  Processed tokens: {metadata['processed_length']} tokens")
            print(f"  Reduction: {(1 - metadata['processed_length']/len(row['text'].split()))*100:.1f}%")
            
        except PreprocessingError as e:
            print(f"\n❌ ERROR: {e}")
    
    print("\n" + "=" * 80)
    print("PREPROCESSING PIPELINE SUMMARY")
    print("=" * 80)
    print("\nSteps:")
    print("  1. clean_text()        → lowercase, remove punctuation, extra spaces")
    print("  2. tokenize()          → word tokenization")
    print("  3. remove_stopwords()  → filter NLTK stopwords")
    print("  4. lemmatize()         → WordNet lemmatization")
    
    print("\nEdge Cases Handled:")
    print("  ✓ Empty input          → PreprocessingError")
    print("  ✓ Very short text      → Warning message")
    print("  ✓ Special chars only   → PreprocessingError")
    
    print("\n✅ This preprocessing module will be used by:")
    print("  - NLP Pipeline (TF-IDF + Classification)")
    print("  - DL Pipeline (LSTM + Embeddings)")
    print("  - Streamlit UI (Inference)")
    print("=" * 80)

if __name__ == "__main__":
    demo_preprocessing()

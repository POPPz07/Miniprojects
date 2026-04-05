"""
Shared Text Preprocessing Module
- Used by both NLP and DL pipelines
- Ensures consistent preprocessing across training and inference
"""

import re
import string
import html
import nltk
import contractions
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Set random seed for reproducibility
import random
import numpy as np
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Download required NLTK data (only once)
def download_nltk_data():
    """Download required NLTK datasets"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading required NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        print("✓ NLTK data downloaded")

# Initialize once
download_nltk_data()

# Custom stopwords list (exclude important negations)
STOP_WORDS = set(stopwords.words('english'))
# Keep important words
KEEP_WORDS = {'not', 'no', 'nor', 'neither', 'never', 'none', 'nothing', 'nowhere'}
STOP_WORDS = STOP_WORDS - KEEP_WORDS

LEMMATIZER = WordNetLemmatizer()


class PreprocessingError(Exception):
    """Custom exception for preprocessing errors"""
    pass


def clean_text(text):
    """
    Clean text by:
    - Decoding HTML entities
    - Fixing encoding issues
    - Expanding contractions
    - Lowercasing
    - Replacing punctuation with space (not removing)
    - Removing extra spaces
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
        
    Raises:
        PreprocessingError: If input is empty or invalid
    """
    # Handle None or empty input
    if text is None or (isinstance(text, str) and text.strip() == ""):
        raise PreprocessingError("Input cannot be empty")
    
    # Convert to string
    text = str(text)
    
    # Decode HTML entities (&amp; → &, &lt; → <, etc.)
    text = html.unescape(text)
    
    # Fix common encoding issues
    text = text.replace('â€™', "'")  # Smart apostrophe
    text = text.replace('â€œ', '"')  # Smart quote left
    text = text.replace('â€', '"')   # Smart quote right
    text = text.replace('â€"', '-')  # Em dash
    text = text.replace('â€"', '-')  # En dash
    text = text.replace('Â', ' ')    # Non-breaking space
    
    # Expand contractions BEFORE lowercasing (contractions library is case-sensitive)
    text = contractions.fix(text)
    
    # Lowercase
    text = text.lower()
    
    # Replace punctuation with space (to avoid merging words)
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Check if only special characters (results in empty after cleaning)
    if text == "":
        raise PreprocessingError("Text contains only special characters")
    
    return text


def tokenize(text):
    """
    Tokenize text into words
    
    Args:
        text (str): Cleaned text
        
    Returns:
        list: List of tokens
    """
    if not text or text.strip() == "":
        return []
    
    tokens = word_tokenize(text)
    return tokens


def remove_stopwords(tokens):
    """
    Remove stopwords from token list (keeping important negations)
    
    Args:
        tokens (list): List of tokens
        
    Returns:
        list: Filtered tokens without stopwords (but keeping 'not', 'no', etc.)
    """
    if not tokens:
        return []
    
    filtered_tokens = [token for token in tokens if token not in STOP_WORDS]
    return filtered_tokens


def lemmatize(tokens):
    """
    Lemmatize tokens using WordNet lemmatizer
    
    Args:
        tokens (list): List of tokens
        
    Returns:
        list: Lemmatized tokens
    """
    if not tokens:
        return []
    
    lemmatized_tokens = [LEMMATIZER.lemmatize(token) for token in tokens]
    return lemmatized_tokens


def preprocess_pipeline(text, return_string=True):
    """
    Complete preprocessing pipeline:
    clean → tokenize → remove stopwords → lemmatize
    
    Args:
        text (str): Raw input text
        return_string (bool): If True, return joined string; if False, return token list
        
    Returns:
        str or list: Processed text (string or tokens)
        dict: Metadata with warnings
        
    Raises:
        PreprocessingError: If input is invalid
    """
    metadata = {
        'warning': None,
        'original_length': len(text) if text else 0,
        'processed_length': 0
    }
    
    try:
        # Step 1: Clean
        cleaned = clean_text(text)
        
        # Step 2: Tokenize
        tokens = tokenize(cleaned)
        
        # Check for very short text
        if len(tokens) < 3:
            metadata['warning'] = "⚠️ Warning: Text is very short. Results may be unreliable."
        
        # Step 3: Remove stopwords
        filtered = remove_stopwords(tokens)
        
        # Step 4: Lemmatize
        lemmatized = lemmatize(filtered)
        
        # Update metadata
        metadata['processed_length'] = len(lemmatized)
        
        # Return as string or list
        if return_string:
            result = ' '.join(lemmatized)
        else:
            result = lemmatized
        
        return result, metadata
        
    except PreprocessingError as e:
        raise e
    except Exception as e:
        raise PreprocessingError(f"Preprocessing failed: {str(e)}")


def validate_input(text):
    """
    Validate input text before preprocessing
    
    Args:
        text (str): Input text
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not text or text.strip() == "":
        return False, "❌ Input cannot be empty"
    
    try:
        cleaned = clean_text(text)
        tokens = tokenize(cleaned)
        
        if len(tokens) < 3:
            return True, "⚠️ Warning: Text is very short. Results may be unreliable."
        
        return True, None
        
    except PreprocessingError as e:
        return False, f"❌ {str(e)}"
    except Exception as e:
        return False, f"❌ Validation failed: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("TEXT PREPROCESSING MODULE - TEST")
    print("=" * 60)
    
    # Test cases
    test_texts = [
        "My payment failed but I was charged twice!",
        "The app keeps crashing when I try to login.",
        "Order hasn't arrived yet.",
        "Hi",  # Very short
        "!!!",  # Only special characters
        ""  # Empty
    ]
    
    print("\n📝 Testing preprocessing pipeline:\n")
    
    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: '{text}'")
        
        try:
            processed, metadata = preprocess_pipeline(text)
            print(f"  ✓ Processed: '{processed}'")
            if metadata['warning']:
                print(f"  {metadata['warning']}")
            print(f"  Original length: {metadata['original_length']} chars")
            print(f"  Processed tokens: {metadata['processed_length']}")
        except PreprocessingError as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    # Additional tests for new features
    print("\n" + "=" * 60)
    print("TESTING NEW FEATURES")
    print("=" * 60)
    
    new_tests = [
        ("HTML entities", "I can't believe it &amp; it's not working!"),
        ("Contractions", "hasn't, didn't, won't, shouldn't"),
        ("Negations", "This is not good and no one can help"),
        ("Encoding issues", "It is broken please fix")
    ]
    
    for test_name, text in new_tests:
        print(f"\n{test_name}: '{text}'")
        try:
            processed, _ = preprocess_pipeline(text)
            print(f"  ✓ Processed: '{processed}'")
        except PreprocessingError as e:
            print(f"  ❌ Error: {e}")

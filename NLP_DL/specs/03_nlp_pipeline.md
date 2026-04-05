# 🟢 NLP Pipeline Specification

## Step 1: Preprocessing

Implement manually:
- Lowercasing
- Remove punctuation
- Tokenization
- Stopword removal
- Lemmatization or stemming

## Step 2: Feature Extraction

Use TF-IDF:
- max_features = 5000
- ngram_range = (1,2)

## Step 3: Duplicate Detection

- Compute cosine similarity
- Threshold = 0.8

If similarity > threshold → duplicate

## Step 4: Classification

Use:
- Logistic Regression OR Naive Bayes

## Outputs

- Predicted category
- Duplicate flag
- Similarity score

## Evaluation

- Accuracy
- Confusion matrix
- Precision, Recall

## Important

Show:
- Preprocessed text
- TF-IDF vector shape
- Sample predictions
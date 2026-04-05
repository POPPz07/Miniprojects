# 🧠 Project Overview: Ticket Deduplication & Routing System

## Objective
Build a system that:
1. Detects duplicate customer tickets
2. Routes tickets to correct department

## Two Separate Implementations

### 🟢 NLP Pipeline
- Manual preprocessing
- TF-IDF feature extraction
- Logistic Regression / Naive Bayes
- Cosine similarity for duplicate detection

### 🔵 Deep Learning Pipeline
- Tokenization + padding
- LSTM-based RNN
- Dense layers for classification
- Optional similarity logic

## Core Requirement
Both pipelines must:
- Work independently
- Be clearly distinguishable
- Produce comparable outputs

## Final Output
For any input ticket:
- Duplicate or not
- Category (billing, technical, delivery, account)
- NLP vs DL comparison
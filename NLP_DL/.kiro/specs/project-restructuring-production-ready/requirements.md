# Requirements Document

## Introduction

This document specifies the requirements for restructuring a customer support ticket classification system to be production-ready. The system uses both NLP (Natural Language Processing) and Deep Learning pipelines for ticket classification and duplicate detection. The restructuring aims to consolidate training workflows, enhance model performance, clean up unused files, and prepare the system for deployment.

## Glossary

- **System**: The complete customer support ticket classification application
- **Training_Notebook**: The unified Jupyter/Colab notebook for training all models
- **NLP_Pipeline**: Traditional machine learning approach using TF-IDF, Character n-grams, Word2Vec, and XGBoost
- **DL_Pipeline**: Deep learning approach using LSTM neural networks
- **Streamlit_App**: The web application interface for ticket classification
- **Dataset_Preparation**: The script that prepares training and test data from raw sources
- **Model_Artifacts**: Trained model files (.pkl, .h5, .npy, .npz) stored in the models/ directory
- **Documentation**: README and guide files for users and developers
- **Deployment_Configuration**: Settings and files required for cloud deployment

## Requirements

### Requirement 1: Unified Training Notebook Creation

**User Story:** As a data scientist, I want a single comprehensive training notebook, so that I can train all models in one place without switching between multiple scripts.

#### Acceptance Criteria

1. THE Training_Notebook SHALL contain exactly 5 parts: Setup & Data Loading, Enhanced NLP Training, Deep Learning Training, Evaluation & Comparison, and Model Download
2. WHEN the Setup & Data Loading part executes, THE Training_Notebook SHALL install dependencies, import libraries, download NLTK data, and upload train.csv
3. WHEN the Enhanced NLP Training part executes, THE Training_Notebook SHALL train Word TF-IDF vectorizer, Character TF-IDF vectorizer, Word2Vec embeddings, text statistics features, and XGBoost classifier
4. WHEN the Deep Learning Training part executes, THE Training_Notebook SHALL train LSTM model with Embedding layer, LSTM layer, Dropout layer, and Dense layers
5. WHEN the Evaluation & Comparison part executes, THE Training_Notebook SHALL evaluate both pipelines on test data and compare classification accuracy and duplicate detection F1-scores
6. WHEN the Model Download part executes, THE Training_Notebook SHALL provide download functionality for all trained model artifacts
7. THE Training_Notebook SHALL include progress indicators, error handling with try-except blocks, and validation checks after each major step
8. THE Training_Notebook SHALL include clear section markers, cell titles, and expected output descriptions for each cell
9. THE Training_Notebook SHALL be compatible with Google Colab environment
10. THE Training_Notebook SHALL complete execution within 30 minutes on Google Colab with GPU

### Requirement 2: Enhanced NLP Pipeline Implementation

**User Story:** As a machine learning engineer, I want an enhanced NLP pipeline with multiple feature types, so that I can achieve better classification and duplicate detection performance.

#### Acceptance Criteria

1. THE NLP_Pipeline SHALL extract Word TF-IDF features with 10,000 max features, 1-3 word n-grams, and sublinear term frequency scaling
2. THE NLP_Pipeline SHALL extract Character TF-IDF features with 2,000 max features and 3-5 character n-grams for handling typos
3. THE NLP_Pipeline SHALL train Word2Vec embeddings with 100 dimensions on the training corpus
4. THE NLP_Pipeline SHALL compute text statistics features including text length, word count, average word length, punctuation count, uppercase ratio, digit count, stopword ratio, unique word ratio, sentence count, and average sentence length
5. THE NLP_Pipeline SHALL use XGBoost classifier with 200 estimators, max depth of 6, and learning rate of 0.1
6. WHEN the NLP_Pipeline trains on the full dataset, THE NLP_Pipeline SHALL achieve classification accuracy between 93% and 95%
7. WHEN the NLP_Pipeline performs duplicate detection, THE NLP_Pipeline SHALL achieve F1-score between 35% and 45%
8. THE NLP_Pipeline SHALL save the following model artifacts: nlp_classifier.pkl, tfidf_vectorizer.pkl, char_vectorizer.pkl, word2vec_model.pkl, train_tfidf_vectors.npz, train_word2vec_embeddings.npy, and label_encoder.pkl

### Requirement 3: Optimized Deep Learning Pipeline

**User Story:** As a machine learning engineer, I want an optimized LSTM model trained on the full dataset, so that I can achieve better performance especially for duplicate detection.

#### Acceptance Criteria

1. THE DL_Pipeline SHALL use an LSTM architecture with Embedding layer (vocab_size, 128, mask_zero=True), LSTM layer (64 units), Dropout layer (0.2), Dense layer (32 units, relu), and output Dense layer (4 units, softmax)
2. WHEN the DL_Pipeline trains on the full dataset, THE DL_Pipeline SHALL achieve classification accuracy between 92% and 94%
3. WHEN the DL_Pipeline performs duplicate detection using LSTM embeddings, THE DL_Pipeline SHALL achieve F1-score between 60% and 70%
4. THE DL_Pipeline SHALL train for 10 epochs with batch size of 32 and validation split of 0.2
5. THE DL_Pipeline SHALL use Adam optimizer and categorical crossentropy loss
6. THE DL_Pipeline SHALL save the following model artifacts: dl_model.h5, tokenizer.pkl, label_encoder.pkl, and train_embeddings_normalized.npy
7. THE DL_Pipeline SHALL extract LSTM embeddings from the LSTM layer output for duplicate detection
8. THE DL_Pipeline SHALL normalize embeddings using L2 normalization before computing cosine similarity

### Requirement 4: Dataset Preparation Preservation

**User Story:** As a developer, I want the existing dataset preparation script to remain unchanged, so that I can continue using the properly configured 120k row dataset.

#### Acceptance Criteria

1. THE System SHALL NOT modify the file data/prepare_dataset.py
2. THE Dataset_Preparation SHALL continue to generate train.csv and test.csv with the current configuration
3. THE Dataset_Preparation SHALL maintain the 80/20 train-test split ratio
4. THE Dataset_Preparation SHALL maintain the duplicate generation logic and duplicate ratio of approximately 25-35%

### Requirement 5: Streamlit Application Updates

**User Story:** As an application user, I want the Streamlit app to load and use the new enhanced models, so that I can benefit from improved classification and duplicate detection.

#### Acceptance Criteria

1. THE Streamlit_App SHALL load the new model artifacts: char_vectorizer.pkl, word2vec_model.pkl, and train_word2vec_embeddings.npy
2. WHEN the Streamlit_App performs NLP prediction, THE Streamlit_App SHALL use the enhanced feature extraction including character n-grams and Word2Vec embeddings
3. THE Streamlit_App SHALL maintain backward compatibility with existing functionality including single ticket analysis, batch processing, model comparison, and about pages
4. THE Streamlit_App SHALL display predictions from both NLP and DL pipelines side-by-side
5. THE Streamlit_App SHALL show confidence scores, duplicate detection results, and category probabilities for each prediction
6. THE Streamlit_App SHALL handle preprocessing errors gracefully and display user-friendly error messages

### Requirement 6: Documentation Consolidation

**User Story:** As a new user or developer, I want consolidated documentation in a single README file, so that I can quickly understand and use the system.

#### Acceptance Criteria

1. THE Documentation SHALL consolidate information from APP_SCREENSHOTS_GUIDE.md, STREAMLIT_APP_SUMMARY.md, STREAMLIT_README.md, QUICK_START.md, and KAGGLE_SETUP.md into README.md
2. THE Documentation SHALL include the following sections: Project Overview, Features, Dataset, Models, Installation, Usage, Project Structure, Performance, Deployment, and Contributing
3. THE Documentation SHALL provide clear instructions for training models using Google Colab
4. THE Documentation SHALL provide clear instructions for deploying to Streamlit Cloud
5. THE Documentation SHALL include performance metrics tables comparing NLP and DL approaches
6. THE Documentation SHALL include setup instructions for both local development and cloud deployment
7. THE Documentation SHALL be written in clear, professional language suitable for both technical and non-technical audiences

### Requirement 7: Project Cleanup

**User Story:** As a developer, I want unused files and directories removed, so that the project structure is clean and maintainable.

#### Acceptance Criteria

1. THE System SHALL delete the following files: check_duplicates.py, preprocessing/demo_preprocessing.py, APP_SCREENSHOTS_GUIDE.md, STREAMLIT_APP_SUMMARY.md, STREAMLIT_README.md, QUICK_START.md, KAGGLE_SETUP.md, run_app.ps1, run_app.bat, restart_app.ps1, and notebooks/README_COLAB.md
2. THE System SHALL delete the following directories: nlp_module/, dl_module/, results/, and specs/
3. THE System SHALL delete the file notebooks/dl_pipeline_colab.ipynb
4. THE System SHALL preserve all files in the data/ directory including prepare_dataset.py
5. THE System SHALL preserve all files in the preprocessing/ directory except demo_preprocessing.py
6. THE System SHALL preserve all files in the models/ directory
7. WHEN cleanup is complete, THE System SHALL contain only essential files for production deployment

### Requirement 8: Deployment Configuration

**User Story:** As a DevOps engineer, I want proper deployment configuration files, so that I can deploy the application to Streamlit Cloud without issues.

#### Acceptance Criteria

1. THE Deployment_Configuration SHALL include a .streamlit/config.toml file with appropriate settings for cloud deployment
2. THE Deployment_Configuration SHALL specify theme settings, server settings, and browser settings in config.toml
3. THE System SHALL include a requirements.txt file with all necessary dependencies including xgboost, gensim, tensorflow, streamlit, scikit-learn, pandas, numpy, nltk, contractions, matplotlib, seaborn, and plotly
4. THE requirements.txt SHALL specify compatible version numbers for all dependencies
5. THE System SHALL be deployable to Streamlit Cloud without additional configuration

### Requirement 9: Model Performance Validation

**User Story:** As a quality assurance engineer, I want to validate that the new models meet performance targets, so that I can ensure the system is production-ready.

#### Acceptance Criteria

1. WHEN the NLP_Pipeline is evaluated on test data, THE NLP_Pipeline SHALL achieve classification accuracy of at least 91.33%
2. WHEN the DL_Pipeline is evaluated on test data, THE DL_Pipeline SHALL achieve classification accuracy of at least 90.05%
3. WHEN the NLP_Pipeline performs duplicate detection, THE NLP_Pipeline SHALL achieve F1-score greater than 10.31%
4. WHEN the DL_Pipeline performs duplicate detection, THE DL_Pipeline SHALL achieve F1-score greater than 50.80%
5. THE Training_Notebook SHALL display confusion matrices for both classification and duplicate detection tasks
6. THE Training_Notebook SHALL display precision, recall, and F1-score for each category
7. THE Training_Notebook SHALL include threshold tuning analysis for duplicate detection

### Requirement 10: Notebook Quality Standards

**User Story:** As a student or researcher, I want a professional, well-organized notebook, so that I can understand the workflow and use it for academic purposes.

#### Acceptance Criteria

1. THE Training_Notebook SHALL include a table of contents with jump links to each major section
2. THE Training_Notebook SHALL include time estimates for each major section
3. THE Training_Notebook SHALL use markdown headers to clearly separate sections and subsections
4. THE Training_Notebook SHALL include explanatory text before each code cell describing what the cell does
5. THE Training_Notebook SHALL include expected output descriptions after code cells
6. THE Training_Notebook SHALL use progress bars for long-running operations
7. THE Training_Notebook SHALL include visualizations for training curves, confusion matrices, and performance comparisons
8. THE Training_Notebook SHALL avoid cluttered output by suppressing verbose logs where appropriate
9. THE Training_Notebook SHALL include checkpoint saves after training each major component
10. THE Training_Notebook SHALL be suitable for academic submission and presentation

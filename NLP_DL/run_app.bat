@echo off
echo ========================================
echo  Ticket Classification System - Launcher
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please create venv first: python -m venv venv
    pause
    exit /b 1
)

REM Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if models exist
set MISSING=0
if not exist "models\tfidf_vectorizer.pkl" set MISSING=1
if not exist "models\nlp_classifier.pkl" set MISSING=1
if not exist "models\label_encoder.pkl" set MISSING=1
if not exist "models\train_tfidf_vectors.npz" set MISSING=1
if not exist "models\dl_model.h5" set MISSING=1
if not exist "models\tokenizer.pkl" set MISSING=1
if not exist "models\train_embeddings_normalized.npy" set MISSING=1

if %MISSING%==1 (
    echo.
    echo [WARNING] Some model files are missing!
    echo The app may not work correctly without all models.
    echo Press Ctrl+C to cancel or any key to continue...
    pause >nul
)

REM Launch Streamlit
echo.
echo [INFO] Launching Streamlit application...
echo The app will open in your default browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

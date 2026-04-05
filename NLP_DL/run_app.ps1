# Streamlit Application Launcher
# Run this script to start the Ticket Classification System

Write-Host "🎫 Ticket Classification System - Launcher" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create venv first: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate venv
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if models exist
$modelFiles = @(
    "models/tfidf_vectorizer.pkl",
    "models/nlp_classifier.pkl",
    "models/label_encoder.pkl",
    "models/train_tfidf_vectors.npz",
    "models/dl_model.h5",
    "models/tokenizer.pkl",
    "models/train_embeddings_normalized.npy"
)

$missingFiles = @()
foreach ($file in $modelFiles) {
    if (-Not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "⚠️  Warning: Some model files are missing:" -ForegroundColor Yellow
    foreach ($file in $missingFiles) {
        Write-Host "   - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "The app may not work correctly without all models." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to cancel or wait 5 seconds to continue..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

# Launch Streamlit
Write-Host ""
Write-Host "🚀 Launching Streamlit application..." -ForegroundColor Green
Write-Host "The app will open in your default browser at http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

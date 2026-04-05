# Restart Streamlit App with Cache Clear
Write-Host "🔄 Restarting Streamlit with cache clear..." -ForegroundColor Cyan

# Kill any existing streamlit processes
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Clear Streamlit cache
Write-Host "🧹 Clearing Streamlit cache..." -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\.streamlit\cache") {
    Remove-Item -Path "$env:USERPROFILE\.streamlit\cache" -Recurse -Force -ErrorAction SilentlyContinue
}

# Activate venv
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Start Streamlit with cache cleared
Write-Host "🚀 Starting Streamlit..." -ForegroundColor Green
streamlit run app.py --server.runOnSave true

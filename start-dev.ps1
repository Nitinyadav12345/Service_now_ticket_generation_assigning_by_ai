# Jira AI Assistant - Development Setup (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jira AI Assistant - Development Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path "Backend\.env")) {
    Write-Host "[ERROR] Backend\.env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create Backend\.env file with your credentials." -ForegroundColor Yellow
    Write-Host "See CREDENTIALS_TEMPLATE.md for details." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Quick setup:" -ForegroundColor Yellow
    Write-Host "1. Copy Backend\.env.example to Backend\.env" -ForegroundColor Yellow
    Write-Host "2. Edit Backend\.env with your Jira and LLM credentials" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/5] Starting Docker services (PostgreSQL, Redis, Qdrant)..." -ForegroundColor Green
Set-Location Backend
docker-compose -f docker-compose.simple.yml up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Docker services failed to start. Make sure Docker Desktop is running." -ForegroundColor Yellow
    Write-Host "You can continue without Docker, but some features won't work." -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
}
Set-Location ..

Write-Host ""
Write-Host "[2/5] Checking Python virtual environment..." -ForegroundColor Green
if (-not (Test-Path "Backend\venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    Set-Location Backend
    python -m venv venv
    Set-Location ..
}

Write-Host ""
Write-Host "[3/5] Installing Backend dependencies..." -ForegroundColor Green
Set-Location Backend
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet
Set-Location ..

Write-Host ""
Write-Host "[4/5] Installing Frontend dependencies..." -ForegroundColor Green
Set-Location jira-ai-frontend
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm packages (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
}
Set-Location ..

Write-Host ""
Write-Host "[5/5] Starting services..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services will start in separate windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend UI: http://localhost:4200" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop services" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to start services"

# Start Backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Backend; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start Frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd jira-ai-frontend; npm start"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Services are starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API will be ready at: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend UI will be ready at: http://localhost:4200" -ForegroundColor Green
Write-Host ""
Write-Host "Check the opened windows for startup progress." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop: Close the PowerShell windows or press Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit this window"

@echo off
echo ========================================
echo Jira AI Assistant - Development Setup
echo ========================================
echo.

REM Check if .env exists
if not exist "Backend\.env" (
    echo [ERROR] Backend\.env file not found!
    echo.
    echo Please create Backend\.env file with your credentials.
    echo See SETUP_AND_RUN_GUIDE.md for details.
    echo.
    echo Quick setup:
    echo 1. Copy Backend\.env.example to Backend\.env
    echo 2. Edit Backend\.env with your Jira and OpenAI credentials
    echo.
    pause
    exit /b 1
)

echo [1/5] Starting Docker services (PostgreSQL, Redis, Qdrant)...
cd Backend
docker-compose -f docker-compose.simple.yml up -d
if errorlevel 1 (
    echo [WARNING] Docker services failed to start. Make sure Docker Desktop is running.
    echo You can continue without Docker, but some features won't work.
    pause
)
cd ..

echo.
echo [2/5] Checking Python virtual environment...
if not exist "Backend\venv" (
    echo Creating Python virtual environment...
    cd Backend
    python -m venv venv
    cd ..
)

echo.
echo [3/5] Installing Backend dependencies...
cd Backend
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
cd ..

echo.
echo [4/5] Installing Frontend dependencies...
cd jira-ai-frontend
if not exist "node_modules" (
    echo Installing npm packages (this may take a few minutes)...
    call npm install
)
cd ..

echo.
echo [5/5] Starting services...
echo.
echo ========================================
echo Services will start in separate windows
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:4200
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each window to stop services
echo.
pause

REM Start Backend in new window
start "Jira AI - Backend API" cmd /k "cd Backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"

REM Wait a bit for backend to start
timeout /t 5 /nobreak > nul

REM Start Frontend in new window
start "Jira AI - Frontend" cmd /k "cd jira-ai-frontend && npm start"

echo.
echo ========================================
echo Services are starting...
echo ========================================
echo.
echo Backend API will be ready at: http://localhost:8000
echo Frontend UI will be ready at: http://localhost:4200
echo.
echo Check the opened windows for startup progress.
echo.
echo To stop: Close the terminal windows or press Ctrl+C
echo.
pause

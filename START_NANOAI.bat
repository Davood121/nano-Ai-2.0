@echo off
echo ========================================
echo   NanoAI 2.0 - One-Click Startup
echo ========================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Ollama is already running!
) else (
    echo Starting Ollama...
    start "Ollama Server" ollama serve
    timeout /t 3 /nobreak >nul
)

echo.
echo [2/3] Starting Backend Server...
start "NanoAI Backend" cmd /k "cd /d %~dp0 && python backend/main.py"
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Opening Frontend...
start "" "%~dp0frontend\index.html"

echo.
echo ========================================
echo   All systems launched successfully!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: Opened in browser
echo.
echo Press any key to exit this window...
pause >nul

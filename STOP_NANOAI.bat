@echo off
echo ========================================
echo   NanoAI 2.0 - Shutdown
echo ========================================
echo.

echo Stopping Backend Server...
taskkill /FI "WINDOWTITLE eq NanoAI Backend*" /F >nul 2>&1

echo Stopping Ollama...
taskkill /IM ollama.exe /F >nul 2>&1

echo.
echo All services stopped!
echo.
pause

@echo off
cd /d "%~dp0"

start "" cmd /c "python app.py"

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:5000"
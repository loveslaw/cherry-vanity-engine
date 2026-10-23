@echo off
title Cherry Vanity Engine (Python - Ultra-Fast)
cd /d "%~dp0"

echo [!] Checking Python installation...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://python.org/
    pause
    exit /b 1
)

python -m pip install -r requirements.txt --quiet
python main.py
pause

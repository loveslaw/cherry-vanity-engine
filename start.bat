@echo off
title Cherry Vanity Engine (Python - Ultra-Fast)
cd /d "%~dp0"

echo [*] Checking Python environment...

:: 1. Try 'py' launcher first (standard Windows Python launcher)
py -3 --version >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [+] Found Python Launcher (py)
    echo [*] Installing dependencies...
    py -3 -m pip install -r requirements.txt --quiet
    echo [*] Starting Vanity Engine...
    py -3 main.py
    pause
    exit /b 0
)

:: 2. Try 'python' command
python --version >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [+] Found Python
    echo [*] Installing dependencies...
    python -m pip install -r requirements.txt --quiet
    echo [*] Starting Vanity Engine...
    python main.py
    pause
    exit /b 0
)

:: 3. If neither works, guide the user
echo.
echo ====================================================================
echo [!] PYTHON NOT FOUND OR NOT IN PATH!
echo ====================================================================
echo Agar aapke PC me Python installed hai:
echo   1. Windows Search me "Manage app execution aliases" search karo
echo   2. "App Installer (python.exe)" ko OFF kar do
echo.
echo Agar Python installed nahi hai:
echo   1. https://www.python.org/downloads/ se Python download karo
echo   2. Installer me niche "[x] Add python.exe to PATH" par TICK zaroor lagana!
echo ====================================================================
echo.
pause

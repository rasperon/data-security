@echo off
echo Loading the necessary libraries.

pip install rich cryptography

if %errorlevel% neq 0 (
    echo There was an error loading libraries. Please make sure pip is installed and try again.
    pause
    exit /b %errorlevel%
)

echo Loading libraries. running cipher.py...

python cipher.py

if %errorlevel% neq 0 (
    echo An error occurred while running cipher.py. Please make sure python is installed and try again.
    pause
    exit /b %errorlevel%
)

echo Program Finished
pause

@echo off
echo ================================
echo  MAX Bot - Dependency Counseling
echo ================================
echo.
echo Starting MAX bot...
echo.

python main_max.py

if errorlevel 1 (
    echo.
    echo Error: Bot failed to start!
    echo.
    echo Please check:
    echo - Python is installed and in PATH
    echo - All dependencies are installed: pip install -r requirements.txt
    echo - .env file contains MAX_BOT_TOKEN
    echo.
    pause
)

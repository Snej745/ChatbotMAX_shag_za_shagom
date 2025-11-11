@echo off
REM MAX Dependency Counseling Bot - Docker Build Script (Windows)
REM Скрипт для сборки Docker образа

echo 🐳 Building MAX Bot Docker Image...

REM Проверка наличия .env файла
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please create .env file with BOT_TOKEN and MAX_API_BASE_URL
    exit /b 1
)

REM Сборка образа
docker build -t maxbot:latest .

if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker image built successfully!
    echo.
    echo 📊 Image details:
    docker images maxbot:latest
    echo.
    echo 🚀 To run the bot, use:
    echo    docker-compose up -d
) else (
    echo ❌ Build failed!
    exit /b 1
)

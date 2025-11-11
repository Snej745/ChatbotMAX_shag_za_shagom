#!/bin/bash

# MAX Dependency Counseling Bot - Docker Build Script
# Скрипт для сборки Docker образа

echo "🐳 Building MAX Bot Docker Image..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with BOT_TOKEN and MAX_API_BASE_URL"
    exit 1
fi

# Сборка образа
docker build -t maxbot:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "📊 Image details:"
    docker images maxbot:latest
    echo ""
    echo "🚀 To run the bot, use:"
    echo "   docker-compose up -d"
else
    echo "❌ Build failed!"
    exit 1
fi

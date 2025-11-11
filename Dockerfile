# Используем официальный Python образ
FROM python:3.11-slim

# Метаданные образа
LABEL maintainer="MAX Dependency Counseling Bot Team"
LABEL description="Telegram Dependency Counseling Bot for MAX Messenger"
LABEL version="2.0.0"

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Создаем непривилегированного пользователя для запуска приложения
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Переключаемся на непривилегированного пользователя
USER botuser

# Указываем переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Healthcheck для проверки работы бота
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('/app/bot.log') else 1)"

# Запускаем бота
CMD ["python", "main_max.py"]

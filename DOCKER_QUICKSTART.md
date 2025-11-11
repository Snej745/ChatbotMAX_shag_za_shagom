# 🚀 Быстрый запуск Docker

## За 3 минуты

### 1. Проверка Docker (30 секунд)
```bash
docker --version
docker-compose --version
```

Если не установлен:
- **Windows**: https://docs.docker.com/desktop/install/windows-install/
- **Mac**: https://docs.docker.com/desktop/install/mac-install/
- **Linux**: https://docs.docker.com/engine/install/

### 2. Создать .env файл (1 минута)
```bash
# Создайте файл .env в корне проекта
BOT_TOKEN=your_token_here
MAX_API_BASE_URL=https://platform-api.max.ru
```

### 3. Запуск (1 минута)
```bash
# Сборка образа
docker-compose build

# Запуск бота
docker-compose up -d

# Проверка логов
docker-compose logs -f
```

## ✅ Готово!

Бот запущен и работает в фоне.

---

## 📋 Основные команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Логи
docker-compose logs -f maxbot

# Статус
docker-compose ps
```

---

## 🛠️ С Makefile (Linux/Mac)

```bash
make help      # Помощь
make build     # Собрать образ
make up        # Запустить
make logs      # Логи
make down      # Остановить
make status    # Статус
```

---

## 📚 Подробная документация

Смотрите `DOCKER_README.md` для:
- Детальной настройки
- Мониторинга
- Отладки
- Production развертывания
- Troubleshooting

---

## 🐛 Проблемы?

### Ошибка: "Cannot connect to Docker daemon"
```bash
# Запустите Docker Desktop (Windows/Mac)
# или службу Docker (Linux)
sudo systemctl start docker
```

### Ошибка: ".env file not found"
```bash
# Создайте .env файл с вашим токеном
echo "BOT_TOKEN=your_token" > .env
echo "MAX_API_BASE_URL=https://platform-api.max.ru" >> .env
```

### Бот не отвечает
```bash
# Проверьте логи
docker-compose logs -f maxbot

# Проверьте статус
docker-compose ps
```

---

Удачи! 🎉

# 🐳 Docker развертывание MAX Bot

## Быстрый старт

### 1. Подготовка

Убедитесь, что у вас установлены:
- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)

Проверить версии:
```bash
docker --version
docker-compose --version
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
BOT_TOKEN=your_max_bot_token_here
MAX_API_BASE_URL=https://platform-api.max.ru
```

### 3. Сборка образа

**Linux/Mac:**
```bash
chmod +x docker-build.sh
./docker-build.sh
```

**Windows:**
```cmd
docker-build.bat
```

**Вручную:**
```bash
docker build -t maxbot:latest .
```

### 4. Запуск бота

```bash
docker-compose up -d
```

### 5. Проверка работы

```bash
# Проверить статус контейнера
docker-compose ps

# Посмотреть логи
docker-compose logs -f maxbot

# Проверить логи последних 100 строк
docker-compose logs --tail=100 maxbot
```

---

## Управление контейнером

### Запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose stop
```

### Перезапуск
```bash
docker-compose restart
```

### Остановка и удаление
```bash
docker-compose down
```

### Пересборка образа
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## Логи

### Просмотр логов в реальном времени
```bash
docker-compose logs -f maxbot
```

### Последние N строк
```bash
docker-compose logs --tail=50 maxbot
```

### Логи с временными метками
```bash
docker-compose logs -t maxbot
```

### Экспорт логов в файл
```bash
docker-compose logs maxbot > bot_logs.txt
```

---

## Мониторинг

### Статус контейнера
```bash
docker-compose ps
```

### Использование ресурсов
```bash
docker stats max-dependency-bot
```

### Информация о контейнере
```bash
docker inspect max-dependency-bot
```

### Healthcheck
```bash
docker inspect --format='{{json .State.Health}}' max-dependency-bot
```

---

## Отладка

### Зайти в контейнер
```bash
docker-compose exec maxbot /bin/bash
```

### Запустить команду в контейнере
```bash
docker-compose exec maxbot python -c "import sys; print(sys.version)"
```

### Проверить переменные окружения
```bash
docker-compose exec maxbot env
```

### Проверить файлы
```bash
docker-compose exec maxbot ls -la
```

---

## Обновление

### Обновить код и перезапустить
```bash
git pull
docker-compose build
docker-compose up -d
```

### Обновить только образ (без изменения кода)
```bash
docker-compose pull
docker-compose up -d
```

---

## Очистка

### Удалить контейнер
```bash
docker-compose down
```

### Удалить контейнер и volumes
```bash
docker-compose down -v
```

### Удалить образ
```bash
docker rmi maxbot:latest
```

### Очистить все неиспользуемые образы
```bash
docker system prune -a
```

---

## Конфигурация

### Dockerfile

Основной образ: `python:3.11-slim`

**Особенности**:
- Непривилегированный пользователь `botuser`
- Оптимизированные слои
- Healthcheck встроен
- Логи в `/app/logs`

### docker-compose.yml

**Настройки**:
- Автоматический перезапуск (`restart: unless-stopped`)
- Ограничение ресурсов (CPU: 1 core, RAM: 512MB)
- Volume для логов
- Логирование с ротацией (max 10MB × 3 файла)

---

## Переменные окружения

Можно задать в `.env` или `docker-compose.yml`:

| Переменная | Описание | Обязательная | По умолчанию |
|-----------|----------|--------------|--------------|
| `BOT_TOKEN` | Токен MAX бота | ✅ Да | - |
| `MAX_API_BASE_URL` | URL MAX API | ✅ Да | https://platform-api.max.ru |
| `LOG_LEVEL` | Уровень логирования | ❌ Нет | INFO |
| `PYTHONUNBUFFERED` | Отключить буферизацию Python | ❌ Нет | 1 |

---

## Производственное развертывание

### Docker Swarm

```bash
# Инициализировать swarm
docker swarm init

# Развернуть стек
docker stack deploy -c docker-compose.yml maxbot

# Проверить сервисы
docker service ls

# Посмотреть логи
docker service logs maxbot_maxbot
```

### Kubernetes

Для развертывания в Kubernetes создайте манифесты:

**deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: maxbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: maxbot
  template:
    metadata:
      labels:
        app: maxbot
    spec:
      containers:
      - name: maxbot
        image: maxbot:latest
        envFrom:
        - secretRef:
            name: maxbot-secrets
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "500m"
            memory: "256Mi"
```

---

## Troubleshooting

### Проблема: Контейнер не запускается

**Проверка**:
```bash
docker-compose logs maxbot
```

**Возможные причины**:
- Отсутствует `.env` файл
- Неверный токен в `.env`
- Нет доступа к MAX API

### Проблема: Бот не отвечает

**Проверка**:
```bash
# Проверить логи
docker-compose logs -f maxbot

# Проверить healthcheck
docker inspect --format='{{json .State.Health}}' max-dependency-bot
```

### Проблема: Нехватка памяти

**Решение**: Увеличить лимит в `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 1G
```

### Проблема: Образ слишком большой

**Решение**: 
1. Проверьте `.dockerignore`
2. Используйте multi-stage build
3. Очистите кэш: `docker builder prune`

---

## Best Practices

### ✅ DO:
- Используйте `.env` для секретов
- Монтируйте volume для логов
- Настройте healthcheck
- Ограничивайте ресурсы
- Используйте непривилегированного пользователя

### ❌ DON'T:
- Не храните секреты в Dockerfile
- Не запускайте от root
- Не игнорируйте логи
- Не используйте `latest` в продакшене

---

## Размер образа

```bash
# Проверить размер
docker images maxbot:latest

# Типичный размер: ~200-300MB
```

**Оптимизация**:
- Base image: `python:3.11-slim` (вместо full)
- Multi-stage build (если нужно)
- `.dockerignore` настроен
- `--no-cache-dir` для pip

---

## Безопасность

### Сканирование уязвимостей

```bash
# Docker scan (требует Docker Hub аккаунт)
docker scan maxbot:latest

# Trivy
trivy image maxbot:latest
```

### Обновление base image

```bash
# В Dockerfile обновите версию
FROM python:3.11-slim  # актуальная версия

# Пересоберите
docker-compose build --no-cache
```

---

## Мониторинг в продакшене

### Prometheus + Grafana

Добавьте экспортер метрик:
```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

### Healthcheck endpoint

Можно добавить HTTP healthcheck:
```python
# В main_max.py
from aiohttp import web

async def health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/health', health)
```

---

## Полезные команды

```bash
# Быстрый перезапуск с пересборкой
docker-compose up -d --build

# Просмотр ресурсов всех контейнеров
docker stats

# Очистка всего Docker
docker system prune -a --volumes

# Экспорт образа
docker save maxbot:latest | gzip > maxbot.tar.gz

# Импорт образа
gunzip -c maxbot.tar.gz | docker load
```

---

## Контакты и поддержка

**Docker Hub**: (если опубликован)  
**Issues**: GitHub Issues  
**Документация**: PROJECT_DOCUMENTATION.md

---

✅ Docker образ готов к использованию!

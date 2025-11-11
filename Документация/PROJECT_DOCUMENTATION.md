# Telegram Dependency Counseling Bot - Полная документация

## 📋 Оглавление

1. [Обзор проекта](#обзор-проекта)
2. [Архитектура](#архитектура)
3. [Установка и настройка](#установка-и-настройка)
4. [Структура файлов](#структура-файлов)
5. [Основные компоненты](#основные-компоненты)
6. [Conversation Flow](#conversation-flow)
7. [MAX API Integration](#max-api-integration)
8. [База данных зависимостей](#база-данных-зависимостей)
9. [Навигация и состояния](#навигация-и-состояния)
10. [Обработка ошибок](#обработка-ошибок)
11. [Развертывание](#развертывание)

---

## Обзор проекта

**Название**: Бот психологической поддержки для людей с зависимостями  
**Платформа**: MAX Messenger (Российский мессенджер от HiHub)  
**Тип**: Чат-бот для консультирования и поддержки  
**Версия**: 2.0.0  
**Python**: 3.9+  

### Цель проекта

Предоставить доступную и конфиденциальную помощь людям, столкнувшимся с различными видами зависимостей:
- Алкогольная зависимость
- Наркотическая зависимость
- Игровая зависимость
- Пищевая зависимость
- Интернет-зависимость
- Никотиновая зависимость
- Созависимость
- Любовная зависимость
- Трудоголизм
- И другие виды зависимостей

### Основные возможности

✅ **Подбор групп поддержки** - база ссылок для 25 городов России  
✅ **Консультация специалиста** - подбор по полу и возрасту  
✅ **Информационные материалы** - литература о зависимостях  
✅ **Анонимные вопросы** - возможность задать вопрос анонимно  
✅ **FAQ и вебинары** - дополнительная информация  
✅ **Полная конфиденциальность** - анонимное общение  

---

## Архитектура

### Технологический стек

```
Python 3.9+
├── python-telegram-bot 22.5  (базовые типы и структуры)
├── aiohttp 3.13.2           (HTTP клиент для MAX API)
└── python-dotenv 1.0.0      (управление конфигурацией)
```

### Паттерны проектирования

1. **Adapter Pattern** - адаптация Telegram Bot API к MAX API
2. **State Pattern** - управление состояниями диалога
3. **Proxy Pattern** - прокси для сообщений и callback запросов
4. **Strategy Pattern** - разные стратегии обработки типов обновлений

### Схема взаимодействия

```
MAX Messenger
     ↓
MAX API (platform-api.max.ru)
     ↓
MaxBot (HTTP Client)
     ↓
MaxUpdateProxy → Routing
     ↓
BotHandlers (State Machine)
     ↓
ConversationFlow (UI)
     ↓
Response → MaxBot → MAX API
```

---

## Установка и настройка

### Шаг 1: Клонирование репозитория

```bash
git clone <repository_url>
cd "Chat bot MAX"
```

### Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 3: Настройка переменных окружения

Создайте файл `.env`:

```env
BOT_TOKEN=f9LHodD0cOJb2_z16WWFRPh9OfN5JALUynWJFfMV2J-vQwGE_guoBzcpm8F7Po3Gk6hc6QvXjx36UiaABmGp
MAX_API_BASE_URL=https://platform-api.max.ru
```

### Шаг 4: Запуск бота

**Windows:**
```bash
python main_max.py
# или
run_max_bot.bat
```

**Linux/Mac:**
```bash
python3 main_max.py
```

### Проверка работы

После запуска вы должны увидеть:
```
INFO - Starting MAX Dependency Counseling Bot...
INFO - Bot started: @t38_hakaton_bot
```

---

## Структура файлов

```
Chat bot MAX/
│
├── main_max.py                 # Точка входа (MAX версия)
├── config.py                   # Конфигурация
├── requirements.txt            # Зависимости + документация
├── .env                        # Переменные окружения (не в Git)
├── .env.example                # Пример .env
│
├── bot/                        # Основной код бота
│   ├── __init__.py
│   ├── max_adapter.py          # Адаптер MAX API
│   ├── handlers.py             # Обработчики состояний
│   ├── conversation_flow.py    # Генераторы клавиатур
│   ├── dependency_links.py     # База ссылок на группы
│   ├── states.py               # Перечисление состояний
│   └── utils.py                # Утилиты (логирование)
│
├── Зависимости.txt             # Исходные данные ссылок
│
└── docs/                       # Документация (создаваемая)
    ├── PROJECT_DOCUMENTATION.md
    ├── MAX_SETUP_COMPLETE.md
    ├── QUICKSTART_MAX.md
    └── TESTING_RESULTS.md
```

---

## Основные компоненты

### 1. MaxBot (bot/max_adapter.py)

**Класс**: `MaxBot`  
**Назначение**: HTTP клиент для взаимодействия с MAX API

**Основные методы**:
```python
async def get_updates(marker: str = None, timeout: int = 30)
    # Получение обновлений с long polling
    
async def send_message(chat_id: int, text: str, reply_markup: Dict = None)
    # Отправка сообщения пользователю
    
async def edit_message(chat_id: int, message_id: int, text: str, reply_markup: Dict = None)
    # Редактирование существующего сообщения
    
async def answer_callback_query(callback_id: str)
    # Ответ на callback от inline кнопок
```

**Особенности**:
- Long polling с marker-based пагинацией
- Автоматическая retry логика при ошибках
- Timestamp фильтрация для предотвращения дубликатов
- Поддержка inline клавиатур

### 2. MaxUpdate (bot/max_adapter.py)

**Класс**: `MaxUpdate`  
**Назначение**: Представление обновления от MAX API

**Структура**:
```python
class MaxUpdate:
    update_id: int              # Уникальный ID обновления
    message: Dict               # Новое сообщение (если есть)
    callback_query: Dict        # Callback от кнопки (если есть)
    update_type: str            # Тип: message_created, message_callback, bot_started
    timestamp: int              # Временная метка
    raw_data: Dict              # Полные сырые данные
    
    @property
    def effective_user(self)    # Информация о пользователе
    
    @property
    def effective_chat(self)    # Информация о чате
```

**Типы обновлений**:
- `message_created` - новое текстовое сообщение
- `message_callback` - нажатие на inline кнопку
- `bot_started` - пользователь подключился к боту
- `bot_stopped` - пользователь отключился (игнорируется)
- `message_edited` - редактирование сообщения (игнорируется)
- `message_deleted` - удаление сообщения (игнорируется)

### 3. BotHandlers (bot/handlers.py)

**Класс**: `BotHandlers`  
**Назначение**: Обработка всех состояний диалога

**Основные методы**:
```python
async def start()                           # Приветствие
async def handle_dependency_selection()     # Выбор зависимости
async def handle_timezone_selection()       # Выбор часового пояса
async def handle_city_selection()           # Выбор города
async def handle_help_type()                # Выбор типа помощи
async def handle_gender_selection()         # Выбор пола специалиста
async def handle_age_user()                 # Возраст пользователя
async def handle_literature_choice()        # Выбор литературы
async def handle_support_choice()           # Выбор поддержки
async def handle_discovery_question()       # Вопрос об открытии проблемы
async def handle_anonymous_question()       # Анонимный вопрос
```

**Глобальные обработчики** (работают из любого состояния):
```python
back_to_dependency      # Вернуться к выбору зависимости
back_to_timezones       # Вернуться к часовым поясам
back_to_city            # Вернуться к выбору города
back_to_help            # Вернуться к выбору помощи
restart_conversation    # Начать заново
final_faq               # FAQ
final_webinars          # Вебинары
```

### 4. ConversationFlow (bot/conversation_flow.py)

**Класс**: `ConversationFlow`  
**Назначение**: Генерация клавиатур и управление данными

**Данные**:
```python
dependency_types = {
    'alcohol': 'Алкогольная зависимость',
    'drugs': 'Наркотическая зависимость',
    'gaming': 'Игровая зависимость',
    'food': 'Пищевая зависимость',
    'internet': 'Интернет-зависимость',
    'nicotine': 'Никотиновая зависимость',
    'codependency': 'Созависимость',
    'vad': 'ВСД/ПА',
    'love': 'Любовная зависимость',
    'workaholism': 'Трудоголизм',
    'vr': 'Виртуальные отношения'
}

time_zones = {
    'msk-2': 'МСК-2 (Калининград)',
    'msk': 'МСК (Москва)',
    'msk+1': 'МСК+1 (Самара)',
    # ... и т.д. (11 поясов)
}

cities_by_timezone = {
    'msk': {
        'moscow': 'Москва',
        'spb': 'Санкт-Петербург',
        # ... и т.д.
    }
    # ... всего 25 городов
}
```

**Методы генерации клавиатур**:
```python
get_dependency_keyboard()       # Клавиатура выбора зависимости
get_time_zone_keyboard()        # Клавиатура часовых поясов
get_city_keyboard(timezone)     # Клавиатура городов для пояса
get_help_type_keyboard()        # Типы помощи
get_gender_keyboard()           # Выбор пола специалиста
get_age_keyboard()              # Выбор возраста
get_literature_keyboard()       # Литература
get_support_keyboard()          # Группы/специалист
```

### 5. DependencyLinks (bot/dependency_links.py)

**Структура**: `DEPENDENCY_LINKS` - словарь с ссылками

**Формат**:
```python
DEPENDENCY_LINKS = {
    'moscow': {
        'alcohol': 'https://example.com/moscow/alcohol',
        'drugs': 'https://example.com/moscow/drugs',
        # ... все 11 типов
    },
    'spb': {
        'alcohol': 'https://example.com/spb/alcohol',
        # ... и т.д.
    }
    # ... всего 25 городов
}
```

**Функция**:
```python
def get_dependency_link(city: str, dependency: str) -> Optional[str]:
    """
    Получить ссылку на группу поддержки
    
    Args:
        city: Код города (например, 'moscow')
        dependency: Код зависимости (например, 'alcohol')
    
    Returns:
        URL ссылки или None если не найдено
    """
```

---

## Conversation Flow

### Схема диалога

```
START (bot_started / message)
   ↓
DEPENDENCY_SELECTION (выбор зависимости)
   ↓
TIME_ZONE_SELECTION (выбор часового пояса)
   ↓
CITY_SELECTION (выбор города)
   ↓
HELP_TYPE (выбор типа помощи)
   ├→ groups_selection → показать ссылки на группы
   ├→ specialist → GENDER_PREFERENCE → AGE_USER → показать специалиста
   └→ literature → LITERATURE_CHOICE → материалы
   ↓
HELP_CHOICE (группы / специалист / оба / пропустить)
   ├→ support_group → показать группы → ONLINE_OFFLINE_GROUPS
   ├→ specialist → GENDER_PREFERENCE → AGE_USER → SPECIALIST_CONSULTATION
   ├→ both → специалист → GENDER_PREFERENCE → AGE_USER → SPECIALIST_CONSULTATION
   └→ none → DISCOVERY_QUESTION
   ↓
DISCOVERY_QUESTION (готовы открыться близким?)
   ├→ yes → показать информацию → ANONYMOUS_QUESTION
   └→ no → показать информацию → ANONYMOUS_QUESTION
   ↓
ANONYMOUS_QUESTION (есть вопрос?)
   ├→ yes → ввести вопрос → TEXT_INPUT → FINAL_MENU
   └→ no → FINAL_MENU
   ↓
FINAL_MENU (FAQ / Вебинары / Начать заново)
```

### Детали состояний

#### 1. START
- **Trigger**: bot_started событие или любое сообщение от нового пользователя
- **Сообщение**: Приветствие с описанием зависимостей и целей бота
- **Кнопки**: 11 типов зависимостей
- **Следующее состояние**: DEPENDENCY_SELECTION

#### 2. DEPENDENCY_SELECTION
- **Обработчик**: `handle_dependency_selection`
- **Callback**: `dep_<type>`
- **Сохраняется**: `context.user_data['preferences']['dependency']`
- **Кнопка "Назад"**: Нет (начало диалога)
- **Следующее состояние**: TIME_ZONE_SELECTION

#### 3. TIME_ZONE_SELECTION
- **Обработчик**: `handle_timezone_selection`
- **Callback**: `timezone_<zone>`
- **Сохраняется**: `context.user_data['preferences']['timezone']`
- **Кнопка "Назад"**: `back_to_dependency`
- **Следующее состояние**: CITY_SELECTION

#### 4. CITY_SELECTION
- **Обработчик**: `handle_city_selection`
- **Callback**: `city_<city>`
- **Сохраняется**: `context.user_data['preferences']['city']`
- **Кнопка "Назад"**: `back_to_timezones`
- **Следующее состояние**: HELP_TYPE

#### 5. HELP_TYPE
- **Обработчик**: `handle_help_type`
- **Callback**: `groups_selection`, `specialist`, `literature`
- **Варианты**:
  - **Группы поддержки** → показать ссылки → возврат к HELP_TYPE
  - **Специалист** → GENDER_PREFERENCE
  - **Литература** → LITERATURE_CHOICE
- **Кнопка "Назад"**: `back_to_city`

#### 6. GENDER_PREFERENCE
- **Обработчик**: `handle_gender_selection`
- **Callback**: `gender_male`, `gender_female`, `gender_any`
- **Сохраняется**: `context.user_data['preferences']['gender']`
- **Кнопка "Назад"**: `back_from_gender` → HELP_TYPE
- **Следующее состояние**: AGE_USER

#### 7. AGE_USER
- **Обработчик**: `handle_age_user`
- **Callback**: `ageu_young`, `ageu_middle`, `ageu_senior`, `ageu_any`
- **Сохраняется**: `context.user_data['preferences']['age_user']`
- **Кнопка "Назад"**: `back_to_gender`
- **Следующее состояние**: SPECIALIST_CONSULTATION

#### 8. LITERATURE_CHOICE
- **Обработчик**: `handle_literature_choice`
- **Callback**: `lit_<topic>`, `yes_<action>`, `back_to_help`
- **Варианты литературы**:
  - Алкоголизм
  - Наркомания
  - Игромания
  - Пищевая зависимость
  - Созависимость
- **Следующее состояние**: HELP_CHOICE

#### 9. HELP_CHOICE
- **Обработчик**: `handle_support_choice`
- **Callback**: `support_group`, `specialist`, `both`, `none`
- **Варианты**:
  - Группа поддержки → ONLINE_OFFLINE_GROUPS
  - Специалист → GENDER_PREFERENCE
  - Оба варианта → GENDER_PREFERENCE
  - Пропустить → DISCOVERY_QUESTION

#### 10. DISCOVERY_QUESTION
- **Обработчик**: `handle_discovery_question`
- **Callback**: `yes_discovery`, `no_discovery`
- **Показывается**: Информация об открытии проблемы близким
- **Следующее состояние**: ANONYMOUS_QUESTION

#### 11. ANONYMOUS_QUESTION
- **Обработчик**: `handle_anonymous_question_choice`
- **Callback**: `yes_anonymous`, `no_anonymous`
- **Если "Да"**: TEXT_INPUT для ввода вопроса
- **Если "Нет"**: FINAL_MENU

#### 12. TEXT_INPUT
- **Обработчик**: `handle_text_input`
- **Тип**: Текстовое сообщение
- **Действие**: Сохранение вопроса
- **Следующее состояние**: FINAL_MENU

#### 13. FINAL_MENU
- **Обработчик**: `handle_final_faq`, `handle_final_webinars`, `handle_restart_conversation`
- **Callback**: `final_faq`, `final_webinars`, `restart_conversation`
- **Варианты**:
  - FAQ → показать часто задаваемые вопросы → возврат к FINAL_MENU
  - Вебинары → показать информацию о вебинарах → возврат к FINAL_MENU
  - Начать заново → START

---

## MAX API Integration

### Особенности MAX API

**Базовый URL**: `https://platform-api.max.ru`

**Аутентификация**: 
```python
headers = {
    'Authorization': f'{BOT_TOKEN}',
    'Content-Type': 'application/json'
}
```

### Endpoints

#### 1. GET /bot/v1/updates
Получение обновлений (long polling)

**Query Parameters**:
```
marker: str (optional) - ID последнего обновления для пагинации
timeout: int (optional) - Таймаут long polling в секундах (макс 30)
```

**Response**:
```json
{
  "updates": [
    {
      "update_id": 1762864187199,
      "update_type": "message_created",
      "timestamp": 1762864187199,
      "chat_id": 29266258,
      "user_id": 100371934,
      "message": {
        "message_id": 123456,
        "sender": {
          "user_id": 100371934,
          "first_name": "Роман",
          "last_name": "Сурмач",
          "username": null,
          "is_bot": false
        },
        "recipient": {
          "chat_id": 29266258,
          "chat_type": "dialog"
        },
        "body": {
          "text": "Привет",
          "mid": "msg_123"
        }
      }
    }
  ],
  "marker": "next_marker_string"
}
```

#### 2. POST /bot/v1/messages/send
Отправка сообщения

**Body**:
```json
{
  "chat_id": 29266258,
  "text": "Текст сообщения",
  "attachments": {
    "inline_keyboard": [
      [
        {
          "text": "Кнопка",
          "callback_data": "button_callback"
        }
      ]
    ]
  }
}
```

**Response**:
```json
{
  "message_id": 123457
}
```

#### 3. POST /bot/v1/messages/edit
Редактирование сообщения

**Body**:
```json
{
  "chat_id": 29266258,
  "message_id": 123457,
  "text": "Новый текст",
  "attachments": {
    "inline_keyboard": [...]
  }
}
```

#### 4. POST /bot/v1/callbacks/answer
Ответ на callback query

**Body**:
```json
{
  "callback_id": "callback_unique_id"
}
```

### Типы обновлений

#### message_created
Новое текстовое сообщение от пользователя

**Структура**:
```json
{
  "update_type": "message_created",
  "message": {
    "sender": {...},
    "recipient": {...},
    "body": {
      "text": "..."
    }
  }
}
```

#### message_callback
Нажатие на inline кнопку

**Структура**:
```json
{
  "update_type": "message_callback",
  "callback": {
    "callback_id": "unique_id",
    "payload": "button_callback_data",
    "user": {...}
  },
  "message": {
    "recipient": {
      "chat_id": 123
    }
  }
}
```

#### bot_started
Пользователь подключился к боту

**Структура**:
```json
{
  "update_type": "bot_started",
  "chat_id": 29266258,
  "user": {
    "user_id": 100371934,
    "first_name": "Роман",
    "last_name": "Сурмач"
  }
}
```

### Long Polling реализация

```python
class MaxBot:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url
        self.session = aiohttp.ClientSession(...)
        self.last_marker = None
        self.last_update_id = 0  # Для фильтрации дубликатов
    
    async def get_updates(self, timeout: int = 30):
        params = {'timeout': timeout}
        if self.last_marker:
            params['marker'] = self.last_marker
        
        response = await self.session.get(
            f'{self.base_url}/bot/v1/updates',
            params=params,
            timeout=aiohttp.ClientTimeout(total=timeout + 10)
        )
        
        data = await response.json()
        updates = []
        
        for update_data in data.get('updates', []):
            timestamp = update_data.get('timestamp')
            
            # Фильтрация дубликатов
            if timestamp and timestamp <= self.last_update_id:
                continue
            
            self.last_update_id = max(self.last_update_id, timestamp or 0)
            
            # Создание MaxUpdate объекта
            update = self._parse_update(update_data)
            updates.append(update)
        
        # Сохранение marker для следующего запроса
        self.last_marker = data.get('marker')
        
        return updates
```

### Обработка ошибок API

```python
try:
    response = await self.session.post(url, json=body)
    response.raise_for_status()
    return await response.json()
except aiohttp.ClientError as e:
    logger.error(f"API Error: {e}")
    # Retry logic
except asyncio.TimeoutError:
    logger.warning("API Timeout")
    # Retry logic
```

---

## База данных зависимостей

### Структура DEPENDENCY_LINKS

Полная база содержит:
- **25 городов** России
- **11 типов зависимостей**
- **275 ссылок** на группы поддержки

### Города (25)

**Европейская часть**:
- Москва (moscow)
- Санкт-Петербург (spb)
- Воронеж (voronezh)
- Краснодар (krasnodar)
- Казань (kazan)
- Самара (samara)
- Ижевск (izhevsk)
- Калининград (kaliningrad)

**Урал**:
- Екатеринбург (ekaterinburg)
- Челябинск (chelyabinsk)

**Сибирь**:
- Омск (omsk)
- Барнаул (barnaul)
- Новосибирск (novosibirsk)
- Красноярск (krasnoyarsk)
- Иркутск (irkutsk)

**Дальний Восток**:
- Улан-Удэ (ulan_ude)
- Якутск (yakutsk)
- Благовещенск (blagoveshchensk)
- Владивосток (vladivostok)
- Хабаровск (khabarovsk)
- Магадан (magadan)
- Южно-Сахалинск (yuzhno_sakhalinsk)
- Петропавловск-Камчатский (petropavlovsk)
- Анадырь (anadyr)

### Типы зависимостей (11)

1. **alcohol** - Алкогольная зависимость
2. **drugs** - Наркотическая зависимость
3. **gaming** - Игровая зависимость
4. **food** - Пищевая зависимость
5. **internet** - Интернет-зависимость
6. **nicotine** - Никотиновая зависимость
7. **codependency** - Созависимость
8. **vad** - ВСД/ПА зависимость
9. **love** - Любовная зависимость
10. **workaholism** - Трудоголизм
11. **vr** - Виртуальные отношения (None - данные появятся позже)

### Пример использования

```python
from bot.dependency_links import get_dependency_link

# Получить ссылку для Москвы и алкогольной зависимости
link = get_dependency_link('moscow', 'alcohol')
print(link)  # https://example.com/moscow/alcohol

# Проверка на None
if link:
    message = f"Ссылка: {link}"
else:
    message = "Информация появится позже"
```

---

## Навигация и состояния

### BotStates Enum

```python
class BotStates(Enum):
    DEPENDENCY_SELECTION = "dependency_selection"
    TIME_ZONE_SELECTION = "time_zone_selection"
    CITY_SELECTION = "city_selection"
    HELP_TYPE = "help_type"
    GENDER_PREFERENCE = "gender_preference"
    AGE_USER = "age_user"
    LITERATURE_CHOICE = "literature_choice"
    HELP_CHOICE = "help_choice"
    ONLINE_OFFLINE_GROUPS = "online_offline_groups"
    SPECIALIST_CONSULTATION = "specialist_consultation"
    DISCOVERY_QUESTION = "discovery_question"
    ANONYMOUS_QUESTION = "anonymous_question"
    TEXT_INPUT = "text_input"
    FINAL_MENU = "final_menu"
```

### Глобальные обработчики

Глобальные обработчики работают независимо от текущего состояния:

```python
global_handlers = {
    'continue_to_discovery': self.bot_handlers.handle_continue_to_discovery,
    'choose_support': self.bot_handlers.handle_choose_support,
    'choose_literature': self.bot_handlers.handle_choose_literature,
    'skip_both': self.bot_handlers.handle_skip_both,
    'continue_after_info': self.bot_handlers.handle_continue_after_info,
    'continue_after_literature': self.bot_handlers.handle_continue_after_literature,
    'restart_conversation': self.bot_handlers.handle_restart_conversation,
    'back_to_final': self.bot_handlers.handle_back_to_final,
    'back_to_help': self.bot_handlers.handle_back_to_help,
    'back_to_city': self.bot_handlers.back_to_city,
    'back_to_timezones': self.bot_handlers.back_to_timezones,
    'back_to_dependency': self.bot_handlers.back_to_dependency,
    'final_faq': self.bot_handlers.handle_final_faq,
    'final_webinars': self.bot_handlers.handle_final_webinars,
}
```

### Маршрутизация

```python
async def handle_callback_query(self, update, context):
    callback_data = update.callback_query.data
    user_id = update.effective_user.get('id')
    current_state = self.user_states.get(user_id)
    
    # 1. Проверка глобальных обработчиков
    if callback_data in global_handlers:
        return await global_handlers[callback_data](update, context)
    
    # 2. Маршрутизация по состоянию
    handlers_map = {
        BotStates.DEPENDENCY_SELECTION.value: self.bot_handlers.handle_dependency_selection,
        BotStates.TIME_ZONE_SELECTION.value: self.bot_handlers.handle_timezone_selection,
        # ... и т.д.
    }
    
    if current_state in handlers_map:
        handler = handlers_map[current_state]
        new_state = await handler(update, context)
        self.user_states[user_id] = new_state
```

### User Context

Структура `context.user_data`:
```python
{
    'preferences': {
        'dependency': 'alcohol',
        'timezone': 'msk',
        'city': 'moscow',
        'gender': 'any',
        'age_user': 'middle',
        'consultation_type': 'specialist',
        'sos_choice': 'support_group',
        'discovery_answer': 'yes'
    },
    'current_state': 'final_menu',
    'anonymous_question': 'Мой вопрос...'
}
```

---

## Обработка ошибок

### Уровни логирования

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Уровни**:
- `DEBUG` - детальная отладочная информация
- `INFO` - общая информация о работе
- `WARNING` - предупреждения о потенциальных проблемах
- `ERROR` - ошибки, требующие внимания
- `CRITICAL` - критические ошибки

### Try-Catch обертки

```python
async def handle_dependency_selection(self, update, context):
    try:
        query = update.callback_query
        await query.answer()
        
        # Основная логика
        # ...
        
        return BotStates.TIME_ZONE_SELECTION.value
        
    except Exception as e:
        logger.error(f"Error in handle_dependency_selection: {e}", exc_info=True)
        await query.answer("Произошла ошибка. Попробуйте снова.")
        return current_state
```

### Обработка API ошибок

```python
try:
    response = await self.bot.send_message(chat_id, text, reply_markup)
except aiohttp.ClientError as e:
    logger.error(f"Failed to send message: {e}")
    # Fallback действие
except asyncio.TimeoutError:
    logger.warning("Message send timeout")
    # Retry logic
```

### Graceful Shutdown

```python
async def run(self):
    try:
        while True:
            updates = await self.bot.get_updates(timeout=30)
            # Обработка обновлений
            
    except KeyboardInterrupt:
        logger.info("Shutting down bot...")
    finally:
        await self.bot.close()
```

---

## Развертывание

### Локальное развертывание

```bash
# 1. Клонирование
git clone <repo_url>
cd "Chat bot MAX"

# 2. Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка .env
cp .env.example .env
# Отредактировать .env с токеном

# 5. Запуск
python main_max.py
```

### Docker развертывание

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main_max.py"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./bot.log:/app/bot.log
```

**Запуск**:
```bash
docker-compose up -d
```

### Systemd сервис (Linux)

**/etc/systemd/system/maxbot.service**:
```ini
[Unit]
Description=MAX Dependency Counseling Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/maxbot
ExecStart=/opt/maxbot/venv/bin/python main_max.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Команды**:
```bash
sudo systemctl enable maxbot
sudo systemctl start maxbot
sudo systemctl status maxbot
```

### Мониторинг

**Логирование**:
```python
# bot/utils.py
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )
```

**Проверка здоровья**:
```bash
# Проверка логов
tail -f bot.log

# Проверка процесса
ps aux | grep main_max.py

# Проверка сетевых подключений
netstat -an | grep 443
```

---

## FAQ

### Как добавить новый тип зависимости?

1. Добавить в `conversation_flow.py`:
```python
dependency_types = {
    # ...
    'new_type': 'Новая зависимость'
}
```

2. Добавить ссылки в `dependency_links.py`:
```python
DEPENDENCY_LINKS = {
    'moscow': {
        # ...
        'new_type': 'https://...'
    }
}
```

### Как добавить новый город?

1. Определить часовой пояс города

2. Добавить в `conversation_flow.py`:
```python
cities_by_timezone = {
    'msk': {
        # ...
        'new_city': 'Новый Город'
    }
}
```

3. Добавить ссылки в `dependency_links.py`:
```python
DEPENDENCY_LINKS = {
    # ...
    'new_city': {
        'alcohol': 'https://...',
        # ... все типы
    }
}
```

### Как изменить текст приветствия?

Отредактировать метод `start()` в `bot/handlers.py`:
```python
async def start(self, update, context):
    welcome_message = """
    Ваш новый текст приветствия
    """
    # ...
```

### Как добавить новое состояние?

1. Добавить в `bot/states.py`:
```python
class BotStates(Enum):
    # ...
    NEW_STATE = "new_state"
```

2. Создать обработчик в `bot/handlers.py`:
```python
async def handle_new_state(self, update, context):
    # Ваша логика
    return BotStates.NEXT_STATE.value
```

3. Добавить маршрут в `main_max.py`:
```python
handlers_map = {
    # ...
    BotStates.NEW_STATE.value: self.bot_handlers.handle_new_state
}
```

---

## Контакты и поддержка

**Разработчик**: Команда поддержки зависимостей  
**MAX Bot**: @t38_hakaton_bot  
**Версия**: 2.0.0  
**Дата**: Ноябрь 2025

---

## Лицензия

Этот проект разработан для хакатона и предназначен для помощи людям с зависимостями.

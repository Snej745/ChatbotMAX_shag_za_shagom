"""
MAX Messenger API Adapter
Адаптер для работы с мессенджером MAX
"""

import logging
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MaxUpdate:
    """Represents an update from MAX API."""
    update_id: int = None  # MAX не возвращает update_id, используем timestamp
    message: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None
    update_type: Optional[str] = None
    timestamp: Optional[int] = None
    raw_data: Optional[Dict[str, Any]] = None  # Полный raw update для callback
    
    @property
    def effective_user(self):
        """Get the effective user from the update."""
        # Для bot_started событий
        if self.update_type == 'bot_started' and self.raw_data:
            user = self.raw_data.get('user', {})
            return {
                'id': user.get('user_id'),
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', ''),
                'username': user.get('username'),
                'is_bot': user.get('is_bot', False)
            }
        # Для callback queries приоритет у callback.user (не message.sender!)
        elif self.update_type == 'message_callback' and self.raw_data:
            # Для callback queries пользователь в callback.user
            callback = self.raw_data.get('callback', {})
            user = callback.get('user', {})
            return {
                'id': user.get('user_id'),
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', ''),
                'username': user.get('username'),
                'is_bot': user.get('is_bot', False)
            }
        elif self.message:
            # В MAX sender содержит информацию о пользователе
            sender = self.message.get('sender', {})
            return {
                'id': sender.get('user_id'),
                'first_name': sender.get('first_name', ''),
                'last_name': sender.get('last_name', ''),
                'username': sender.get('username'),
                'is_bot': sender.get('is_bot', False)
            }
        return None
    
    @property
    def effective_chat(self):
        """Get the effective chat from the update."""
        if self.message:
            # В MAX recipient содержит информацию о чате
            recipient = self.message.get('recipient', {})
            return {
                'id': recipient.get('chat_id'),
                'type': recipient.get('chat_type', 'dialog')
            }
        elif self.callback_query and self.callback_query.get('message'):
            return self.callback_query['message'].get('chat')
        return None


class MaxBot:
    """MAX Bot API client."""
    
    def __init__(self, token: str, base_url: str = "https://platform-api.max.ru", verify_ssl: bool = True):
        """
        Initialize MAX Bot.
        
        Args:
            token: Bot API token
            base_url: Base URL for MAX Bot API (default: https://platform-api.max.ru)
            verify_ssl: Whether to verify SSL certificates
        """
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
        self.last_update_id = 0
        self.last_marker = None  # MAX использует marker вместо offset
        self.verify_ssl = verify_ssl
        
        # Заголовки для авторизации
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
    
    def _convert_telegram_buttons_to_max(self, telegram_buttons: List[List[Dict[str, Any]]]) -> List[List[Dict[str, Any]]]:
        """
        Конвертирует кнопки из формата Telegram в формат MAX.
        
        Telegram формат:
        [{'text': 'Button', 'callback_data': 'data'}]
        
        MAX формат:
        [{'type': 'callback', 'text': 'Button', 'payload': 'data'}]
        """
        max_buttons = []
        
        for row in telegram_buttons:
            max_row = []
            for button in row:
                max_button = {
                    'type': 'callback',
                    'text': button.get('text', ''),
                    'payload': button.get('callback_data', '')
                }
                max_row.append(max_button)
            max_buttons.append(max_row)
        
        return max_buttons
        
    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(ssl=self.verify_ssl)
        self.session = aiohttp.ClientSession(connector=connector)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, data: Optional[Dict[str, Any]] = None, http_method: str = 'GET') -> Dict[str, Any]:
        """
        Make an API request to MAX.
        
        Args:
            method: API method path (e.g., '/me', '/messages')
            data: Request data
            http_method: HTTP method (GET, POST, etc.)
            
        Returns:
            API response
        """
        if not self.session:
            connector = aiohttp.TCPConnector(ssl=self.verify_ssl)
            self.session = aiohttp.ClientSession(connector=connector)
        
        url = f"{self.base_url}{method}"
        
        try:
            if http_method.upper() == 'GET':
                async with self.session.get(url, headers=self.headers, params=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"API error {response.status}: {error_text}")
                        return {}
            else:
                async with self.session.post(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"API error {response.status}: {error_text}")
                        return {}
        except Exception as e:
            logger.error(f"Request error: {e}")
            return {}
    
    async def get_updates(self, offset: Optional[int] = None, timeout: int = 30, limit: int = 100) -> List[MaxUpdate]:
        """
        Get updates from MAX API using long polling.
        
        Args:
            offset: Not used (for compatibility) - MAX uses marker
            timeout: Long polling timeout in seconds
            limit: Maximum number of updates to retrieve
            
        Returns:
            List of MaxUpdate objects
        """
        params = {
            'timeout': timeout,
            'limit': limit
        }
        
        # MAX использует marker вместо offset
        if self.last_marker is not None:
            params['marker'] = self.last_marker
        
        result = await self._make_request('/updates', params, 'GET')
        
        if not result or not isinstance(result, dict):
            return []
        
        # Сохраняем marker для следующего запроса
        if 'marker' in result:
            self.last_marker = result['marker']
        
        updates_data = result.get('updates', [])
        
        updates = []
        for update_data in updates_data:
            # Логируем структуру update для отладки
            logger.debug(f"Update data: {update_data}")
            
            # MAX возвращает другую структуру данных
            timestamp = update_data.get('timestamp')
            update_type = update_data.get('update_type')
            
            # Пропускаем уже обработанные обновления
            if timestamp and timestamp <= self.last_update_id:
                logger.debug(f"Skipping already processed update: {timestamp}")
                continue
            
            update = MaxUpdate(
                update_id=timestamp,  # Используем timestamp как уникальный ID
                message=update_data.get('message'),
                callback_query=update_data.get('message_callback'),
                update_type=update_type,
                timestamp=timestamp,
                raw_data=update_data  # Сохраняем полный raw update для callback
            )
            updates.append(update)
            
            if timestamp and timestamp > self.last_update_id:
                self.last_update_id = timestamp
        
        return updates
    
    async def send_message(self, chat_id: int, text: str, 
                          reply_markup: Optional[Dict[str, Any]] = None,
                          parse_mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message to a chat.
        
        Args:
            chat_id: Chat ID (передается как query параметр!)
            text: Message text
            reply_markup: Inline keyboard markup
            parse_mode: Parse mode (markdown, html)
            
        Returns:
            Sent message data
        """
        # Формируем тело сообщения согласно MAX API
        message_body = {
            'text': text
        }
        
        # MAX использует 'format' вместо 'parse_mode'
        if parse_mode:
            message_body['format'] = parse_mode.lower()
        
        # Добавляем inline keyboard как attachment
        if reply_markup and reply_markup.get('inline_keyboard'):
            # Конвертируем Telegram формат кнопок в MAX формат
            max_buttons = self._convert_telegram_buttons_to_max(reply_markup['inline_keyboard'])
            
            message_body['attachments'] = [{
                'type': 'inline_keyboard',
                'payload': {
                    'buttons': max_buttons
                }
            }]
        
        # MAX требует chat_id в query параметрах!
        url = f"{self.base_url}/messages"
        params = {'chat_id': chat_id}
        
        logger.info(f"Sending message to chat_id={chat_id}, text length={len(text)}, has_buttons={bool(reply_markup)}")
        
        try:
            if not self.session:
                connector = aiohttp.TCPConnector(ssl=self.verify_ssl)
                self.session = aiohttp.ClientSession(connector=connector)
            
            async with self.session.post(url, headers=self.headers, params=params, 
                                        json=message_body) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Message sent successfully, response: {result.get('message_id', 'no_id')}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Send message error {response.status}: {error_text}")
                    return {}
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return {}
    
    async def edit_message_text(self, chat_id: int, message_id: int, text: str,
                               reply_markup: Optional[Dict[str, Any]] = None,
                               parse_mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Edit an existing message.
        
        Note: MAX API не поддерживает редактирование сообщений.
        Вместо этого отправляем новое сообщение.
        
        Args:
            chat_id: Chat ID
            message_id: Message ID (игнорируется, так как нельзя редактировать)
            text: New message text
            reply_markup: New inline keyboard markup
            parse_mode: Parse mode (markdown, html)
            
        Returns:
            New message data
        """
        # MAX API не поддерживает редактирование, просто отправляем новое сообщение
        logger.info(f"MAX doesn't support message editing, sending new message instead")
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    
    async def answer_callback_query(self, callback_query_id: str, 
                                   text: Optional[str] = None,
                                   show_alert: bool = False) -> bool:
        """
        Answer a callback query.
        
        Args:
            callback_query_id: Callback query ID
            text: Notification text
            show_alert: Show as alert (not used in MAX, for compatibility)
            
        Returns:
            Success status
        """
        # В MAX для ответа на callback используется другой подход
        # Обычно достаточно просто обработать callback и отправить сообщение
        # Этот метод оставлен для совместимости
        return True
    
    async def get_me(self) -> Dict[str, Any]:
        """
        Get bot information.
        
        Returns:
            Bot information
        """
        return await self._make_request('/me', None, 'GET')
    
    def create_inline_keyboard(self, buttons: List[List[Dict[str, str]]]) -> Dict[str, Any]:
        """
        Create inline keyboard markup.
        
        Args:
            buttons: List of button rows, each containing button dicts with 'text' and 'callback_data'
            
        Returns:
            Inline keyboard markup dict
        """
        return {
            'inline_keyboard': buttons
        }


class MaxMessageProxy:
    """Proxy class to make MAX messages compatible with Telegram bot handlers."""
    
    def __init__(self, bot: MaxBot, message: Dict[str, Any]):
        self.bot = bot
        self.data = message
        
        # MAX структура: message.recipient содержит chat_id
        recipient = message.get('recipient', {})
        self.chat = {
            'id': recipient.get('chat_id'),
            'type': recipient.get('chat_type', 'dialog')
        }
        
        # MAX структура: message.sender содержит данные пользователя
        sender = message.get('sender', {})
        self.from_user = {
            'id': sender.get('user_id'),
            'first_name': sender.get('first_name', ''),
            'last_name': sender.get('last_name', ''),
            'username': sender.get('username'),
            'is_bot': sender.get('is_bot', False)
        }
        
        # MAX структура: message.body.text содержит текст
        body = message.get('body', {})
        self.text = body.get('text', '')
        self.message_id = body.get('mid')
    
    async def reply_text(self, text: str, reply_markup=None, parse_mode=None):
        """Reply to the message."""
        # Convert reply_markup if it's from Telegram format
        if reply_markup and hasattr(reply_markup, 'to_dict'):
            reply_markup = reply_markup.to_dict()
        
        return await self.bot.send_message(
            chat_id=self.chat.get('id'),
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )


class MaxCallbackQueryProxy:
    """Proxy class for MAX callback queries."""
    
    def __init__(self, bot: MaxBot, max_update: Dict[str, Any]):
        """
        Initialize callback query from MAX update structure.
        
        MAX callback structure:
        {
            "callback": {
                "timestamp": 123456,
                "callback_id": "xxx",
                "user": {"user_id": 123, "first_name": "Name", ...},
                "payload": "callback_data_here"
            },
            "message": {
                "recipient": {"chat_id": 456, ...},
                "body": {"mid": "message_id", ...},
                ...
            },
            "update_type": "message_callback"
        }
        """
        self.bot = bot
        self.data_raw = max_update
        
        # Извлекаем данные из структуры MAX
        callback = max_update.get('callback', {})
        message = max_update.get('message', {})
        
        # Callback ID для ответа
        self.id = callback.get('callback_id', '')
        
        # Данные callback (payload)
        self.data = callback.get('payload', '')
        
        # Информация о пользователе
        user = callback.get('user', {})
        self.from_user = {
            'id': user.get('user_id'),
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'username': user.get('username'),
            'is_bot': user.get('is_bot', False)
        }
        
        # Информация о сообщении
        recipient = message.get('recipient', {})
        body = message.get('body', {})
        self.message = {
            'chat': {
                'id': recipient.get('chat_id')
            },
            'message_id': body.get('mid'),
            'text': body.get('text', '')
        }
    
    async def answer(self, text: Optional[str] = None, show_alert: bool = False):
        """Answer the callback query."""
        return await self.bot.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert
        )
    
    async def edit_message_text(self, text: str, reply_markup=None, parse_mode=None):
        """Edit the message that triggered this callback query."""
        # Convert reply_markup if it's from Telegram format
        if reply_markup and hasattr(reply_markup, 'to_dict'):
            reply_markup = reply_markup.to_dict()
        
        return await self.bot.edit_message_text(
            chat_id=self.message.get('chat', {}).get('id'),
            message_id=self.message.get('message_id'),
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )


def convert_telegram_keyboard_to_max(telegram_markup) -> Dict[str, Any]:
    """
    Convert Telegram InlineKeyboardMarkup to MAX format.
    
    Args:
        telegram_markup: Telegram InlineKeyboardMarkup object
        
    Returns:
        MAX-compatible keyboard dict
    """
    if hasattr(telegram_markup, 'to_dict'):
        return telegram_markup.to_dict()
    
    return telegram_markup

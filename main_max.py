#!/usr/bin/env python3
"""
MAX Messenger Dependency Counseling Bot
Main entry point for the MAX bot application.
"""

import logging
import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import Config
from bot.conversation_flow import ConversationFlow
from bot.handlers import BotHandlers
from bot.utils import setup_logging
from bot.max_adapter import (
    MaxBot, 
    MaxUpdate, 
    MaxMessageProxy, 
    MaxCallbackQueryProxy,
    convert_telegram_keyboard_to_max
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class MaxUpdateProxy:
    """Proxy to make MAX updates compatible with Telegram handlers."""
    
    def __init__(self, max_update: MaxUpdate, bot: MaxBot):
        self.update_id = max_update.update_id
        self.bot = bot
        self._max_update = max_update
        
        # Используем свойства MaxUpdate напрямую
        self.effective_user = max_update.effective_user
        self.effective_chat = max_update.effective_chat
        
        # Create message proxy if message exists
        if max_update.message:
            self.message = MaxMessageProxy(bot, max_update.message)
        elif max_update.update_type == 'bot_started' and max_update.raw_data:
            # Для bot_started создаем "виртуальное" сообщение для отправки ответа
            # В bot_started chat_id находится прямо в raw_data, а не в recipient
            chat_id = max_update.raw_data.get('chat_id')
            user = max_update.raw_data.get('user', {})
            
            # Debug logging
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"bot_started: chat_id={chat_id}, user={user}")
            
            if chat_id:
                # Создаем минимальное сообщение для reply_text с правильной структурой MAX API
                virtual_message = {
                    'recipient': {
                        'chat_id': chat_id,
                        'chat_type': 'dialog'
                    },
                    'sender': user,
                    'body': {
                        'text': '',
                        'mid': None
                    }
                }
                self.message = MaxMessageProxy(bot, virtual_message)
            else:
                logger.warning(f"bot_started without chat_id. raw_data keys: {max_update.raw_data.keys() if max_update.raw_data else 'None'}")
                self.message = None
        else:
            self.message = None
        
        # Create callback query proxy for message_callback type
        if max_update.update_type == 'message_callback':
            # Передаем весь max_update, так как callback данные в корне update
            self.callback_query = MaxCallbackQueryProxy(bot, max_update.raw_data)
        else:
            self.callback_query = None


class MaxContextProxy:
    """Proxy to provide context similar to Telegram's ContextTypes.DEFAULT_TYPE."""
    
    def __init__(self):
        self.user_data = {}
        self.chat_data = {}
        self.bot_data = {}


class MaxBotApplication:
    """Main application for MAX bot."""
    
    def __init__(self, token: str, base_url: str = "https://platform-api.max.ru", verify_ssl: bool = True):
        self.token = token
        self.base_url = base_url
        self.bot = MaxBot(token, base_url, verify_ssl=verify_ssl)
        self.conversation_flow = ConversationFlow()
        self.bot_handlers = BotHandlers(self.conversation_flow)
        
        # Store user contexts
        self.user_contexts: Dict[int, MaxContextProxy] = {}
        
        # Store user states
        self.user_states: Dict[int, str] = {}
    
    def get_user_context(self, user_id: int) -> MaxContextProxy:
        """Get or create context for a user."""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = MaxContextProxy()
        return self.user_contexts[user_id]
    
    async def handle_message(self, update: MaxUpdateProxy, context: MaxContextProxy):
        """Handle incoming message."""
        if not update.message:
            return
        
        text = update.message.text
        user_id = update.effective_user.get('id')
        
        # If new user (no state) - automatically start conversation
        if user_id not in self.user_states:
            logger.info(f"New user {user_id} connected, automatically starting conversation")
            new_state = await self.bot_handlers.start(update, context)
            self.user_states[user_id] = new_state
            return
        
        # Handle /start command
        if text == '/start':
            new_state = await self.bot_handlers.start(update, context)
            self.user_states[user_id] = new_state
        
        # Handle /help command
        elif text == '/help':
            await self.bot_handlers.help_command(update, context)
        
        # Handle /cancel command
        elif text == '/cancel':
            await self.bot_handlers.cancel(update, context)
            if user_id in self.user_states:
                del self.user_states[user_id]
        
        # Handle /back command
        elif text == '/back':
            await self.bot_handlers.back_command(update, context)
        
        else:
            # Handle text input based on current state
            current_state = self.user_states.get(user_id)
            
            if current_state:
                await self.handle_state_message(update, context, current_state)
    
    async def handle_callback_query(self, update: MaxUpdateProxy, context: MaxContextProxy):
        """Handle callback query (button click)."""
        if not update.callback_query:
            return
        
        user_id = update.effective_user.get('id')
        current_state = self.user_states.get(user_id)
        
        if not current_state:
            await update.callback_query.answer("Сессия истекла. Начните заново с /start")
            return
        
        # Route to appropriate handler based on current state
        new_state = await self.route_callback_to_handler(update, context, current_state)
        
        if new_state:
            self.user_states[user_id] = new_state
    
    async def route_callback_to_handler(self, update: MaxUpdateProxy, 
                                       context: MaxContextProxy, 
                                       current_state: str) -> str:
        """Route callback to the appropriate handler based on state."""
        from bot.states import BotStates
        
        # Получаем callback_data
        callback_data = update.callback_query.data if update.callback_query else None
        
        # Глобальные обработчики (не зависят от состояния)
        global_handlers = {
            'continue_to_discovery': self.bot_handlers.handle_continue_to_discovery,
            'choose_support': self.bot_handlers.handle_choose_support,
            'choose_literature': self.bot_handlers.handle_choose_literature,
            'skip_both': self.bot_handlers.handle_skip_both,
            'continue_after_info': self.bot_handlers.handle_continue_after_info,
            'continue_after_literature': self.bot_handlers.handle_continue_after_literature,
            'restart_conversation': self.bot_handlers.handle_restart_conversation,
            'cancel_help': self.bot_handlers.handle_cancel_help,
            'back_to_final': self.bot_handlers.handle_back_to_final,
            'back_to_help': self.bot_handlers.handle_back_to_help,
            'back_to_city': self.bot_handlers.back_to_city,
            'back_to_timezones': self.bot_handlers.back_to_timezones,
            'back_to_dependency': self.bot_handlers.back_to_dependency,
            'final_faq': self.bot_handlers.handle_final_faq,
            'final_webinars': self.bot_handlers.handle_final_webinars,
        }
        
        # Проверяем глобальные обработчики
        if callback_data in global_handlers:
            try:
                handler = global_handlers[callback_data]
                return await handler(update, context)
            except Exception as e:
                logger.error(f"Error in global handler: {e}", exc_info=True)
                return current_state
        
        # Маршрутизация по состоянию
        handlers_map = {
            # Основные состояния выбора
            BotStates.DEPENDENCY_SELECTION.value: self.bot_handlers.handle_dependency_selection,
            BotStates.TIME_ZONE_SELECTION.value: self.bot_handlers.handle_timezone_selection,
            BotStates.CITY_SELECTION.value: self.bot_handlers.handle_city_selection,
            
            # Состояния помощи
            BotStates.HELP_TYPE.value: self.bot_handlers.handle_help_type,
            BotStates.HELP_CHOICE.value: self.bot_handlers.handle_support_choice_after_info,
            
            # Литература
            BotStates.LITERATURE_CHOICE.value: self.bot_handlers.handle_literature_choice,
            
            # Поддержка или специалист
            BotStates.SUPPORT_OR_SPECIALIST.value: self.bot_handlers.handle_support_or_specialist,
            
            # Настройки специалиста
            BotStates.GENDER_PREFERENCE.value: self.bot_handlers.handle_gender_selection,
            BotStates.AGE_USER.value: self.bot_handlers.handle_age_user,
            BotStates.AGE_SPECIALIST_PREFERENCE.value: self.bot_handlers.handle_age_specialist,
            
            # Обнаружение
            BotStates.HOW_FOUND_US.value: self.bot_handlers.handle_discovery_answer,
            
            # Анонимный вопрос
            BotStates.ANONYMOUS_QUESTION_CHOICE.value: self.bot_handlers.handle_anonymous_question_choice,
            
            # Информационные состояния
            BotStates.FAQ_ANSWERS.value: self.bot_handlers.handle_final_faq,
            BotStates.WEBINAR_SCHEDULE.value: self.bot_handlers.handle_final_webinars,
        }
        
        handler = handlers_map.get(current_state)
        
        if handler:
            try:
                return await handler(update, context)
            except Exception as e:
                logger.error(f"Error in handler: {e}", exc_info=True)
                await update.callback_query.answer("Произошла ошибка. Попробуйте снова.")
                return current_state
        
        return current_state
    
    async def handle_state_message(self, update: MaxUpdateProxy, 
                                   context: MaxContextProxy, 
                                   current_state: str):
        """Handle text messages based on current state."""
        from bot.states import BotStates
        
        # Text input handlers for specific states
        text_handlers = {
            BotStates.AGE_USER.value: self.bot_handlers.handle_age_user,
            BotStates.GROUP_NAME_INPUT.value: self.bot_handlers.handle_group_name_input,
            BotStates.PSYCHOLOGIST_NAME_INPUT.value: self.bot_handlers.handle_psychologist_name_input,
            BotStates.ANONYMOUS_QUESTION_INPUT.value: self.bot_handlers.handle_anonymous_question_input,
        }
        
        handler = text_handlers.get(current_state)
        if handler:
            try:
                user_id = update.effective_user.get('id')
                new_state = await handler(update, context)
                if new_state:
                    self.user_states[user_id] = new_state
            except Exception as e:
                logger.error(f"Error in text handler: {e}", exc_info=True)
    
    async def run(self):
        """Run the bot with long polling."""
        logger.info("Starting MAX Dependency Counseling Bot...")
        
        # Get bot info
        bot_info = await self.bot.get_me()
        if bot_info:
            logger.info(f"Bot started: @{bot_info.get('username', 'unknown')}")
        else:
            logger.error("Failed to get bot info")
            return
        
        # Start polling loop
        try:
            while True:
                try:
                    updates = await self.bot.get_updates(timeout=30)
                    
                    if updates:
                        logger.info(f"Received {len(updates)} updates")
                    
                    for max_update in updates:
                        try:
                            logger.info(f"Processing update: {max_update.update_id}, type: {max_update.update_type}")
                            
                            # Обработка события подключения пользователя к боту
                            if max_update.update_type == 'bot_started':
                                logger.info("User started bot, sending welcome message")
                                try:
                                    # Создаем прокси для отправки приветственного сообщения
                                    update = MaxUpdateProxy(max_update, self.bot)
                                    user_id = update.effective_user.get('id') if update.effective_user else None
                                    
                                    if user_id:
                                        context = self.get_user_context(user_id)
                                        # Вызываем метод start для отправки приветствия
                                        new_state = await self.bot_handlers.start(update, context)
                                        self.user_states[user_id] = new_state
                                        logger.info(f"Welcome message sent to user {user_id}")
                                    else:
                                        logger.warning("bot_started event without user_id")
                                except Exception as e:
                                    logger.error(f"Error handling bot_started: {e}", exc_info=True)
                                
                                continue
                            
                            # Обрабатываем только новые сообщения и callback'и
                            # Игнорируем message_edited, message_deleted и др.
                            if max_update.update_type not in ['message_created', 'message_callback']:
                                logger.info(f"Skipping update type: {max_update.update_type}")
                                continue
                            
                            # Create proxy update
                            update = MaxUpdateProxy(max_update, self.bot)
                            
                            # Get user context
                            user_id = update.effective_user.get('id') if update.effective_user else None
                            
                            if not user_id:
                                logger.warning("Update without user_id, skipping")
                                continue
                            
                            logger.info(f"User ID: {user_id}")
                            
                            context = self.get_user_context(user_id)
                            
                            # Handle callback query or message (callback имеет приоритет!)
                            if update.callback_query:
                                logger.info(f"Handling callback query: {update.callback_query.data}")
                                await self.handle_callback_query(update, context)
                            elif update.message:
                                logger.info(f"Handling message: {update.message.text}")
                                await self.handle_message(update, context)
                            else:
                                logger.warning("Update has no message or callback_query")
                        
                        except Exception as e:
                            logger.error(f"Error processing update: {e}", exc_info=True)
                
                except Exception as e:
                    logger.error(f"Error in polling loop: {e}", exc_info=True)
                    await asyncio.sleep(5)  # Wait before retrying
        
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        
        finally:
            if self.bot.session:
                await self.bot.session.close()


async def main():
    """Main entry point."""
    # Initialize configuration for MAX
    try:
        config = Config(messenger_type='max')
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.info("Please set MAX_BOT_TOKEN in .env file or environment variable")
        return
    
    # Create and run the bot application
    # Используем SSL проверку для официального API MAX
    app = MaxBotApplication(config.BOT_TOKEN, config.MAX_API_BASE_URL, verify_ssl=True)
    
    try:
        await app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == '__main__':
    asyncio.run(main())

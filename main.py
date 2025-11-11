#!/usr/bin/env python3
"""
Telegram Dependency Counseling Bot
Main entry point for the bot application.
"""

import logging
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from config import Config
from bot.conversation_flow import ConversationFlow
from bot.handlers import BotHandlers
from bot.utils import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Initialize configuration
    config = Config()
    
    # Create the Application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Initialize conversation flow and handlers
    conversation_flow = ConversationFlow()
    bot_handlers = BotHandlers(conversation_flow)
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_handlers.start)],
        states=bot_handlers.get_conversation_states(),
        fallbacks=[
            CommandHandler('help', bot_handlers.help_command),
            CommandHandler('cancel', bot_handlers.cancel),
            CommandHandler('back', bot_handlers.back_command),
        ],
        per_message=False,
        per_chat=True,
        per_user=True,
    )
    
    application.add_handler(conv_handler)
    
    # Add other handlers
    application.add_handler(CommandHandler('help', bot_handlers.help_command))
    
    # Run the bot
    logger.info("Starting Telegram Dependency Counseling Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
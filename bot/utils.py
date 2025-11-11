"""
Utilities module for the bot.
Contains helper functions and logging setup.
"""

import logging
import sys
from typing import Optional

def setup_logging(log_level: str = 'INFO') -> None:
    """Setup logging configuration for the bot."""
    
    # Define log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure logging
    logging.basicConfig(
        format=log_format,
        level=getattr(logging, log_level.upper()),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('telegram').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging setup complete with level: {log_level}")

def format_user_info(user) -> str:
    """Format user information for logging."""
    if not user:
        return "Unknown User"
    
    # Поддержка как объектов, так и словарей
    if isinstance(user, dict):
        username = user.get('username')
        first_name = user.get('first_name', '')
        last_name = user.get('last_name', '')
        user_id = user.get('id')
    else:
        username = getattr(user, 'username', None)
        first_name = getattr(user, 'first_name', '')
        last_name = getattr(user, 'last_name', '')
        user_id = getattr(user, 'id', None)
    
    username_str = f"@{username}" if username else "No username"
    full_name = f"{first_name} {last_name}".strip()
    
    return f"{full_name} ({username_str}, ID: {user_id})"

def sanitize_input(text: Optional[str], max_length: int = 1000) -> str:
    """Sanitize user input to prevent issues."""
    if not text:
        return ""
    
    # Remove potentially harmful characters and limit length
    sanitized = text.replace('<', '&lt;').replace('>', '&gt;')
    return sanitized[:max_length]
"""
Configuration module for the bot.
Contains all configuration settings and environment variables.
Supports both Telegram and MAX messengers.
"""

import os
from typing import Optional

class Config:
    """Configuration class for the bot."""
    
    def __init__(self, messenger_type: str = 'telegram'):
        """
        Initialize configuration.
        
        Args:
            messenger_type: Type of messenger ('telegram' or 'max')
        """
        self.MESSENGER_TYPE = messenger_type
        
        # Get token based on messenger type
        if messenger_type == 'max':
            self.BOT_TOKEN: Optional[str] = os.getenv('MAX_BOT_TOKEN')
            self.MAX_API_BASE_URL: str = os.getenv('MAX_API_BASE_URL', 'https://api.max.ru/bot')
        else:
            self.BOT_TOKEN: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
        
        self.ADMIN_IDS: list = self._parse_admin_ids()
        self.LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
        self.DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
        
        # Validate required settings
        if not self.BOT_TOKEN:
            token_name = 'MAX_BOT_TOKEN' if messenger_type == 'max' else 'TELEGRAM_BOT_TOKEN'
            raise ValueError(f"{token_name} environment variable is required")
    
    def _parse_admin_ids(self) -> list:
        """Parse admin IDs from environment variable."""
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if not admin_ids_str:
            return []
        
        try:
            return [int(admin_id.strip()) for admin_id in admin_ids_str.split(',') if admin_id.strip()]
        except ValueError:
            return []
    
    @property
    def is_admin_configured(self) -> bool:
        """Check if admin IDs are configured."""
        return len(self.ADMIN_IDS) > 0
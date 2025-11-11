"""
Bot handlers for the dependency counseling bot.
Contains all message and callback handlers.
"""

import logging
from typing import Dict, Any, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from .states import BotStates
from .conversation_flow import ConversationFlow
from .utils import format_user_info, sanitize_input

logger = logging.getLogger(__name__)

class BotHandlers:
    """Handles all bot interactions and conversation flow."""
    
    def __init__(self, conversation_flow: ConversationFlow):
        self.conversation_flow = conversation_flow
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle the /start command."""
        user = update.effective_user
        logger.info(f"User started conversation: {format_user_info(user)}")
        
        # Initialize user context
        context.user_data.clear()
        context.user_data['preferences'] = {}
        context.user_data['current_state'] = BotStates.DEPENDENCY_SELECTION.value
        
        welcome_message = """
🤝 **Добро пожаловать в бот поддержки!**

Я помогу вам получить помощь и поддержку в преодолении различных видов зависимостей.

Наша беседа конфиденциальна и анонимна. 
Вы можете в любой момент прервать разговор командой /cancel.

**Что умеет этот бот?**
✅ Определить тип зависимости
✅ Подобрать специалиста
✅ Найти группы поддержки
✅ Предоставить информацию и ресурсы
✅ Записать на консультацию

Давайте начнем! Сначала укажите, с каким видом зависимости вы столкнулись:
        """
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.conversation_flow.get_dependency_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_SELECTION.value
    
    async def handle_dependency_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle dependency type selection."""
        query = update.callback_query
        await query.answer()
        
        dependency_type = query.data.replace('dep_', '')
        context.user_data['preferences']['dependency'] = dependency_type
        
        dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'Неизвестный тип')
        
        logger.info(f"User {format_user_info(query.from_user)} selected dependency: {dependency_name}")
        
        message = f"""
✅ **Выбрано: {dependency_name}**

Теперь укажите ваш часовой пояс:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_time_preference_keyboard(page=0),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.TIME_PREFERENCE.value
        return BotStates.TIME_PREFERENCE.value
    
    async def handle_time_preference(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle time preference selection."""
        query = update.callback_query
        await query.answer()
        
        time_pref = query.data.replace('time_', '')
        context.user_data['preferences']['time'] = time_pref
        
        time_name = self.conversation_flow.time_slots.get(time_pref, 'Неизвестное время')
        
        logger.info(f"User {format_user_info(query.from_user)} selected time: {time_name}")
        
        message = f"""
✅ **Часовой пояс: {time_name}**

Какая помощь вам нужна?
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.HELP_TYPE.value
        return BotStates.HELP_TYPE.value
    
    async def handle_time_page(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle time zone page navigation."""
        query = update.callback_query
        await query.answer()
        
        page = int(query.data.replace('timepage_', ''))
        
        dependency_type = context.user_data['preferences'].get('dependency', '')
        dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'Неизвестный тип')
        
        message = f"""
✅ **Выбрано: {dependency_name}**

Теперь укажите ваш часовой пояс:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_time_preference_keyboard(page=page),
            parse_mode='Markdown'
        )
        
        return BotStates.TIME_PREFERENCE.value
    
    async def handle_help_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle help type selection."""
        query = update.callback_query
        await query.answer()
        
        help_type = query.data.replace('help_', '')
        context.user_data['preferences']['help_type'] = help_type
        
        logger.info(f"User {format_user_info(query.from_user)} selected help type: {help_type}")
        
        if help_type == 'specialist':
            message = """
👨‍⚕️ **Консультация специалиста**

Для подбора наиболее подходящего специалиста, укажите ваши предпочтения по полу:
            """
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_gender_preference_keyboard(),
                parse_mode='Markdown'
            )
            context.user_data['current_state'] = BotStates.GENDER_PREFERENCE.value
            return BotStates.GENDER_PREFERENCE.value
            
        elif help_type == 'online':
            return await self.handle_online_help(update, context)
            
        elif help_type == 'info':
            return await self.handle_info_request(update, context)
        
        return BotStates.CONVERSATION_END.value
    
    async def handle_gender_preference(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle gender preference for specialist."""
        query = update.callback_query
        await query.answer()
        
        gender_pref = query.data.replace('gender_', '')
        context.user_data['preferences']['gender'] = gender_pref
        
        message = """
👥 **Возраст специалиста**

Есть ли у вас предпочтения по возрасту специалиста?
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_age_preference_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.AGE_PREFERENCE.value
        return BotStates.AGE_PREFERENCE.value
    
    async def handle_age_preference(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle age preference for specialist."""
        query = update.callback_query  
        await query.answer()
        
        age_pref = query.data.replace('age_', '')
        context.user_data['preferences']['age'] = age_pref
        
        # Generate specialist search results
        specialist_info = self.conversation_flow.format_specialist_search(
            context.user_data['preferences']
        )
        
        # Add discovery question keyboard
        discovery_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Продолжить", callback_data="continue_discovery")]
        ])
        
        await query.edit_message_text(
            specialist_info,
            reply_markup=discovery_keyboard,
            parse_mode='Markdown'
        )
        
        return BotStates.HOW_FOUND_US.value
    
    async def handle_online_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle online help request."""
        query = update.callback_query
        
        dependency_type = context.user_data['preferences'].get('dependency', '')
        time_pref = context.user_data['preferences'].get('time', '')
        
        message = f"""
💻 **Онлайн группы поддержки**

На основе ваших предпочтений мы подберем подходящие онлайн-группы:

{self.conversation_flow.get_webinar_schedule()}

**Ваши предпочтения учтены:**
• Тип: {self.conversation_flow.dependency_types.get(dependency_type, 'Не указано')}
• Время: {self.conversation_flow.time_slots.get(time_pref, 'Гибкое')}

Администратор свяжется с вами для записи в группу.
        """
        
        discovery_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Продолжить", callback_data="continue_discovery")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=discovery_keyboard,
            parse_mode='Markdown'
        )
        
        return BotStates.HOW_FOUND_US.value
    
    async def handle_info_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle information request."""
        query = update.callback_query
        
        dependency_type = context.user_data['preferences'].get('dependency', '')
        info_text = self.conversation_flow.get_dependency_info(dependency_type)
        
        # Create keyboard with additional options
        info_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Вебинары и группы", callback_data="show_webinars")],
            [InlineKeyboardButton("Ответы на частые вопросы", callback_data="show_faq")],
            [InlineKeyboardButton("Продолжить", callback_data="continue_discovery")]
        ])
        
        await query.edit_message_text(
            info_text,
            reply_markup=info_keyboard, 
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_INFO.value
    
    async def handle_discovery_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle how user found us question."""
        query = update.callback_query
        await query.answer()
        
        message = """
📊 **Как вы о нас узнали?**

Эта информация поможет нам лучше помогать другим людям:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_discovery_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.HOW_FOUND_US.value
    
    async def handle_discovery_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle discovery source answer.""" 
        query = update.callback_query
        await query.answer()
        
        source = query.data.replace('found_', '')
        context.user_data['discovery_source'] = source
        
        source_name = self.conversation_flow.discovery_sources.get(source, 'Другое')
        
        logger.info(f"User {format_user_info(query.from_user)} found us via: {source_name}")
        
        final_message = """
✨ **Спасибо за обращение!**

Ваша заявка принята. В ближайшее время с вами свяжется наш специалист.

**Важные контакты:**
🆘 Экстренная помощь: 8-800-XXX-XX-XX
💬 Поддержка: t.me/support_chat  
📧 Email: help@support.ru

**Помните:** 
• Вы не одиноки в этой борьбе
• Обращение за помощью - это проявление силы
• Каждый день без зависимости - это победа

Вы можете начать новый разговор командой /start

*Берегите себя! 💚*
        """
        
        await query.edit_message_text(
            final_message,
            parse_mode='Markdown'
        )
        
        # Log completion
        logger.info(f"Conversation completed for user: {format_user_info(query.from_user)}")
        
        return BotStates.CONVERSATION_END.value
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command."""
        help_text = """
🤖 **Помощь по использованию бота**

**Команды:**
/start - Начать новый разговор
/back - Вернуться на шаг назад
/help - Показать эту справку
/cancel - Отменить текущий разговор

**Что я умею:**
• Помочь определить тип зависимости
• Подобрать специалиста по вашим критериям  
• Найти подходящие группы поддержки
• Предоставить информацию о зависимостях
• Записать на консультацию или вебинар

**Навигация:**
• Используйте кнопки ⬅️ "Назад" в меню
• Или команду /back для возврата на предыдущий шаг

**Конфиденциальность:**
Все разговоры анонимны и конфиденциальны.
Ваши данные не передаются третьим лицам.

**Экстренная помощь:**
📞 8-800-XXX-XX-XX (круглосуточно)
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle conversation cancellation."""
        user = update.effective_user
        logger.info(f"User {format_user_info(user)} cancelled conversation")
        
        await update.message.reply_text(
            "Разговор отменен. Вы можете начать заново командой /start\n"
            "При необходимости экстренной помощи: 8-800-XXX-XX-XX",
            parse_mode='Markdown'
        )
        
        context.user_data.clear()
        return -1
    
    async def back_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle /back command to go to previous step."""
        user = update.effective_user
        
        # Get current state from context
        if 'current_state' not in context.user_data:
            await update.message.reply_text(
                "Нет предыдущего шага. Начните диалог с команды /start",
                parse_mode='Markdown'
            )
            return -1
        
        current_state = context.user_data.get('current_state')
        logger.info(f"User {format_user_info(user)} used /back from state: {current_state}")
        
        # Determine which state to go back to based on current state
        if current_state == BotStates.TIME_PREFERENCE.value:
            return await self._back_to_dependency_from_command(update, context)
        elif current_state == BotStates.HELP_TYPE.value:
            return await self._back_to_time_from_command(update, context)
        elif current_state == BotStates.GENDER_PREFERENCE.value:
            return await self._back_to_help_from_command(update, context)
        elif current_state == BotStates.AGE_PREFERENCE.value:
            return await self._back_to_gender_from_command(update, context)
        elif current_state in [BotStates.HOW_FOUND_US.value, BotStates.DEPENDENCY_INFO.value]:
            return await self._back_to_help_from_command(update, context)
        else:
            await update.message.reply_text(
                "Нет предыдущего шага. Используйте кнопки для навигации или /start для начала.",
                parse_mode='Markdown'
            )
            return current_state
    
    async def _back_to_dependency_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to dependency selection from command."""
        message = """
🤝 **Выбор типа зависимости**

Укажите, с каким видом зависимости вы столкнулись:
        """
        
        await update.message.reply_text(
            message,
            reply_markup=self.conversation_flow.get_dependency_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.DEPENDENCY_SELECTION.value
        return BotStates.DEPENDENCY_SELECTION.value
    
    async def _back_to_time_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to time preference from command."""
        dependency_type = context.user_data['preferences'].get('dependency', '')
        dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'Неизвестный тип')
        
        message = f"""
✅ **Выбрано: {dependency_name}**

Теперь укажите ваш часовой пояс:
        """
        
        await update.message.reply_text(
            message,
            reply_markup=self.conversation_flow.get_time_preference_keyboard(page=0),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.TIME_PREFERENCE.value
        return BotStates.TIME_PREFERENCE.value
    
    async def _back_to_help_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to help type from command."""
        time_pref = context.user_data['preferences'].get('time', '')
        time_name = self.conversation_flow.time_slots.get(time_pref, 'Неизвестный часовой пояс')
        
        message = f"""
✅ **Часовой пояс: {time_name}**

Какая помощь вам нужна?
        """
        
        await update.message.reply_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.HELP_TYPE.value
        return BotStates.HELP_TYPE.value
    
    async def _back_to_gender_from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to gender preference from command."""
        message = """
👨‍⚕️ **Консультация специалиста**

Для подбора наиболее подходящего специалиста, укажите ваши предпочтения по полу:
        """
        
        await update.message.reply_text(
            message,
            reply_markup=self.conversation_flow.get_gender_preference_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.GENDER_PREFERENCE.value
        return BotStates.GENDER_PREFERENCE.value
    
    async def back_to_dependency(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to dependency selection."""
        query = update.callback_query
        await query.answer()
        
        message = """
🤝 **Выбор типа зависимости**

Укажите, с каким видом зависимости вы столкнулись:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_dependency_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_SELECTION.value
    
    async def back_to_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to time preference selection."""
        query = update.callback_query
        await query.answer()
        
        dependency_type = context.user_data['preferences'].get('dependency', '')
        dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'Неизвестный тип')
        
        message = f"""
✅ **Выбрано: {dependency_name}**

Теперь укажите ваш часовой пояс:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_time_preference_keyboard(page=0),
            parse_mode='Markdown'
        )
        
        return BotStates.TIME_PREFERENCE.value
    
    async def back_to_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to help type selection."""
        query = update.callback_query
        await query.answer()
        
        time_pref = context.user_data['preferences'].get('time', '')
        time_name = self.conversation_flow.time_slots.get(time_pref, 'Неизвестный часовой пояс')
        
        message = f"""
✅ **Часовой пояс: {time_name}**

Какая помощь вам нужна?
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.HELP_TYPE.value
    
    async def back_to_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to gender preference selection."""
        query = update.callback_query
        await query.answer()
        
        message = """
👨‍⚕️ **Консультация специалиста**

Для подбора наиболее подходящего специалиста, укажите ваши предпочтения по полу:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_gender_preference_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.GENDER_PREFERENCE.value
    
    def get_conversation_states(self) -> Dict[str, list]:
        """Get conversation states mapping for ConversationHandler."""
        return {
            BotStates.DEPENDENCY_SELECTION.value: [
                CallbackQueryHandler(self.handle_dependency_selection, pattern='^dep_')
            ],
            BotStates.TIME_PREFERENCE.value: [
                CallbackQueryHandler(self.back_to_dependency, pattern='^back_to_dependency'),
                CallbackQueryHandler(self.handle_time_page, pattern='^timepage_'),
                CallbackQueryHandler(self.handle_time_preference, pattern='^time_')
            ],
            BotStates.HELP_TYPE.value: [
                CallbackQueryHandler(self.back_to_time, pattern='^back_to_time'),
                CallbackQueryHandler(self.handle_help_type, pattern='^help_')
            ],
            BotStates.GENDER_PREFERENCE.value: [
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_help'),
                CallbackQueryHandler(self.handle_gender_preference, pattern='^gender_')
            ],
            BotStates.AGE_PREFERENCE.value: [
                CallbackQueryHandler(self.back_to_gender, pattern='^back_to_gender'),
                CallbackQueryHandler(self.handle_age_preference, pattern='^age_')
            ],
            BotStates.DEPENDENCY_INFO.value: [
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_info'),
                CallbackQueryHandler(self.handle_discovery_question, pattern='^continue_discovery'),
                CallbackQueryHandler(self.handle_webinar_info, pattern='^show_webinars'),
                CallbackQueryHandler(self.handle_faq, pattern='^show_faq')
            ],
            BotStates.HOW_FOUND_US.value: [
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_previous'),
                CallbackQueryHandler(self.handle_discovery_question, pattern='^continue_discovery'),
                CallbackQueryHandler(self.handle_discovery_answer, pattern='^found_')
            ]
        }
    
    async def handle_webinar_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle webinar information request."""
        query = update.callback_query
        await query.answer()
        
        webinar_info = self.conversation_flow.get_webinar_schedule()
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="back_to_info")],
            [InlineKeyboardButton("Продолжить", callback_data="continue_discovery")]
        ])
        
        await query.edit_message_text(
            webinar_info,
            reply_markup=back_keyboard,
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_INFO.value
    
    async def handle_faq(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle FAQ request."""
        query = update.callback_query
        await query.answer()
        
        faq_text = """
❓ **Часто задаваемые вопросы**

**Q: Сколько стоят консультации?**
A: Первая консультация бесплатная. Дальнейшие - по доступным тарифам.

**Q: Гарантируете ли вы анонимность?**  
A: Да, полная анонимность и конфиденциальность гарантированы.

**Q: Можно ли получить помощь онлайн?**
A: Да, доступны онлайн-консультации и группы поддержки.

**Q: Как быстро можно попасть к специалисту?**
A: Обычно в течение 24-48 часов после заявки.

**Q: Что если я сорвусь во время лечения?**
A: Срывы - это часть процесса выздоровления. Мы поможем вернуться на путь.

**Q: Помогаете ли вы семьям зависимых?**
A: Да, у нас есть специальные программы для созависимых.
        """
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="back_to_info")],
            [InlineKeyboardButton("Продолжить", callback_data="continue_discovery")]
        ])
        
        await query.edit_message_text(
            faq_text,
            reply_markup=back_keyboard,
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_INFO.value
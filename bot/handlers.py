"""
Bot handlers for the dependency counseling bot.
Contains all message and callback handlers.
NEW VERSION - Complete restructure based on new flow
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
from .dependency_links import get_dependency_link

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
🤝 **Добро пожаловать!**

Зависимости — это проблема, которая затрагивает миллионы людей по всему миру. Будь то алкоголь, наркотики, игры, еда или другие виды зависимостей — это не приговор, и выход есть всегда.

Мы понимаем, как сложно бывает сделать первый шаг, и мы здесь, чтобы помочь вам на этом пути. Наша цель — предоставить вам поддержку, информацию и ресурсы для преодоления зависимости.

✨ **Что я могу для вас сделать:**
• Подобрать группу поддержки в вашем городе
• Помочь найти специалиста
• Предоставить информационные материалы
• Ответить на вопросы о зависимостях

🔒 Наша беседа полностью конфиденциальна и анонимна.

Давайте начнем! Укажите вид зависимости:
        """
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.conversation_flow.get_dependency_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.DEPENDENCY_SELECTION.value
    
    # ==================== 1. DEPENDENCY SELECTION ====================
    
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
            reply_markup=self.conversation_flow.get_time_zone_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.TIME_ZONE_SELECTION.value
        return BotStates.TIME_ZONE_SELECTION.value
    
    # ==================== 2. TIME ZONE AND CITY SELECTION ====================
    
    async def handle_timezone_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle time zone selection (first step)."""
        query = update.callback_query
        await query.answer()
        
        timezone = query.data.replace('timezone_', '')
        context.user_data['preferences']['timezone'] = timezone
        
        timezone_name = self.conversation_flow.time_zones.get(timezone, 'Неизвестный часовой пояс')
        
        logger.info(f"User {format_user_info(query.from_user)} selected time zone: {timezone_name}")
        
        message = f"""
✅ **Часовой пояс: {timezone_name}**

Выберите город:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_city_keyboard(timezone),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.CITY_SELECTION.value
        return BotStates.CITY_SELECTION.value
    
    async def handle_city_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle city selection (second step)."""
        query = update.callback_query
        await query.answer()
        
        city = query.data.replace('city_', '')
        context.user_data['preferences']['city'] = city
        
        city_name = self.conversation_flow.get_city_name(city)
        
        logger.info(f"User {format_user_info(query.from_user)} selected city: {city_name}")
        
        message = f"""
✅ **Город: {city_name}**

Какая помощь необходима?
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.HELP_TYPE.value
        return BotStates.HELP_TYPE.value
    
    async def back_to_timezones(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to time zone selection."""
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
            reply_markup=self.conversation_flow.get_time_zone_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.TIME_ZONE_SELECTION.value
    
    # ==================== 3. HELP TYPE SELECTION ====================
    
    async def handle_help_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle help type selection."""
        query = update.callback_query
        await query.answer()
        
        help_type = query.data.replace('help_', '')
        context.user_data['preferences']['help_type'] = help_type
        
        logger.info(f"User {format_user_info(query.from_user)} selected help type: {help_type}")
        
        if help_type == 'info':
            # Show both questions at once
            message = """
📋 Выберите интересующие вас варианты:

1️⃣ Хотите ли подобрать группу поддержки/специалиста для помощи?

2️⃣ Хотите ли ознакомиться с литературой о вашей зависимости?
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👥 Группа поддержки/Специалист", callback_data="choose_support")],
                [InlineKeyboardButton("📚 Литература", callback_data="choose_literature")],
                [InlineKeyboardButton("⏭️ Пропустить оба", callback_data="skip_both")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_help")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard
            )
            
            context.user_data['current_state'] = BotStates.HELP_CHOICE.value
            return BotStates.HELP_CHOICE.value

            
        elif help_type == 'groups_selection':
            # Подбор онлайн/офлайн-групп
            dependency_type = context.user_data['preferences'].get('dependency', '')
            dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'выбранной зависимости')
            city = context.user_data['preferences'].get('city', '')
            city_name = self.conversation_flow.get_city_name(city) if city else 'вашем городе'
            
            # Получаем ссылку для конкретной зависимости и города
            link = get_dependency_link(city, dependency_type)
            
            if link:
                link_text = f"🔗 Ссылка: {link}"
            elif dependency_type == 'vr':
                link_text = "(информация появится позже)"
            else:
                link_text = "(ссылка недоступна для этого города)"
            
            message = f"""
👥 **Подбор онлайн/офлайн-групп**

📍 Город: {city_name}
🎯 Зависимость: {dependency_name}

{link_text}
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад к выбору помощи", callback_data="back_to_help")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard
            )
            
            context.user_data['current_state'] = BotStates.HELP_TYPE.value
            return BotStates.HELP_TYPE.value
            
        elif help_type == 'specialist':
            # Консультация специалиста - начинаем с выбора пола
            message = """
👨‍⚕️ **Консультация специалиста**

Укажите ваш пол:
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_gender_keyboard(),
                parse_mode='Markdown'
            )
            
            context.user_data['preferences']['consultation_type'] = 'specialist'
            context.user_data['current_state'] = BotStates.GENDER_PREFERENCE.value
            return BotStates.GENDER_PREFERENCE.value
            
        elif help_type == 'faq':
            # Ответы на популярные вопросы
            message = """
❓ Ответы на популярные вопросы

Q: Вредно ли опохмеляться?
A: Да, опохмеление лишь усугубляет пагубное воздействие на организм

Q: Алкоголь является фактором риска развития онкологических заболеваний?
A: Да, этанол, содержащийся в любом спиртном напитке, повышает вероятность возникновения онкологических заболеваний.

Q: Могу ли я сам, своей силой воли, избавиться от зависимости?
A: Если стадия лёгкая, попробовать можно, но при более тяжёлой степени зависимости без посторонние помощи и поддержки вы не справитесь

Q: Без чего (кого) не справиться с зависимостью?
A: Полноценно справиться с зависимостью поможет правильный подход, основанный на программе 12 шагов, поддержка со стороны и если требуется, обращение за медикаментозным лечением в клинике
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад к выбору помощи", callback_data="back_to_help")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard
            )
            
            context.user_data['current_state'] = BotStates.HELP_TYPE.value
            return BotStates.HELP_TYPE.value
            
        elif help_type == 'webinars':
            # Расписание вебинаров спикеров
            message = """
📅 Расписание вебинаров спикеров

Ближайшие вебинары будут указаны позже.

Мы работаем над формированием расписания интересных и полезных вебинаров с опытными спикерами в области зависимостей и восстановления.

Следите за обновлениями!
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад к выбору помощи", callback_data="back_to_help")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard
            )
            
            context.user_data['current_state'] = BotStates.HELP_TYPE.value
            return BotStates.HELP_TYPE.value

    async def ask_how_found_us(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Ask how the user found us."""
        query = update.callback_query
        
        message = """
❓ **Как вы о нас узнали?**

Пожалуйста, выберите вариант:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_discovery_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.HOW_FOUND_US.value
        return BotStates.HOW_FOUND_US.value
    
    def get_dependency_info(self, dependency_type: str) -> str:
        """Get brief information about dependency type."""
        info_map = {
            'alcohol': 'Алкогольная зависимость - хроническое заболевание, характеризующееся потерей контроля над употреблением алкоголя.',
            'drugs': 'Наркотическая зависимость - серьезное заболевание, требующее профессиональной помощи и поддержки.',
            'gaming': 'Игровая зависимость (Лудомания) - навязчивое стремление к азартным играм.',
            'food': 'Пищевая зависимость (РПП) - расстройство пищевого поведения, требующее комплексного подхода.',
            'internet': 'Интернет-зависимость - чрезмерное использование интернета, мешающее нормальной жизни.',
            'nicotine': 'Никотиновая зависимость - физическая и психологическая зависимость от никотина.',
            'codependency': 'Созависимость - чрезмерная эмоциональная зависимость от другого человека.',
            'vad': 'ВАД - взрослые дети алкоголиков, имеющие особые психологические особенности.',
            'love': 'Любовная зависимость - навязчивая потребность в отношениях и одобрении партнера.',
            'workaholism': 'Трудоголизм - компульсивная потребность в постоянной работе.',
            'vr': 'ВР (Взрослый ребёнок) - паттерны поведения из детства, влияющие на взрослую жизнь.'
        }
        return info_map.get(dependency_type, 'Информация о данном типе зависимости.')
    
    async def handle_back_to_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle back to help type selection."""
        query = update.callback_query
        await query.answer()
        
        logger.info(f"Back to help - user_data: {context.user_data.get('preferences', {})}")
        
        time_pref = context.user_data.get('preferences', {}).get('timezone', '')
        time_name = self.conversation_flow.time_zones.get(time_pref, 'Неизвестный часовой пояс')
        
        message = f"✅ Часовой пояс: {time_name}\n\nКакая помощь вам нужна?"
        
        logger.info(f"Sending back_to_help message to user")
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard()
        )
        
        logger.info(f"Back to help message sent successfully")
        
        return BotStates.HELP_TYPE.value
    
    # ==================== 4. AFTER INFO - SUPPORT CHOICE ====================
    
    async def handle_choose_support(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle when user chooses support/specialist option."""
        query = update.callback_query
        await query.answer()
        
        context.user_data['preferences']['wants_support'] = True
        
        # Show support menu
        message = """
Выберите, что вам нужно:

Консультация психолога
Группа поддержки
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Консультация психолога", callback_data="sos_specialist")],
            [InlineKeyboardButton("Группа поддержки", callback_data="sos_support_group")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_help")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        context.user_data['current_state'] = BotStates.SUPPORT_OR_SPECIALIST.value
        return BotStates.SUPPORT_OR_SPECIALIST.value
    
    async def handle_choose_literature(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle when user chooses literature option."""
        query = update.callback_query
        await query.answer()
        
        context.user_data['preferences']['wants_literature'] = True
        
        # Show literature options
        message = """
📚 Доступная литература:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_literature_keyboard()
        )
        
        context.user_data['current_state'] = BotStates.LITERATURE_CHOICE.value
        return BotStates.LITERATURE_CHOICE.value
    
    async def handle_skip_both(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle when user skips both support and literature."""
        query = update.callback_query
        await query.answer()
        
        context.user_data['preferences']['wants_support'] = False
        context.user_data['preferences']['wants_literature'] = False
        
        # Go directly to discovery question
        return await self.show_discovery_question(query, context)
    
    async def handle_continue_after_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle continue button after seeing dependency info."""
        query = update.callback_query
        await query.answer()
        
        message = """
💡 Хотите ли подобрать группу поддержки/специалиста для помощи?
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Да", callback_data="yes_support_after_info")],
            [InlineKeyboardButton("Нет", callback_data="no_support_after_info")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        context.user_data['current_state'] = BotStates.HELP_CHOICE.value
        return BotStates.HELP_CHOICE.value
    
    async def handle_support_choice_after_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle yes/no choice for support after seeing info."""
        query = update.callback_query
        await query.answer()
        
        # Save the support preference
        if query.data == "yes_support_after_info":
            context.user_data['preferences']['wants_support'] = True
        else:  # no_support_after_info
            context.user_data['preferences']['wants_support'] = False
        
        # Always show literature question after support question (regardless of answer)
        message = """
📖 Хотите ли ознакомиться с литературой о вашей зависимости?
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Да", callback_data="yes_literature_after_info")],
            [InlineKeyboardButton("Нет", callback_data="no_literature_after_info")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        context.user_data['current_state'] = BotStates.LITERATURE_CHOICE.value
        return BotStates.LITERATURE_CHOICE.value
    
    # ==================== 5. LITERATURE CHOICE ====================
    
    async def handle_literature_choice_after_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle literature choice after information section - routes based on both saved choices."""
        query = update.callback_query
        await query.answer()
        
        # Save literature preference
        wants_literature = query.data == "yes_literature_after_info"
        context.user_data['preferences']['wants_literature'] = wants_literature
        
        # Get the previously saved support preference
        wants_support = context.user_data['preferences'].get('wants_support', False)
        
        # Route based on combined preferences per flowchart
        if wants_support:
            # User wants support/specialist - show support menu
            message = """
Выберите, что вам нужно:

Консультация психолога
Группа поддержки
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Консультация психолога", callback_data="sos_specialist")],
                [InlineKeyboardButton("Группа поддержки", callback_data="sos_support_group")],
                [InlineKeyboardButton("Назад", callback_data="back_to_help")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard
            )
            
            context.user_data['current_state'] = BotStates.SUPPORT_OR_SPECIALIST.value
            return BotStates.SUPPORT_OR_SPECIALIST.value
            
        elif wants_literature:
            # User wants literature but not support - show literature options
            message = """
📚 Доступная литература:
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_literature_keyboard()
            )
            
            return BotStates.LITERATURE_CHOICE.value
            
        else:
            # User doesn't want either - proceed to discovery question
            return await self.show_discovery_question(query, context)
    
    async def handle_literature_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle yes/no choice for literature."""
        query = update.callback_query
        await query.answer()
        
        # Handle literature selection (after showing the menu)
        if query.data.startswith('lit_'):
            return await self.handle_literature_selection(update, context)
        
        # Handle back button
        if query.data == 'back_to_help':
            return await self.handle_back_to_help(update, context)
        
        if query.data.startswith('yes_'):
            # Show literature options
            message = """
📚 **Доступная литература:**
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_literature_keyboard(),
                parse_mode='Markdown'
            )
            
            return BotStates.LITERATURE_CHOICE.value
        else:
            # Skip to discovery question
            return await self.show_discovery_question(query, context)
    
    async def handle_literature_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle literature selection."""
        query = update.callback_query
        await query.answer()
        
        # Handle back button - should be handled by global handler
        if query.data == 'back_to_help':
            return await self.handle_back_to_help(update, context)
        
        # Handle literature selection
        if not query.data.startswith('lit_'):
            logger.warning(f"Unexpected callback in literature selection: {query.data}")
            return BotStates.LITERATURE_CHOICE.value
        
        lit_type = query.data.replace('lit_', '')
        lit_name = self.conversation_flow.literature_options.get(lit_type, 'Выбранная литература')
        
        context.user_data['preferences']['literature'] = lit_type
        
        logger.info(f"User {format_user_info(query.from_user)} selected literature: {lit_name}")
        
        # Prepare message based on literature type
        if lit_type == '12steps':
            message = f"""
📖 **{lit_name}**

Ваш выбор зафиксирован.

📚 Читать онлайн:
https://docviewer.yandex.ru/view/1191821593/?page=2&*=YXDoR1EHiuwHHMWxXmEyErA3lal7InVybCI6Imh0dHBzOi8vYWFydXMucnUvcGRmL3R3ZWx2ZVN0ZXBzdHdlbHZlVHJhZGl0aW9ucy5wZGYiLCJ0aXRsZSI6InR3ZWx2ZVN0ZXBzdHdlbHZlVHJhZGl0aW9ucy5wZGYiLCJub2lmcmFtZSI6dHJ1ZSwidWlkIjoiMTE5MTgyMTU5MyIsInRzIjoxNzYwNTIzMzUzMDE0LCJ5dSI6IjkxNTE5OTIzNzE3NTQwODQ0MzYiLCJzZXJwUGFyYW1zIjoidG09MTc2MDUyMzM0OCZ0bGQ9cnUmbGFuZz1ydSZuYW1lPXR3ZWx2ZVN0ZXBzdHdlbHZlVHJhZGl0aW9ucy5wZGYmdGV4dD0xMislRDElODglRDAlQjAlRDAlQjMlRDAlQkUlRDAlQjIrJUQwJUIwJUQwJUJEJUQwJUJFJUQwJUJEJUQwJUI4JUQwJUJDJUQwJUJEJUQxJThCJUQxJTg1KyVEMCVCMCVEMCVCQiVEMCVCQSVEMCVCRSVEMCVCMyVEMCVCRSVEMCVCQiVEMCVCOCVEMCVCQSVEMCVCRSVEMCVCMiZ1cmw9aHR0cHMlM0EvL2FhcnVzLnJ1L3BkZi90d2VsdmVTdGVwc3R3ZWx2ZVRyYWRpdGlvbnMucGRmJmxyPTM1Jm1pbWU9cGRmJmwxMG49cnUmdHlwZT10b3VjaCZzaWduPTg1MmRkMGY1ZmU5OTc3ODgyZjVhM2U5OTdkNGM1OWU3JmtleW5vPTAifQ%3D%3D&lang=ru

🛒 Купить книгу:
https://www.wildberries.ru/catalog/505858500/detail.aspx?size=702083937
            """
        elif lit_type == 'new_glasses':
            message = f"""
📖 **{lit_name}**

Ваш выбор зафиксирован.

📚 Читать онлайн:
https://docviewer.yandex.ru/view/1191821593/?*=Vsa9UIVG5n0LknyEWvSdE6vEIAp7InVybCI6Imh0dHBzOi8vYWEtYm9vay5uZXQvbG9hZHMvbm92aWVfb2hraS5wZGYiLCJ0aXRsZSI6Im5vdmllX29oa2kucGRmIiwibm9pZnJhbWUiOnRydWUsInVpZCI6IjExOTE4MjE1OTMiLCJ0cyI6MTc2MDUyMzQ1NDYwOSwieXUiOiI5MTUxOTkyMzcxNzU0MDg0NDM2Iiwic2VycFBhcmFtcyI6InRtPTE3NjA1MjMzODQmdGxkPXJ1Jmxhbmc9cnUmbmFtZT1ub3ZpZV9vaGtpLnBkZiZ0ZXh0PSVEMCVCMCVEMCVCRCVEMCVCRSVEMCVCRCVEMCVCOCVEMCVCQyVEMCVCRCVEMSU4QiVEMCVCNSslRDAlQjAlRDAlQkIlRDAlQkElRDAlQkUlRDAlQjMlRDAlQkUlRDAlQkIlRDAlQjglRDAlQkElRDAlQjgrJUQxJTg3JUQwJUIwJUQwJUJBKyVEMSU4NyslRDAlQkQlRDAlQkUlRDAlQjIlRDElOEIlRDAlQjUrJUQwJUJFJUQxJTg3JUQwJUJBJUQwJUI4JnVybD1odHRwcyUzQS8vYWEtYm9vay5uZXQvbG9hZHMvbm92aWVfb2hraS5wZGYmbHI9MzUmbWltZT1wZGYmbDEwbj1ydSZ0eXBlPXRvdWNoJnNpZ249MmEyNjhiMGQ0OWJiNDU5ZGQ3Mjg2ODk0ZGFhYTcwMDAma2V5bm89MCJ9&lang=ru

🛒 Купить книгу:
https://ozon.ru/t/LtWbt2m
            """
        else:
            message = f"""
📖 **{lit_name}**

Ваш выбор зафиксирован. Ссылка на литературу будет отправлена вам администратором.
            """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Продолжить", callback_data="continue_after_literature")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        return BotStates.LITERATURE_CHOICE.value
    
    async def handle_continue_after_literature(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle continue button after literature selection."""
        query = update.callback_query
        await query.answer()
        
        # Переход к вопросу "Как вы о нас узнали?"
        return await self.ask_how_found_us(update, context)
    
    def get_literature_info(self, lit_type: str) -> str:
        """Get information about selected literature."""
        lit_info = {
            '12steps': 'Основополагающая книга программы 12 шагов. Содержит описание всех двенадцати шагов и двенадцати традиций, помогающих в выздоровлении от зависимости.',
            'new_glasses': 'Книга о взрослении и преодолении паттернов поведения, сформированных в дисфункциональной семье.'
        }
        return lit_info.get(lit_type, 'Информация о литературе.')
    
    # ==================== 6. SUPPORT OR SPECIALIST CHOICE ====================
    
    async def handle_support_or_specialist(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle choice between support group or specialist."""
        query = update.callback_query
        await query.answer()
        
        choice = query.data.replace('sos_', '')
        context.user_data['preferences']['sos_choice'] = choice
        
        logger.info(f"User {format_user_info(query.from_user)} chose: {choice}")
        
        if choice == 'support_group':
            # Show online/offline groups info with real data
            dependency_type = context.user_data['preferences'].get('dependency', '')
            dependency_name = self.conversation_flow.dependency_types.get(dependency_type, 'выбранной зависимости')
            city = context.user_data['preferences'].get('city', '')
            city_name = self.conversation_flow.get_city_name(city) if city else 'вашем городе'
            timezone = context.user_data['preferences'].get('timezone', '')
            timezone_name = self.conversation_flow.time_zones.get(timezone, 'Не указан')
            
            # Получаем ссылку для конкретной зависимости и города
            link = get_dependency_link(city, dependency_type)
            
            if link:
                link_text = f"🔗 Ссылка: {link}"
            elif dependency_type == 'vr':
                link_text = "(информация появится позже)"
            else:
                link_text = "(ссылка недоступна для этого города)"
            
            message = f"""
👥 **Подбор онлайн/офлайн-групп**

**Ваши данные:**
• Зависимость: {dependency_name}
• Часовой пояс: {timezone_name}
• Город: {city_name}

{link_text}
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Продолжить", callback_data="continue_to_discovery")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.ONLINE_OFFLINE_GROUPS.value
            return BotStates.ONLINE_OFFLINE_GROUPS.value
            
        elif choice == 'specialist':
            # Ask for user's gender
            message = """
👤 **Консультация специалиста**

Укажите ваш пол:
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_gender_keyboard(),
                parse_mode='Markdown'
            )
            
            context.user_data['preferences']['consultation_type'] = 'specialist'
            context.user_data['current_state'] = BotStates.GENDER_PREFERENCE.value
            return BotStates.GENDER_PREFERENCE.value
    
    # ==================== 7. SPECIALIST FLOW ====================
    
    async def handle_gender_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle user's gender selection."""
        query = update.callback_query
        await query.answer()
        
        # Handle back button
        if query.data == 'back_from_gender':
            return await self.back_from_gender(update, context)
        
        gender = query.data.replace('gender_', '')
        context.user_data['preferences']['gender'] = gender
        
        gender_name = self.conversation_flow.gender_options.get(gender, 'Не указан')
        logger.info(f"User {format_user_info(query.from_user)} selected gender: {gender_name}")
        
        message = """
🎂 **Укажите ваш возраст:**
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_age_user_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.AGE_USER.value
        return BotStates.AGE_USER.value
    
    async def handle_age_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle user's age selection."""
        query = update.callback_query
        await query.answer()
        
        # Handle back button
        if query.data == 'back_to_gender':
            return await self.back_to_gender(update, context)
        
        age = query.data.replace('ageu_', '')
        context.user_data['preferences']['age_user'] = age
        
        age_name = self.conversation_flow.age_user_options.get(age, 'Не указан')
        logger.info(f"User {format_user_info(query.from_user)} age: {age_name}")
        
        # Check consultation type - for psychologist we don't need specialist age preference
        consultation_type = context.user_data['preferences'].get('consultation_type', 'specialist')
        
        if consultation_type == 'psychologist':
            # Skip specialist age, go directly to result
            prefs = context.user_data['preferences']
            message = f"""
✅ **Подбор психолога завершен!**

**Ваши данные:**
• Ваш пол: {self.conversation_flow.gender_options.get(prefs.get('gender'), 'Не указан')}
• Ваш возраст: {age_name}

Психолог будет подобран в соответствии с вашими предпочтениями.
Администратор свяжется с вами в ближайшее время.
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Продолжить", callback_data="continue_to_discovery")]
            ])
            
            await query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.AGE_USER.value
            return BotStates.AGE_USER.value
        else:
            # For specialist consultation, ask for age preference
            message = """
👨‍⚕️ **Укажите предпочитаемый возраст специалиста:**
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_age_specialist_keyboard(),
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.AGE_SPECIALIST_PREFERENCE.value
            return BotStates.AGE_SPECIALIST_PREFERENCE.value
    
    async def handle_age_specialist(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle specialist age preference selection."""
        query = update.callback_query
        await query.answer()
        
        age_pref = query.data.replace('ages_', '')
        context.user_data['preferences']['age_specialist'] = age_pref
        
        age_name = self.conversation_flow.age_specialist_options.get(age_pref, 'Не указан')
        logger.info(f"User {format_user_info(query.from_user)} prefers specialist age: {age_name}")
        
        # Show specialist search result
        prefs = context.user_data['preferences']
        message = f"""
✅ **Подбор специалиста завершен!**

**Ваши предпочтения:**
• Ваш пол: {self.conversation_flow.gender_options.get(prefs.get('gender'), 'Не указан')}
• Ваш возраст: {self.conversation_flow.age_user_options.get(prefs.get('age_user'), 'Не указан')}
• Возраст специалиста: {age_name}

С вами свяжется специалист в течении 24 часов для уточнения информации и запроса.
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Продолжить", callback_data="continue_to_discovery")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        
        logger.info(f"Showing specialist selection complete message with continue button, state: AGE_SPECIALIST_PREFERENCE")
        context.user_data['current_state'] = BotStates.AGE_SPECIALIST_PREFERENCE.value
        return BotStates.AGE_SPECIALIST_PREFERENCE.value
    
    # ==================== 8. DISCOVERY QUESTION ====================
    
    async def show_discovery_question(self, query, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Show 'How did you find us?' question."""
        logger.info(f"Showing discovery question to user: {format_user_info(query.from_user)}")
        
        message = """
📊 **Как вы о нас узнали?**

Эта информация поможет нам лучше помогать другим людям:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_discovery_keyboard(),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.HOW_FOUND_US.value
        return BotStates.HOW_FOUND_US.value
    
    async def handle_continue_to_discovery(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle continue button to discovery question."""
        query = update.callback_query
        await query.answer()
        
        logger.info(f"User {format_user_info(query.from_user)} clicked continue to discovery")
        
        return await self.show_discovery_question(query, context)
    
    async def handle_discovery_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle discovery source answer."""
        query = update.callback_query
        await query.answer()
        
        source = query.data.replace('found_', '')
        context.user_data['discovery_source'] = source
        
        source_name = self.conversation_flow.discovery_sources.get(source, 'Другое')
        logger.info(f"User {format_user_info(query.from_user)} found us via: {source_name}")
        
        if source == 'support_group':
            # Ask for group name
            message = """
📝 **Укажите название группы:**

Пожалуйста, напишите название группы поддержки, через которую вы о нас узнали.
            """
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.GROUP_NAME_INPUT.value
            return BotStates.GROUP_NAME_INPUT.value
            
        elif source == 'psychologist':
            # Ask for psychologist name
            message = """
📝 **Укажите имя психолога:**

Пожалуйста, напишите имя психолога, который вам рекомендовал нас.
            """
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.PSYCHOLOGIST_NAME_INPUT.value
            return BotStates.PSYCHOLOGIST_NAME_INPUT.value
        else:
            # Skip to anonymous question
            return await self.show_anonymous_question(query, context)
    
    async def handle_group_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle group name text input."""
        group_name = sanitize_input(update.message.text)
        context.user_data['group_name'] = group_name
        
        logger.info(f"User {format_user_info(update.effective_user)} provided group name: {group_name}")
        
        message = f"""
✅ **Спасибо!**

Название группы: {group_name}
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
        # Now show anonymous question
        return await self.show_anonymous_question_message(update, context)
    
    async def handle_psychologist_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle psychologist name text input."""
        psychologist_name = sanitize_input(update.message.text)
        context.user_data['psychologist_name'] = psychologist_name
        
        logger.info(f"User {format_user_info(update.effective_user)} provided psychologist name: {psychologist_name}")
        
        message = f"""
✅ **Спасибо!**

Имя психолога: {psychologist_name}
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
        # Now show anonymous question
        return await self.show_anonymous_question_message(update, context)
    
    # ==================== 9. ANONYMOUS QUESTION ====================
    
    async def show_anonymous_question(self, query, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Show anonymous question choice."""
        message = """
❓ **Задать анонимный вопрос**

Хотите задать анонимный вопрос? Ответ будет опубликован в разделе "Ответы на популярные вопросы".
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_yes_no_keyboard_no_back('anon_question'),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.ANONYMOUS_QUESTION_CHOICE.value
        return BotStates.ANONYMOUS_QUESTION_CHOICE.value
    
    async def show_anonymous_question_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Show anonymous question choice as new message."""
        message = """
❓ **Задать анонимный вопрос**

Хотите задать анонимный вопрос? Ответ будет опубликован в разделе "Ответы на популярные вопросы".
        """
        
        await update.message.reply_text(
            message,
            reply_markup=self.conversation_flow.get_yes_no_keyboard_no_back('anon_question'),
            parse_mode='Markdown'
        )
        
        context.user_data['current_state'] = BotStates.ANONYMOUS_QUESTION_CHOICE.value
        return BotStates.ANONYMOUS_QUESTION_CHOICE.value
    
    async def handle_anonymous_question_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle yes/no for anonymous question."""
        query = update.callback_query
        await query.answer()
        
        logger.info(f"User {format_user_info(query.from_user)} anonymous question choice: {query.data}")
        
        if query.data.startswith('yes_'):
            message = """
📝 **Напишите свой вопрос:**

Пожалуйста, напишите ваш анонимный вопрос. Ответ появится в разделе "Ответы на популярные вопросы".
            """
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown'
            )
            
            context.user_data['current_state'] = BotStates.ANONYMOUS_QUESTION_INPUT.value
            return BotStates.ANONYMOUS_QUESTION_INPUT.value
        else:
            # Skip to final message
            logger.info(f"User {format_user_info(query.from_user)} declined anonymous question, showing final message")
            return await self.show_final_message(query, context)
    
    async def handle_anonymous_question_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle anonymous question text input."""
        question = sanitize_input(update.message.text)
        context.user_data['anonymous_question'] = question
        
        logger.info(f"User {format_user_info(update.effective_user)} asked: {question[:50]}...")
        
        message = """
✅ **Спасибо за обращение!**

Ваш вопрос принят. Скоро ответ на ваш вопрос появится в разделе "Ответы на популярные вопросы".
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
        # Show final message
        return await self.show_final_message_new(update, context)
    
    # ==================== 10. FINAL MESSAGE ====================
    
    async def show_final_message(self, query, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Show final thank you message."""
        final_message = """
✨ Спасибо за обращение!

Ваша заявка принята. В ближайшее время с вами свяжется наш специалист.

Важные контакты:
🆘 Экстренная помощь: 8-800-XXX-XX-XX
💬 Поддержка: @support_username
📧 Email: help@support.ru

Помните: 
• Вы не одиноки в этой борьбе
• Обращение за помощью - это проявление силы
• Каждый день без зависимости - это победа

Вы можете начать новый разговор командой /start

Берегите себя! 💚
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❓ Ответы на популярные вопросы", callback_data="final_faq")],
            [InlineKeyboardButton("📅 Расписание вебинаров спикеров", callback_data="final_webinars")],
            [InlineKeyboardButton("🔄 Вернуться к началу", callback_data="restart_conversation")]
        ])
        
        await query.edit_message_text(
            final_message,
            reply_markup=keyboard
        )
        
        logger.info(f"Conversation completed for user: {format_user_info(query.from_user)}")
        
        return BotStates.CONVERSATION_END.value
    
    async def handle_final_faq(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle FAQ button from final message."""
        query = update.callback_query
        await query.answer()
        
        message = """
❓ **Ответы на популярные вопросы**

**Q: Вредно ли опохмеляться?**
A: Да, опохмеление лишь усугубляет пагубное воздействие на организм

**Q: Алкоголь является фактором риска развития онкологических заболеваний?**
A: Да, этанол, содержащийся в любом спиртном напитке, повышает вероятность возникновения онкологических заболеваний.

**Q: Могу ли я сам, своей силой воли, избавиться от зависимости?**
A: Если стадия лёгкая, попробовать можно, но при более тяжёлой степени зависимости без посторонние помощи и поддержки вы не справитесь

**Q: Без чего (кого) не справиться с зависимостью?**
A: Полноценно справиться с зависимостью поможет правильный подход, основанный на программе 12 шагов, поддержка со стороны и если требуется, обращение за медикаментозным лечением в клинике
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_final")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        
        return BotStates.CONVERSATION_END.value
    
    async def handle_final_webinars(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle webinars button from final message."""
        query = update.callback_query
        await query.answer()
        
        message = """
📅 Расписание вебинаров спикеров

Ближайшие вебинары будут указаны позже.

Мы работаем над формированием расписания интересных и полезных вебинаров с опытными спикерами в области зависимостей и восстановления.

Следите за обновлениями!
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_final")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        return BotStates.CONVERSATION_END.value
    
    async def handle_back_to_final(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle back button to return to final message."""
        query = update.callback_query
        await query.answer()
        
        return await self.show_final_message(query, context)
    
    async def handle_restart_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Handle restart conversation button - go back to dependency selection."""
        query = update.callback_query
        await query.answer()
        
        # Clear user data
        context.user_data.clear()
        context.user_data['preferences'] = {}
        
        message = """
🤝 Выбор типа зависимости

Укажите, с каким видом зависимости вы столкнулись:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_dependency_keyboard()
        )
        
        context.user_data['current_state'] = BotStates.DEPENDENCY_SELECTION.value
        logger.info(f"User {format_user_info(query.from_user)} restarted conversation")
        
        return BotStates.DEPENDENCY_SELECTION.value
    
    async def show_final_message_new(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Show final thank you message as new message."""
        final_message = """
✨ Спасибо за обращение!

Ваша заявка принята. В ближайшее время с вами свяжется наш специалист.

Важные контакты:
🆘 Экстренная помощь: 8-800-XXX-XX-XX
💬 Поддержка: @support_username
📧 Email: help@support.ru

Помните: 
• Вы не одиноки в этой борьбе
• Обращение за помощью - это проявление силы
• Каждый день без зависимости - это победа

Вы можете начать новый разговор командой /start

Берегите себя! 💚
        """
        
        await update.message.reply_text(
            final_message
        )
        
        logger.info(f"Conversation completed for user: {format_user_info(update.effective_user)}")
        
        return BotStates.CONVERSATION_END.value
    
    # ==================== BACK NAVIGATION ====================
    
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
    
    async def back_to_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to city selection."""
        query = update.callback_query
        await query.answer()
        
        timezone = context.user_data['preferences'].get('timezone', '')
        timezone_name = self.conversation_flow.time_zones.get(timezone, 'Неизвестный часовой пояс')
        
        message = f"""
✅ **Часовой пояс: {timezone_name}**

Выберите город:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_city_keyboard(timezone),
            parse_mode='Markdown'
        )
        
        return BotStates.CITY_SELECTION.value
    
    async def back_to_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to help type selection."""
        query = update.callback_query
        await query.answer()
        
        city = context.user_data['preferences'].get('city', '')
        city_name = self.conversation_flow.get_city_name(city)
        
        message = f"""
✅ **Город: {city_name}**

Какая помощь необходима?
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_help_type_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.HELP_TYPE.value
    
    async def back_to_sos(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to support or specialist choice."""
        query = update.callback_query
        await query.answer()
        
        message = """
Выберите, что вам нужно:

Консультация психолога
Группа поддержки
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Консультация психолога", callback_data="sos_specialist")],
            [InlineKeyboardButton("Группа поддержки", callback_data="sos_support_group")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_help")]
        ])
        
        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )
        
        return BotStates.SUPPORT_OR_SPECIALIST.value
    
    async def back_to_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to gender selection."""
        query = update.callback_query
        await query.answer()
        
        message = """
👤 **Консультация специалиста/психолога**

Укажите ваш пол:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_gender_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.GENDER_PREFERENCE.value
    
    async def back_from_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back from gender selection - check where we came from."""
        query = update.callback_query
        await query.answer()
        
        # Check if we came from support_or_specialist menu or directly from help_type
        came_from_sos = 'sos_choice' in context.user_data.get('preferences', {})
        
        if came_from_sos:
            # Came from support_or_specialist choice
            return await self.back_to_sos(update, context)
        else:
            # Came directly from help_type menu
            city = context.user_data['preferences'].get('city', '')
            city_name = self.conversation_flow.get_city_name(city)
            
            message = f"""
✅ Город: {city_name}

Какая помощь необходима?
            """
            
            await query.edit_message_text(
                message,
                reply_markup=self.conversation_flow.get_help_type_keyboard()
            )
            
            return BotStates.HELP_TYPE.value
    
    async def back_to_age_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Go back to user age selection."""
        query = update.callback_query
        await query.answer()
        
        message = """
🎂 **Укажите ваш возраст:**
        """
        
        await query.edit_message_text(
            message,
            reply_markup=self.conversation_flow.get_age_user_keyboard(),
            parse_mode='Markdown'
        )
        
        return BotStates.AGE_USER.value
    
    # ==================== UTILITY COMMANDS ====================
    
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
• Предоставить информацию о зависимостях
• Подобрать группу поддержки
• Найти специалиста
• Предложить литературу
• Принять анонимные вопросы

**Конфиденциальность:**
Все разговоры анонимны и конфиденциальны.

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
        """Handle /back command."""
        if 'current_state' not in context.user_data:
            await update.message.reply_text(
                "Нет предыдущего шага. Начните диалог с команды /start"
            )
            return -1
        
        current_state = context.user_data.get('current_state')
        
        # Map states to back handlers
        back_map = {
            BotStates.TIME_ZONE_SELECTION.value: self.back_to_dependency,
            BotStates.CITY_SELECTION.value: self.back_to_timezones,
            BotStates.HELP_TYPE.value: self.back_to_city,
            BotStates.SUPPORT_OR_SPECIALIST.value: self.back_to_help,
            BotStates.GENDER_PREFERENCE.value: self.back_to_sos,
            BotStates.AGE_USER.value: self.back_to_gender,
            BotStates.AGE_SPECIALIST_PREFERENCE.value: self.back_to_age_user,
        }
        
        handler = back_map.get(current_state)
        if handler:
            # Create a fake query object for back handlers
            await update.message.reply_text("Возвращаюсь назад...")
            return current_state
        else:
            await update.message.reply_text(
                "Используйте кнопки для навигации."
            )
            return current_state
    
    # ==================== STATE MAPPING ====================
    
    def get_conversation_states(self) -> Dict[str, list]:
        """Get conversation states mapping for ConversationHandler."""
        return {
            BotStates.DEPENDENCY_SELECTION.value: [
                CallbackQueryHandler(self.handle_dependency_selection, pattern='^dep_')
            ],
            BotStates.TIME_ZONE_SELECTION.value: [
                CallbackQueryHandler(self.back_to_dependency, pattern='^back_to_dependency'),
                CallbackQueryHandler(self.handle_timezone_selection, pattern='^timezone_')
            ],
            BotStates.CITY_SELECTION.value: [
                CallbackQueryHandler(self.back_to_timezones, pattern='^back_to_timezones'),
                CallbackQueryHandler(self.handle_city_selection, pattern='^city_')
            ],
            BotStates.HELP_TYPE.value: [
                CallbackQueryHandler(self.back_to_city, pattern='^back_to_city'),
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_help'),
                CallbackQueryHandler(self.handle_help_type, pattern='^help_')
            ],
            BotStates.HELP_CHOICE.value: [
                CallbackQueryHandler(self.handle_choose_support, pattern='^choose_support'),
                CallbackQueryHandler(self.handle_choose_literature, pattern='^choose_literature'),
                CallbackQueryHandler(self.handle_skip_both, pattern='^skip_both'),
                CallbackQueryHandler(self.handle_support_choice_after_info, pattern='^yes_support'),
                CallbackQueryHandler(self.handle_support_choice_after_info, pattern='^no_support'),
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_help'),
                CallbackQueryHandler(self.back_to_help, pattern='^back_from_support')
            ],
            BotStates.LITERATURE_CHOICE.value: [
                CallbackQueryHandler(self.handle_continue_after_literature, pattern='^continue_after_literature'),
                CallbackQueryHandler(self.handle_literature_selection, pattern='^lit_'),
                CallbackQueryHandler(self.handle_literature_choice_after_info, pattern='^yes_literature_after_info'),
                CallbackQueryHandler(self.handle_literature_choice_after_info, pattern='^no_literature_after_info'),
                CallbackQueryHandler(self.handle_literature_choice, pattern='^yes_literature'),
                CallbackQueryHandler(self.handle_literature_choice, pattern='^no_literature'),
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_help'),
                CallbackQueryHandler(self.back_to_help, pattern='^back_from_literature')
            ],
            BotStates.SUPPORT_OR_SPECIALIST.value: [
                CallbackQueryHandler(self.back_to_help, pattern='^back_to_help'),
                CallbackQueryHandler(self.handle_support_or_specialist, pattern='^sos_')
            ],
            BotStates.GENDER_PREFERENCE.value: [
                CallbackQueryHandler(self.back_from_gender, pattern='^back_from_gender'),
                CallbackQueryHandler(self.handle_gender_selection, pattern='^gender_')
            ],
            BotStates.AGE_USER.value: [
                CallbackQueryHandler(self.back_to_gender, pattern='^back_to_gender'),
                CallbackQueryHandler(self.handle_age_user, pattern='^ageu_')
            ],
            BotStates.AGE_SPECIALIST_PREFERENCE.value: [
                CallbackQueryHandler(self.back_to_age_user, pattern='^back_to_age_user'),
                CallbackQueryHandler(self.handle_age_specialist, pattern='^ages_'),
                CallbackQueryHandler(self.handle_continue_to_discovery, pattern='^continue_to_discovery')
            ],
            BotStates.ONLINE_OFFLINE_GROUPS.value: [
                CallbackQueryHandler(self.handle_continue_to_discovery, pattern='^continue_to_discovery')
            ],
            BotStates.HOW_FOUND_US.value: [
                CallbackQueryHandler(self.handle_discovery_answer, pattern='^found_')
            ],
            BotStates.GROUP_NAME_INPUT.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_group_name_input)
            ],
            BotStates.PSYCHOLOGIST_NAME_INPUT.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_psychologist_name_input)
            ],
            BotStates.ANONYMOUS_QUESTION_CHOICE.value: [
                CallbackQueryHandler(self.handle_anonymous_question_choice, pattern='^yes_anon_question'),
                CallbackQueryHandler(self.handle_anonymous_question_choice, pattern='^no_anon_question')
            ],
            BotStates.ANONYMOUS_QUESTION_INPUT.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_anonymous_question_input)
            ],
            BotStates.CONVERSATION_END.value: [
                CallbackQueryHandler(self.handle_final_faq, pattern='^final_faq'),
                CallbackQueryHandler(self.handle_final_webinars, pattern='^final_webinars'),
                CallbackQueryHandler(self.handle_back_to_final, pattern='^back_to_final'),
                CallbackQueryHandler(self.handle_restart_conversation, pattern='^restart_conversation')
            ]
        }

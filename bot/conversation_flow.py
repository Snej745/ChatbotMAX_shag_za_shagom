"""
Conversation flow manager for the dependency counseling bot.
Manages the decision tree and conversation logic.
"""

from typing import Dict, List, Any, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .states import BotStates

class ConversationFlow:
    """Manages the conversation flow and decision tree logic."""
    
    def __init__(self):
        self.dependency_types = {
            'alcohol': 'Алкогольная зависимость',
            'drugs': 'Наркотическая зависимость', 
            'gaming': 'Игровая зависимость (Лудомания)',
            'food': 'Пищевая зависимость (РПП)',
            'internet': 'Интернет-зависимость',
            'nicotine': 'Никотиновая зависимость',
            'codependency': 'Созависимость',
            'vad': 'ВДА (взрослые дети алкоголиков)',
            'love': 'Любовная зависимость',
            'workaholism': 'Трудоголизм',
            'vr': 'ВР (Взрослый ребёнок)'
        }
        
        # Часовые пояса (для выбора пояса)
        self.time_zones = {
            'msk': 'МСК',
            'msk_plus_1': 'МСК+1',
            'msk_plus_2': 'МСК+2',
            'msk_plus_3': 'МСК+3',
            'msk_plus_4': 'МСК+4',
            'msk_plus_5': 'МСК+5',
            'msk_plus_6': 'МСК+6',
            'msk_plus_7': 'МСК+7',
            'msk_plus_8': 'МСК+8',
            'msk_plus_9': 'МСК+9',
            'msk_minus_1': 'МСК-1'
        }
        
        # Города по часовым поясам
        self.cities_by_timezone = {
            'msk': {
                'moscow': 'Москва',
                'spb': 'Санкт-Петербург',
                'voronezh': 'Воронеж',
                'krasnodar': 'Краснодар',
                'kazan': 'Казань'
            },
            'msk_plus_1': {
                'samara': 'Самара',
                'izhevsk': 'Ижевск'
            },
            'msk_plus_2': {
                'ekaterinburg': 'Екатеринбург',
                'chelyabinsk': 'Челябинск'
            },
            'msk_plus_3': {
                'omsk': 'Омск',
                'barnaul': 'Барнаул'
            },
            'msk_plus_4': {
                'novosibirsk': 'Новосибирск',
                'krasnoyarsk': 'Красноярск'
            },
            'msk_plus_5': {
                'irkutsk': 'Иркутск',
                'ulan_ude': 'Улан-Удэ'
            },
            'msk_plus_6': {
                'yakutsk': 'Якутск',
                'blagoveshchensk': 'Благовещенск'
            },
            'msk_plus_7': {
                'vladivostok': 'Владивосток',
                'khabarovsk': 'Хабаровск'
            },
            'msk_plus_8': {
                'magadan': 'Магадан',
                'yuzhno_sakhalinsk': 'Южно-Сахалинск'
            },
            'msk_plus_9': {
                'petropavlovsk': 'Петропавловск-Камчатский',
                'anadyr': 'Анадырь'
            },
            'msk_minus_1': {
                'kaliningrad': 'Калининград'
            }
        }
        
        self.help_types = {
            'info': 'Информация о зависимости',
            'groups_selection': 'Подбор онлайн/офлайн-групп',
            'specialist': 'Консультация специалиста',
            'faq': 'Ответы на популярные вопросы',
            'webinars': 'Расписание вебинаров спикеров'
        }
        
        self.support_or_specialist = {
            'support_group': 'Группа поддержки',
            'specialist': 'Консультация специалиста'
        }
        
        self.literature_options = {
            '12steps': '12 шагов и 12 традиций',
            'new_glasses': 'Новые очки'
        }
        
        self.gender_options = {
            'male': 'Мужской',
            'female': 'Женский'
        }
        
        self.age_user_options = {
            '16_18': '16-18',
            '18_25': '18-25',
            '25_35': '25-35',
            '35_50': '35-50',
            '50_plus': '50+'
        }
        
        self.age_specialist_options = {
            'young': 'Молодой',
            'middle': 'Средний'
        }
        
        self.discovery_sources = {
            'friends': 'Друзья/знакомые',
            'ads': 'Реклама',
            'psychologist': 'Психолог',
            'support_group': 'Группа поддержки',
            'other': 'Другое'
        }
    
    def get_dependency_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for dependency type selection."""
        keyboard = []
        for key, value in self.dependency_types.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"dep_{key}")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_time_zone_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for time zone selection (first step)."""
        keyboard = []
        for key, value in self.time_zones.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"timezone_{key}")])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_dependency")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_city_keyboard(self, timezone: str) -> InlineKeyboardMarkup:
        """Create keyboard for city selection within a time zone."""
        keyboard = []
        cities = self.cities_by_timezone.get(timezone, {})
        
        for key, value in cities.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"city_{key}")])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("⬅️ Назад к часовым поясам", callback_data="back_to_timezones")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_city_name(self, city_key: str) -> str:
        """Get city name by its key."""
        for timezone_cities in self.cities_by_timezone.values():
            if city_key in timezone_cities:
                return timezone_cities[city_key]
        return "Неизвестный город"
    
    def get_help_type_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for help type selection."""
        keyboard = []
        for key, value in self.help_types.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"help_{key}")])
        
        # Add back button to city selection
        keyboard.append([InlineKeyboardButton("⬅️ Назад к выбору города", callback_data="back_to_city")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_yes_no_keyboard(self, context: str) -> InlineKeyboardMarkup:
        """Create Yes/No keyboard for various contexts."""
        keyboard = [
            [InlineKeyboardButton("Да", callback_data=f"yes_{context}")],
            [InlineKeyboardButton("Нет", callback_data=f"no_{context}")],
            [InlineKeyboardButton("⬅️ Назад", callback_data=f"back_from_{context}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_yes_no_keyboard_no_back(self, context: str) -> InlineKeyboardMarkup:
        """Create Yes/No keyboard without back button."""
        keyboard = [
            [InlineKeyboardButton("Да", callback_data=f"yes_{context}")],
            [InlineKeyboardButton("Нет", callback_data=f"no_{context}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_support_or_specialist_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for support group or specialist choice."""
        keyboard = []
        for key, value in self.support_or_specialist.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"sos_{key}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_help")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_literature_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for literature selection."""
        keyboard = []
        for key, value in self.literature_options.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"lit_{key}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_help")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_gender_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for gender selection."""
        keyboard = []
        for key, value in self.gender_options.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"gender_{key}")])
        
        # Back button should go to help type if consultation_type is 'psychologist'
        # otherwise to support_or_specialist
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_from_gender")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_age_user_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for user age selection."""
        keyboard = []
        for key, value in self.age_user_options.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"ageu_{key}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_gender")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_age_specialist_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for specialist age preference."""
        keyboard = []
        for key, value in self.age_specialist_options.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"ages_{key}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_age_user")])
        return InlineKeyboardMarkup(keyboard)
    
    def get_discovery_keyboard(self) -> InlineKeyboardMarkup:
        """Create keyboard for discovery source selection."""
        keyboard = []
        for key, value in self.discovery_sources.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"found_{key}")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_dependency_info(self, dependency_type: str) -> str:
        """Get information about a specific dependency type."""
        info_texts = {
            'alcohol': """
🍷 **Алкогольная зависимость**

Алкогольная зависимость - это хроническое заболевание, характеризующееся:
• Потерей контроля над употреблением
• Физической и психологической зависимостью  
• Негативным влиянием на все сферы жизни

**Признаки:**
• Увеличение толерантности к алкоголю
• Синдром отмены при прекращении употребления
• Пренебрежение обязанностями и интересами
• Продолжение употребления несмотря на проблемы

**Помощь доступна 24/7**
            """,
            'drugs': """
💊 **Наркотическая зависимость**

Наркотическая зависимость - серьезное заболевание, требующее профессиональной помощи:
• Физическая зависимость от психоактивных веществ
• Компульсивное поведение в поиске наркотиков
• Разрушение социальных связей и здоровья

**Важно знать:**
• Зависимость - это болезнь, а не слабость характера
• Существуют эффективные методы лечения
• Поддержка близких играет важную роль
• Анонимность гарантирована

**Обратитесь за помощью прямо сейчас**
            """,
            'gaming': """
🎮 **Игровая зависимость/Лудомания**

Игровая зависимость включает зависимость от:
• Компьютерных и видеоигр
• Азартных игр (лудомания)  
• Онлайн-игр и казино

**Симптомы:**
• Потеря контроля времени за игрой
• Пренебрежение реальной жизнью
• Финансовые проблемы (при лудомании)
• Агрессия при попытке ограничить игру
• Ложь о времени, проведенном в играх

**Вы не одиноки в этой борьбе**
            """
        }
        
        return info_texts.get(dependency_type, "Информация о данном типе зависимости находится в разработке.")
    
    def get_webinar_schedule(self) -> str:
        """Get webinar schedule information."""
        return """
📅 **Расписание вебинаров и групп поддержки**

**Еженедельные онлайн-встречи:**
• Понедельник, 19:00 - Группа для зависимых от алкоголя
• Вторник, 20:00 - Созависимые и семьи
• Среда, 18:30 - Игровая зависимость  
• Четверг, 19:30 - Наркотическая зависимость
• Пятница, 20:00 - Группа поддержки для всех типов зависимостей
• Суббота, 16:00 - Семинар "Первые шаги к выздоровлению"
• Воскресенье, 18:00 - Медитация и практики осознанности

**Специальные программы:**
• Месячный курс "Преодоление зависимости" - каждый первый понедельник месяца
• Индивидуальные консультации - по записи

Для участия напишите администратору.
        """
    
    def format_specialist_search(self, user_preferences: Dict[str, str]) -> str:
        """Format specialist search results based on user preferences."""
        dependency = self.dependency_types.get(user_preferences.get('dependency', ''), 'Не указано')
        time_pref = self.time_slots.get(user_preferences.get('time', ''), 'Гибкий')
        gender_pref = self.specialist_preferences['gender'].get(user_preferences.get('gender', ''), 'Без предпочтений')
        age_pref = self.specialist_preferences['age'].get(user_preferences.get('age', ''), 'Без предпочтений')
        
        return f"""
👨‍⚕️ **Подбор специалиста**

**Ваши предпочтения:**
• Тип зависимости: {dependency}
• Удобное время: {time_pref}  
• Пол специалиста: {gender_pref}
• Возраст специалиста: {age_pref}

**Найденные специалисты будут связаны с вами в течение 24 часов.**

В случае срочной необходимости обратитесь:
📞 Горячая линия: 8-800-XXX-XX-XX (круглосуточно)
💬 Чат поддержки: t.me/support_chat

*Все консультации конфиденциальны*
        """
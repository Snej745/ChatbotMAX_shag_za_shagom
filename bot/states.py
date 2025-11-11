"""
Bot states for conversation flow.
Defines all possible states in the conversation.
"""

from enum import Enum

class BotStates(Enum):
    """Enumeration of bot conversation states."""
    
    # Initial states
    MAIN_MENU = "main_menu"
    DEPENDENCY_SELECTION = "dependency_selection"
    
    # Time preference states
    TIME_ZONE_SELECTION = "time_zone_selection"
    CITY_SELECTION = "city_selection"
    
    # Help type states
    HELP_TYPE = "help_type"
    HELP_CHOICE = "help_choice"
    
    # Literature choice
    LITERATURE_CHOICE = "literature_choice"
    
    # Support group or specialist choice
    SUPPORT_OR_SPECIALIST = "support_or_specialist"
    
    # Specialist consultation states
    GENDER_PREFERENCE = "gender_preference"
    AGE_USER = "age_user"
    AGE_SPECIALIST_PREFERENCE = "age_specialist_preference"
    
    # Online/Offline groups
    ONLINE_OFFLINE_GROUPS = "online_offline_groups"
    
    # Information states
    DEPENDENCY_INFO = "dependency_info"
    FAQ_ANSWERS = "faq_answers"
    WEBINAR_SCHEDULE = "webinar_schedule"
    
    # Discovery states
    HOW_FOUND_US = "how_found_us"
    GROUP_NAME_INPUT = "group_name_input"
    PSYCHOLOGIST_NAME_INPUT = "psychologist_name_input"
    
    # Anonymous question
    ANONYMOUS_QUESTION_CHOICE = "anonymous_question_choice"
    ANONYMOUS_QUESTION_INPUT = "anonymous_question_input"
    
    # End states
    CONVERSATION_END = "conversation_end"
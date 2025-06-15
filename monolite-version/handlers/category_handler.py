# handlers/category_handler.py

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.menu_keyboards import get_category_selection_keyboard, get_period_selection_keyboard
from services.database_service import get_articles_from_db
from models.user_state import UserArticleState

user_state = UserArticleState()

def register_category_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda message: message.text == "Создать запрос")
    def handle_create_request(message: Message):
        try:
            markup = get_category_selection_keyboard()
            bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup)
        except Exception as e:
            from logging import getLogger
            logger = getLogger(__name__)
            logger.error(f"Ошибка при обработке 'Создать запрос': {e}")

    @bot.callback_query_handler(func=lambda call: call.data in [
        "Environmental", "Safety", "Sustainable Cities", "Manufacturing", "Culture"
    ])
    def handle_category_selection(call: CallbackQuery):
        try:
            category = call.data
            bot.answer_callback_query(call.id)

            # Сохраняем выбранную категорию в контексте пользователя
            if not hasattr(bot, "context"):
                bot.context = {}
            bot.context[call.message.chat.id] = {"category": category}

            markup = get_period_selection_keyboard()
            bot.send_message(call.message.chat.id, "Выберите период:", reply_markup=markup)
        except Exception as e:
            from logging import getLogger
            logger = getLogger(__name__)
            logger.error(f"Ошибка при выборе категории: {e}")
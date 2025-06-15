from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from keyboards.menu_keyboards import get_main_menu_keyboard


def register_start_handlers(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message: Message):
        try:
            menu_markup = get_main_menu_keyboard()
            welcome_text = (
                f"Привет, {message.chat.first_name}!\n"
                "Здесь вы можете посмотреть сбор публикаций по теме AI for Good за последний месяц 🚀\n"
                "Это поможет исследователям отслеживать ключевые научные достижения и технологические тренды 💯"
            )
            bot.send_message(message.chat.id, welcome_text, reply_markup=menu_markup)
        except Exception as e:
            from logging import getLogger
            logger = getLogger(__name__)
            logger.error(f"Ошибка в обработчике start: {e}")

# handlers/contact_handler.py

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

def register_contact_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda message: message.text == "Связаться с разработчиками")
    def handle_contact(message: Message):
        try:
            back_to_menu = ReplyKeyboardMarkup(resize_keyboard=True)
            btn = KeyboardButton("↩️ Вернуться в меню")
            back_to_menu.add(btn)

            bot.send_message(
                message.chat.id,
                "📬 Свяжитесь с нами:\n\n"
                "📧 Email: example@example.com\n"
                "📱 Telegram: @developer_username",
                reply_markup=back_to_menu
            )
        except Exception as e:
            from logging import getLogger
            logger = getLogger(__name__)
            logger.error(f"Ошибка в обработчике контактов: {e}")

    @bot.message_handler(func=lambda message: message.text == "↩️ Вернуться в меню")
    def handle_back_to_menu(message: Message):
        try:
            from handlers.start_handler import start
            start(message)
        except Exception as e:
            from logging import getLogger
            logger = getLogger(__name__)
            logger.error(f"Ошибка при возврате в меню: {e}")
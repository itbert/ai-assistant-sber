# bot/bot.py

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.handlers import start, show_categories, handle_category_selection
from config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.application = self._create_application()
        self._register_handlers()

    def _create_application(self):
        """Создаёт и настраивает приложение Telegram-бота."""
        logger.info("Initializing Telegram bot application")
        return Application.builder().token(Config.BOT_TOKEN).build()

    def _register_handlers(self):
        """Регистрирует обработчики команд и callback'ов."""
        logger.info("Registering bot handlers")

        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("categories", show_categories))
        self.application.add_handler(CallbackQueryHandler(handle_category_selection))

    def run(self):
        """Запускает бота в режиме polling."""
        logger.info("Starting Telegram bot...")
        self.application.run_polling()
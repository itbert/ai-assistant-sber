# main.py

import telebot
from telebot import types
from config.config import BOT_TOKEN
from handlers.start_handler import register_start_handlers
from handlers.category_handler import register_category_handlers
from handlers.article_handler import register_article_handlers
from handlers.contact_handler import register_contact_handlers
from logging import getLogger

import logging
from utils.logger_setup import setup_logger

# Настройка логгирования
setup_logger()
logger = getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Регистрация обработчиков
register_start_handlers(bot)
register_category_handlers(bot)
register_article_handlers(bot)
register_contact_handlers(bot)

if __name__ == '__main__':
    logger.info("Бот успешно запущен")
    bot.polling(none_stop=True)
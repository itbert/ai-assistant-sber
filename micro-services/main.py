# main.py

import logging
import threading
from bot.bot import TelegramBot
from parser.scheduler import run_parser_periodically
from config import Config

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start_parser():
    """Запускает парсер в отдельном потоке."""
    logger.info("Starting background parser thread")
    run_parser_periodically()


def main():
    # Инициализация базы данных
    from db.database import ArticleDatabase
    ArticleDatabase()  # вызов __init__, который создаёт таблицы

    # Запуск парсера в фоне
    parser_thread = threading.Thread(target=start_parser, daemon=True)
    parser_thread.start()

    # Запуск бота
    bot = TelegramBot()
    bot.run()


if __name__ == '__main__':
    main()

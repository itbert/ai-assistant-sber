# utils/logger_setup.py

import logging
import sys

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Удаляем стандартные хендлеры (если есть)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Создаем новый форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Хендлер для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Добавляем хендлеры
    logger.addHandler(console_handler)

    return logger
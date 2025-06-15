# bot/keyboard.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from typing import List

# Конфигурация отображения
BUTTONS_PER_ROW = 3  # Количество кнопок в одной строке


def get_categories_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с категориями статей.
    
    :return: объект InlineKeyboardMarkup
    """
    keyboard: List[List[InlineKeyboardButton]] = []

    categories = Config.ARXIV_CATEGORIES
    for i in range(0, len(categories), BUTTONS_PER_ROW):
        row = [
            InlineKeyboardButton(category, callback_data=category)
            for category in categories[i:i + BUTTONS_PER_ROW]
        ]
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def get_back_button() -> InlineKeyboardMarkup:
    """
    Создаёт клавишу "Назад".
    
    :return: объект InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("← Back to categories", callback_data="back")]
    ])
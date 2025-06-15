# keyboards/navigation_keyboards.py

from telebot import types

def get_article_navigation_markup(has_prev: bool, has_next: bool):
    """Клавиатура навигации по статьям"""
    markup = types.InlineKeyboardMarkup()

    row = []
    if has_prev:
        row.append(types.InlineKeyboardButton("⬅️ Предыдущая", callback_data="nav_prev"))
    if has_next:
        row.append(types.InlineKeyboardButton("Следующая ➡️", callback_data="nav_next"))
    if row:
        markup.row(*row)

    markup.add(types.InlineKeyboardButton("↩️ Назад к фильтрам", callback_data="back_to_filters"))
    markup.add(types.InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_menu"))

    return markup
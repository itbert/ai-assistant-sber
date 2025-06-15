# keyboards/menu_keyboards.py

from telebot import types

def get_main_menu_keyboard():
    """Главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать запрос")
    btn2 = types.KeyboardButton("Связаться с разработчиками")
    markup.add(btn1, btn2)
    return markup

def get_category_selection_keyboard():
    """Клавиатура для выбора категории"""
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="🌍 Экология", callback_data="Environmental"),
        types.InlineKeyboardButton(text="🛡 Безопасность", callback_data="Safety"),
        types.InlineKeyboardButton(text="🏙 Устойчивые города", callback_data="Sustainable Cities"),
        types.InlineKeyboardButton(text="🏭 Производство", callback_data="Manufacturing"),
        types.InlineKeyboardButton(text="🏛 Культура", callback_data="Culture")
    ]
    for btn in buttons:
        markup.add(btn)
    return markup

def get_period_selection_keyboard():
    """Выбор временного периода"""
    markup = types.InlineKeyboardMarkup()
    periods = {
        1: "📅 Эта неделя",
        2: "⬅️ Прошлая неделя",
        3: "📆 За весь месяц"
    }
    for key, value in periods.items():
        markup.add(types.InlineKeyboardButton(value, callback_data=f"date_{key}"))
    return markup

def get_source_filter_keyboard():
    """Фильтр по источникам"""
    markup = types.InlineKeyboardMarkup()
    sources = {
        0: "🇷🇺 Отечественные",
        1: "🌐 Иностранные",
        2: "🔍 Любые"
    }
    for key, value in sources.items():
        markup.add(types.InlineKeyboardButton(value, callback_data=f"filter_{key}"))
    return markup

def get_back_to_menu_button():
    """Кнопка 'Вернуться в меню'"""
    return types.InlineKeyboardButton("↩️ В главное меню", callback_data="back_to_menu")
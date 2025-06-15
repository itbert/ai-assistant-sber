# handlers/article_handler.py

from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup
from models.user_state import user_state
from services.database_service import get_articles_from_db
from keyboards.navigation_keyboards import get_article_navigation_markup
from constants import CATEGORIES, SOURCES, TRANSLATION_DICT
import logging

logger = logging.getLogger(__name__)

def register_article_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
    def handle_date_selection(call: CallbackQuery):
        try:
            _, period_str, category = call.data.split("_", 2)
            period_num = int(period_str)

            # Получаем подкатегории для выбранной категории
            subcategories = CATEGORIES.get(category, [])

            # Формируем клавиатуру фильтрации по источникам
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton('🇷🇺 Отечественные', callback_data=f"filter_0_{call.data}"),
                InlineKeyboardButton('🌐 Иностранные', callback_data=f"filter_1_{call.data}"),
                InlineKeyboardButton('🔍 Любые', callback_data=f"filter_2_{call.data}")
            )

            bot.send_message(call.message.chat.id, "Выберите источники:", reply_markup=markup)
        except Exception as e:
            logger.error(f"Ошибка при обработке выбора периода: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("filter_"))
    def handle_source_filter(call: CallbackQuery):
        try:
            _, filter_type, _, period_str, category = call.data.split("_", 4)
            filter_type = int(filter_type)
            period_num = int(period_str)

            # Получаем статьи из БД
            subcategories = CATEGORIES.get(category, [])
            articles = get_articles_from_db(subcategories)

            if not articles:
                bot.send_message(call.message.chat.id, "Статьи не найдены.")
                return

            # Сохраняем состояние пользователя
            user_state.set_user_data(call.message.chat.id, category, articles)

            # Показываем первую статью
            show_article(bot, call.message.chat.id, index=0, filter_type=filter_type, call_id=call.id)
        except Exception as e:
            logger.error(f"Ошибка при обработке фильтра: {e}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("nav_"))
    def handle_navigation(call: CallbackQuery):
        try:
            direction = call.data.split("_")[1]
            chat_id = call.message.chat.id

            # Получаем текущее состояние пользователя
            user_data = user_state.get_user_data(chat_id)
            if not user_data:
                bot.send_message(chat_id, "Произошла ошибка. Попробуйте начать заново.")
                return

            delta = -1 if direction == "prev" else 1
            success = user_state.update_index(chat_id, delta)

            if not success:
                bot.answer_callback_query(call.id, "Вы на границе списка.")
                return

            current_index = user_data["current_index"]
            filter_type = int(call.data.split("_")[-1])

            # Обновляем сообщение с новой статьёй
            show_article(bot, chat_id, current_index, filter_type, call.id, call.message.message_id)
        except Exception as e:
            logger.error(f"Ошибка навигации: {e}")


def show_article(bot: TeleBot, chat_id: int, index: int, filter_type: int, call_id: str, message_id: int = None):
    """
    Отображает текущую статью пользователю
    """
    try:
        user_data = user_state.get_user_data(chat_id)
        if not user_data or index >= len(user_data["articles"]):
            logger.warning(f"Неверные данные или индекс для chat_id {chat_id}")
            return False

        article = user_data["articles"][index]
        headline, time_author, description, link, category, source = article

        # Применяем фильтр по источнику
        if filter_type != 2 and source not in SOURCES[filter_type]:
            return show_article(bot, chat_id, index + 1, filter_type, call_id, message_id)

        time_author = time_author or "Не указано"
        description = description or "Описание отсутствует"
        category_ru = TRANSLATION_DICT.get(category, category)
        clickable_headline = f'<a href="{link}">{headline}</a>'

        message_text = (
            f"📌 <b>Заголовок:</b> {clickable_headline}\n"
            f"⏳ <b>Время:</b> {time_author}\n"
            f"📝 <b>Описание:</b> {description[:300] + '...' if len(description) > 300 else description}\n"
            f"🏷️ <b>Категория:</b> {category_ru}\n"
            f"📰 <b>Источник:</b> {link}"
        )

        has_prev = index > 0
        has_next = index < len(user_data["articles"]) - 1

        markup = get_article_navigation_markup(has_prev, has_next)

        if message_id is None:
            bot.send_message(
                chat_id,
                message_text,
                parse_mode='HTML',
                reply_markup=markup,
                disable_web_page_preview=True
            )
        else:
            bot.edit_message_text(
                message_text,
                chat_id,
                message_id,
                parse_mode='HTML',
                reply_markup=markup,
                disable_web_page_preview=True
            )

        logger.info(f"Статья #{index} успешно отправлена")
        return True

    except Exception as e:
        logger.error(f"Ошибка при отображении статьи: {e}")
        return False
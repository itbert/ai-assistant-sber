# bot/handlers.py
import logging
from typing import List, Tuple
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from bot.keyboard import get_categories_keyboard, get_back_button
from db.database import get_articles_by_tag
from config import Config


logger = logging.getLogger(__name__)

# Сообщения бота
START_MESSAGE = (
    "👋 Welcome to ArXiv ESG Bot!\n"
    "I track scientific articles and categorize them by ESG topics.\n"
    "Use /categories to browse articles."
)

NO_ARTICLES_MESSAGE = "📭 No articles found for `{category}`."

ARTICLE_TEMPLATE = "{index}. **{title}**\n{summary}\n"

SELECT_CATEGORY_MESSAGE = "📚 Select a category:"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    await update.message.reply_text(START_MESSAGE)


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /categories."""
    await update.message.reply_text(
        SELECT_CATEGORY_MESSAGE,
        reply_markup=get_categories_keyboard()
    )


async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора категории через inline-кнопки."""
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.edit_message_text(
            SELECT_CATEGORY_MESSAGE,
            reply_markup=get_categories_keyboard()
        )
        return

    articles = get_articles_by_tag(query.data)
    if not articles:
        await query.edit_message_text(
            NO_ARTICLES_MESSAGE.format(category=query.data),
            parse_mode='Markdown',
            reply_markup=get_back_button()
        )
        return

    response = _format_articles(articles, query.data)
    await query.edit_message_text(
        text=response,
        parse_mode='Markdown',
        reply_markup=get_back_button()
    )


def _format_articles(articles: List[Tuple], category: str) -> str:
    """Форматирует список статей в текстовое сообщение."""
    logger.info(f"Formatting {len(articles)} articles for category '{category}'")
    
    header = f"🔍 Latest articles in `{category}`:\n\n"
    body = ""
    
    for idx, (art_id, title, summary) in enumerate(articles, 1):
        body += ARTICLE_TEMPLATE.format(index=idx, title=title, summary=summary)
    
    return header + body
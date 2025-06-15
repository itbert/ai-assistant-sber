import feedparser
import sqlite3
import logging
import threading
import torch
from datetime import datetime
from transformers import pipeline, AutoTokenizer, MPNetModel
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Конфигурация
BOT_TOKEN = "7642905079:AAEApga21ZloQrAmjdchm_GFugRS0i4C-uU"  # Замените на реальный токен
ARXIV_CATEGORIES = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML']
PARSE_INTERVAL = 3600  # 1 час
DB_FILE = "arxiv_articles.db"

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def init_models():
    # Инициализация суммаризатора
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Инициализация классификатора
    tokenizer = AutoTokenizer.from_pretrained("ai-lab/ESGify")
    model = torch.load('esgify_model.pt', map_location=torch.device('cpu'))
    
    return summarizer, tokenizer, model

# Инициализация БД
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id TEXT PRIMARY KEY, 
                  title TEXT, 
                  summary TEXT,
                  tags TEXT)''')
    conn.commit()
    conn.close()

# Сохранение статьи в БД
def save_article(article):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?)",
              (article['id'], article['title'], article['summary'], ','.join(article['tags'])))
    conn.commit()
    conn.close()

# Загрузка статей из БД по тегу
def get_articles_by_tag(tag, limit=5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, summary FROM articles WHERE tags LIKE ? LIMIT ?", 
             (f'%{tag}%', limit))
    return c.fetchall()

# Классификация текста
def classify_text(text, tokenizer, model):
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt",
        return_attention_mask=True
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Берем топ-3 тега
    top_probs, top_indices = torch.topk(outputs.flatten(), 3)
    tags = [model.id2label[idx.item()] for idx in top_indices]
    return tags

# Парсер arXiv
def parse_arxiv(summarizer, tokenizer, classifier):
    logger.info("Парсинг arXiv...")
    
    for category in ARXIV_CATEGORIES:
        feed = feedparser.parse(f"http://arxiv.org/rss/{category}")
        
        for entry in feed.entries[:5]:  # Берем 5 статей
            article_id = entry.id.split('/')[-1]
            title = entry.title
            abstract = entry.summary
            
            # Суммаризация
            summary = summarizer(abstract, max_length=150, min_length=30)[0]['summary_text']
            
            # Классификация
            tags = classify_text(f"{title} {abstract}", tokenizer, classifier)
            
            # Сохранение статьи
            save_article({
                'id': article_id,
                'title': title,
                'summary': summary,
                'tags': tags
            })
            
            logger.info(f"Добавлено: {title} | Теги: {', '.join(tags)}")

# Периодический парсинг
def scheduled_parsing():
    summarizer, tokenizer, classifier = init_models()
    
    while True:
        try:
            parse_arxiv(summarizer, tokenizer, classifier)
            threading.Event().wait(PARSE_INTERVAL)
        except Exception as e:
            logger.error(f"Ошибка парсинга: {e}")
            threading.Event().wait(60)

# Telegram бот
def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Команда /start
    async def start(update: Update, context):
        await update.message.reply_text(
            "👋 Привет! Я бот для научных статей с arXiv.\n"
            "Используй /tags чтобы выбрать тег и увидеть статьи."
        )
    
    # Команда /tags
    async def show_tags(update: Update, context):
        keyboard = [[InlineKeyboardButton(tag, callback_data=tag)] for tag in ARXIV_CATEGORIES]
        await update.message.reply_text('Выберите тег:', reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Обработка выбора тега
    async def handle_tag(update: Update, context):
        query = update.callback_query
        await query.answer()
        
        articles = get_articles_by_tag(query.data)
        response = f"📚 Статьи с тегом {query.data}:\n\n"
        
        for i, (art_id, title, summary) in enumerate(articles, 1):
            response += f"{i}. {title}\n{summary}\n\n"
        
        await query.edit_message_text(response)
    
    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tags", show_tags))
    app.add_handler(CallbackQueryHandler(handle_tag))
    
    # Запуск бота
    app.run_polling()

# Главная функция
if __name__ == '__main__':
    # Инициализация БД
    init_db()
    
    # Запуск парсера в фоне
    threading.Thread(target=scheduled_parsing, daemon=True).start()
    
    # Запуск бота
    start_bot()
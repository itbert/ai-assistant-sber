import os

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    DB_FILE = "arxiv_articles.db"
    ARXIV_CATEGORIES = [
        'cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML', 
        'cs.NE', 'cs.RO', 'cs.SI', 'cs.SY'
    ]
    SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
    CLASSIFICATION_THRESHOLD = 0.3
    PARSE_INTERVAL = 3600  # 1 hour
    ESGIFY_MODEL_NAME = "ai-lab/ESGify"
    NER_MODEL = "flair/ner-english"
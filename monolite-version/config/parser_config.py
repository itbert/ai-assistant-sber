# config/parser_config.py

from pathlib import Path

# Настройки браузера
CHROME_OPTIONS = {
    "disable-gpu": True,
    "headless": True,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "excludeSwitches": ["enable-automation"],
    "useAutomationExtension": False
}

# URLs
URL_AI_NEWS = 'https://www.artificialintelligence-news.com/artificial-intelligence-news/' 
URL_NATURE = 'https://www.nature.com/latest-news' 

# Пути к CSV
OUTPUT_CSV_PATH_AI = Path("../data_local/ai_news_articles.csv")
OUTPUT_CSV_PATH_NATURE = Path("../data_local/nature.csv")

# Параметры прокрутки
SCROLL_REPEAT = 5
SCROLL_PAUSE = 2
WAIT_TIMEOUT = 15
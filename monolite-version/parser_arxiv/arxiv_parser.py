# parser/arxiv_parser.py

import feedparser
import logging
from typing import List, Dict, Tuple
from datetime import datetime

from config import Config
from ml.classification import ESGClassifier
from ml.summarization import summarize
from db.database import save_article

logger = logging.getLogger(__name__)

# Сообщения логов
PARSING_STARTED = "Starting arXiv parsing..."
ARTICLE_PROCESSED = "Processed article: '{title}' with tags: {tags}"
FAILED_TO_PARSE = "Failed to parse entry: {error}"

class ArxivParser:
    def __init__(self):
        self.classifier = ESGClassifier()
        logger.info("ESG classifier initialized")

    def parse_and_process(self) -> None:
        """Парсит RSS-ленты arXiv и обрабатывает статьи."""
        logger.info(PARSING_STARTED)

        raw_articles = self._fetch_raw_articles()
        texts = self._prepare_texts(raw_articles)
        classifications = self.classifier.predict(texts)

        for entry, tags in zip(raw_articles, classifications):
            try:
                self._process_and_save(entry, tags)
            except Exception as e:
                logger.error(f"Error processing article: {e}", exc_info=True)

    def _fetch_raw_articles(self) -> List[feedparser.FeedParserDict]:
        """Загружает сырые данные из RSS-лент всех категорий."""
        articles = []
        for category in Config.ARXIV_CATEGORIES:
            logger.info(f"Parsing category: {category}")
            feed = feedparser.parse(f"http://arxiv.org/rss/{category}")
            articles.extend(feed.entries[:5])  # Берем по 5 статей с каждой категории
        return articles

    def _prepare_texts(self, entries: List[feedparser.FeedParserDict]) -> List[str]:
        """Формирует входные тексты для классификатора."""
        return [f"{entry.title} {entry.summary}" for entry in entries]

    def _process_and_save(self, entry, tags: List[Tuple[str, float]]) -> None:
        """Обрабатывает один элемент RSS-ленты и сохраняет как статью."""
        article = {
            'id': entry.id.split('/')[-1],
            'title': entry.title,
            'abstract': entry.summary,
            'published': datetime(*entry.published_parsed[:6]).isoformat(),
            'tags': [tag[0] for tag in tags],
            'summary': summarize(entry.summary)
        }

        save_article(article)
        logger.info(ARTICLE_PROCESSED.format(title=article['title'], tags=article['tags']))
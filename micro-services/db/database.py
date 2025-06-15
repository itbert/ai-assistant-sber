# db/database.py

import sqlite3
import logging
from typing import List, Tuple, Optional, Dict
from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# SQL-запросы
CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT,
        abstract TEXT,
        summary TEXT,
        published TEXT,
        tags TEXT
    )
"""

INSERT_OR_REPLACE_ARTICLE_SQL = """
    INSERT OR REPLACE INTO articles VALUES (?, ?, ?, ?, ?, ?)
"""

GET_ARTICLES_BY_TAG_SQL = """
    SELECT id, title, summary 
    FROM articles 
    WHERE tags LIKE ? 
    ORDER BY published DESC 
    LIMIT ?
"""


class ArticleDatabase:
    def __init__(self, db_path: str = Config.DB_FILE):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Создаёт новое соединение с БД."""
        return sqlite3.connect(self.db_path)

    def _initialize_db(self) -> None:
        """Инициализирует структуру БД."""
        try:
            with self._get_connection() as conn:
                logger.info(f"Initializing database at {self.db_path}")
                conn.execute(CREATE_TABLE_SQL)
                logger.info("Database schema created or verified")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            raise

    def save_article(self, article: Dict[str, Any]) -> None:
        """
        Сохраняет или заменяет статью в базе данных.
        
        :param article: словарь с данными статьи
        """
        try:
            with self._get_connection() as conn:
                conn.execute(
                    INSERT_OR_REPLACE_ARTICLE_SQL,
                    (
                        article['id'],
                        article['title'],
                        article['abstract'],
                        article['summary'],
                        article['published'],
                        ','.join(article['tags'])
                    )
                )
                logger.debug(f"Saved article '{article['title']}' to database")
        except sqlite3.Error as e:
            logger.error(f"Database error while saving article: {e}", exc_info=True)

    def get_articles_by_tag(self, tag: str, limit: int = 5) -> List[Tuple[Optional[str], ...]]:
        """
        Возвращает список статей по заданному тегу.
        
        :param tag: тег для фильтрации
        :param limit: максимальное количество статей
        :return: список кортежей (id, title, summary)
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(GET_ARTICLES_BY_TAG_SQL, (f'%{tag}%', limit))
                results = cursor.fetchall()
                logger.info(f"Fetched {len(results)} articles for tag '{tag}'")
                return results
        except sqlite3.Error as e:
            logger.error(f"Database error while fetching articles by tag '{tag}': {e}", exc_info=True)
            return []
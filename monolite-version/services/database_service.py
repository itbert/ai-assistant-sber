# services/database_service.py

import sqlite3
import logging

logger = logging.getLogger(__name__)

def get_articles_from_db(subcategories: list) -> list:
    """
    Получает статьи из БД по списку подкатегорий.
    
    :param subcategories: Список подкатегорий для фильтрации
    :return: Список статей в формате (заголовок, автор/время, описание, ссылка, категория, источник)
    """
    try:
        conn = sqlite3.connect("../Executing/websites.db")
        cursor = conn.cursor()

        # Подготавливаем плейсхолдеры для SQL-запроса
        placeholders = ",".join("?" for _ in subcategories)
        query = f"""
            SELECT headline, time_author, description, link, category, source 
            FROM AllArticles 
            WHERE category IN ({placeholders})
        """

        cursor.execute(query, subcategories)
        articles = cursor.fetchall()
        conn.close()

        logger.info(f"Получено {len(articles)} статей из БД")
        return articles

    except Exception as e:
        logger.error(f"Ошибка при получении статей из БД: {e}")
        return []
# models/user_state.py

from typing import Dict, List, Optional

class UserArticleState:
    def __init__(self):
        # Храним состояние пользователей как словарь: {chat_id: {'category', 'articles', 'current_index'}}
        self.user_data: Dict[int, dict] = {}

    def set_user_data(self, chat_id: int, category: str, articles: List[tuple]):
        """Сохраняет данные пользователя"""
        self.user_data[chat_id] = {
            "category": category,
            "articles": articles,
            "current_index": 0
        }

    def get_user_data(self, chat_id: int) -> Optional[dict]:
        """Получает данные пользователя по chat_id"""
        return self.user_data.get(chat_id)

    def clear_user_data(self, chat_id: int):
        """Очищает данные пользователя"""
        if chat_id in self.user_data:
            del self.user_data[chat_id]

    def update_index(self, chat_id: int, delta: int):
        """Обновляет индекс текущей статьи"""
        user_data = self.get_user_data(chat_id)
        if not user_data:
            return False

        new_index = user_data["current_index"] + delta
        if 0 <= new_index < len(user_data["articles"]):
            user_data["current_index"] = new_index
            return True
        return False
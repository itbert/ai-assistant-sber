# config/config.py

from pathlib import Path

# Путь к токену
TOKEN_PATH = Path("../TOKEN.txt")

# Чтение токена
try:
    with open(TOKEN_PATH, "r") as token_file:
        BOT_TOKEN = token_file.read().strip()
except Exception as e:
    raise RuntimeError(f"Не удалось прочитать токен из файла: {e}")
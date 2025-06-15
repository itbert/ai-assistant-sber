

![Animation - 1744042117243 (1)](https://github.com/user-attachments/assets/33c1fd93-b799-4316-92a7-c78047a21468)

# 🌱 ESG News Analyzer

AI-помощник для аналитиков, автоматизирующий сбор, обработку и категоризацию новостей с ESG-фокусом (Environmental, Social, Governance). Парсит новости, анализирует через NLP-модели и предоставляет удобный интерфейс в Telegram.



<h1 align=center>СберАналитика</h1>

| Разработчик | Чем занимался |
|-----:|---------------|
|     Егор| Куратор              |
|     Савелий| Парсинг              |
|     Андрей| Разработка Telegram-бота               |
|     Ярослав| NLP     |
|     Фёдор| База Данных     |


## 🔍 Возможности

- Парсинг новостей: Автоматический сбор данных с RSS и новостных сайтов
- NLP-обработка:
  - Суммаризация статей (NLTK)
  - Классификация по темам: Окружающая среда, Общество, Корпоративное управление (ESGify)
  - Перевод при необходимости (DeepTranslator)
- Telegram-бот:
  - Фильтрация по временным периодам
  - Поиск по ESG-категориям
  - Экспорт данных в CSV

## 🛠 Технологический стек


Парсинг: BeautifulSoup, Selenium

NLP: ESGify (fine-tuned для ESG), NLTK (токенизация, стемминг, суммаризация)

Перевод: DeepTranslator (поддержка 50+ языков)

Хранение данных: SQLite

Интерфейс: Python-telegram-bot (aiogram)

## 🚀 Установка и запуск
Предварительные требования
Python 3.10+

API-ключи для:

Telegram Bot Father

DeepL (опционально)

Новостных источников

УСТАНОВКА

1. Клонируйте репозиторий:​

git clone https://github.com/S0lerro/AI-Helper-analytics.git

2. Перейдите в директорию проекта:​

cd AI-Helper-analytics

3. Установите необходимые зависимости:​

pip install -r requirements.txt

4. Запустите скрипт обновления базы данных (опционально):

python executor.py

5. Запустите скрипт запуска бота (предварительно заменив токены/API key на свои):

python bot.py

## 📊 Пример работы
Telegram-интерфейс:

[2023-12-01] 🌍 Окружающая среда
📌 Shell сокращает инвестиции в renewables на 12%...
🔗 Читать полностью: example.com/news/123

[2023-11-30] 👥 Общество
📌 Microsoft увеличивает diversity hiring до 40%...
CSV-экспорт:

csv
date,source,category,summary,url
2023-12-01,Reuters,Environment,"Shell cuts renewables...",example.com/123

## ✉️ Контакты
По вопросам интеграции и сотрудничества:

Email: Sakovin1008@gmail.com

Telegram: @Udalova_ES


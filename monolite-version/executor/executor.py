# executor/executor.py

import os
import sqlite3
import pandas as pd
from collections import OrderedDict
from transformers import AutoTokenizer
import torch
import logging
from urllib.parse import urlparse
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Настройка логгирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Пути к CSV-файлам
CSV_PATHS = {
    "ai": "../data_local/ai_news_articles.csv",
    "nature": "../data_local/nature.csv"
}

# Категории для исключения
BANNED_CATEGORIES = [
    'Economic Crime', 'Legal Proceedings & Law Violations', 'Corporate Governance',
    'Values and Ethics', 'Risk Management and Internal Control', 'Strategy Implementation',
    'Disclosure', 'Responsible Investment & Greenwashing', 'Supply Chain (Economic / Governance)',
    'Indigenous People', 'Human Rights', 'Emergencies (Social)', 'Land Acquisition and Resettlement (S)',
    'Data Safety', 'Freedom of Association and Right to Organise', 'Minimum Age and Child Labour',
    'Forced Labour', 'Discrimination', 'Retrenchment', 'Labor Relations Management', 'Supply Chain (Social)'
]


class ESGify(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.id2label = config.id2label
        self.label2id = config.label2id
        self.mpnet = torch.nn.Linear(768, 512)
        self.classifier = torch.nn.Sequential(
            torch.nn.BatchNorm1d(768),
            torch.nn.Linear(768, 512),
            torch.nn.ReLU(),
            torch.nn.BatchNorm1d(512),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(512, 47)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.mpnet(input_ids)
        logits = self.classifier(outputs)
        return torch.sigmoid(logits)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def translate_text(text, chunk_size=3000):
    """Перевод текста на английский"""
    try:
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        translated = []
        for chunk in chunks:
            translated.append(GoogleTranslator(source='auto', target='en').translate(chunk))
        return ' '.join(translated)
    except Exception as e:
        logger.warning(f"Ошибка перевода: {e}")
        return ""


def nlp(text, model, tokenizer, debug=False, title=None):
    """Классификация статьи с помощью модели"""
    translated_text = translate_text(text)
    if not translated_text:
        return False

    if debug:
        print(f"[DEBUG] Title: {title}")
        print(f"[DEBUG] Translated Text: {translated_text[:200]}...")

    encoded = tokenizer.batch_encode_plus(
        [translated_text],
        add_special_tokens=True,
        max_length=140,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    with torch.no_grad():
        results = model(**encoded)

    _, indices = torch.topk(results, k=1)
    top_label = model.id2label[indices.item()]

    if debug:
        logger.info(f"Predicted category: {top_label}")

    if top_label in BANNED_CATEGORIES:
        return False

    return top_label


def summarization(article_text):
    """Создание краткого резюме статьи"""
    words = word_tokenize(article_text.lower())
    stop_words = set(stopwords.words("russian"))
    freq_table = {}

    for word in words:
        if word.isalnum() and word not in stop_words:
            freq_table[word] = freq_table.get(word, 0) + 1

    sentences = sent_tokenize(article_text)
    sentence_value = {}

    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                sentence_value[sentence] = sentence_value.get(sentence, 0) + freq

    sum_values = sum(sentence_value.values())
    average = int(sum_values / len(sentence_value)) if sentence_value else 0

    summary = ""
    for sentence in sentences:
        if sentence_value.get(sentence, 0) > (1.2 * average):
            summary += " " + sentence

    return summary.strip()


def extract_source(url):
    """Извлечение домена из URL"""
    try:
        domain = urlparse(url).netloc
        return domain[4:] if domain.startswith('www.') else domain
    except:
        return "unknown"


def all_nlp(df, fast_mode=False, debug=False):
    """Обработка всех статей"""
    logger.info("Загрузка модели ESGify")
    model = ESGify.from_pretrained('ai-lab/ESGify')
    tokenizer = AutoTokenizer.from_pretrained('ai-lab/ESGify')

    results = []

    for index, row in df.iterrows():
        category = nlp(
            text=str(row['Описание']),
            model=model,
            tokenizer=tokenizer,
            debug=debug,
            title=row['Заголовок']
        )

        if category:
            summary = summarization(str(row['Описание']))
            source = extract_source(row['Ссылка'])

            if debug:
                logger.debug(f"Summary: {summary[:200]}...")
                logger.debug(f"Source: {source}")

            results.append({
                "Категория": category,
                "Заголовок": row['Заголовок'],
                "Время публикации": row['Время публикации'],
                "Описание": summary,
                "Ссылка": f"{row['Заголовок']}: {row['Ссылка']}",
                "Источник": source
            })

    logger.info(f"Классифицировано {len(results)} статей")
    return pd.DataFrame(results)


def run_parsers(debug=False):
    """Запуск парсеров"""
    logger.info("Запуск парсеров")
    parsers = ["parser_rbc.py", "parser_ferra.py", "parser_nature.py"]
    for parser in parsers:
        logger.info(f"Выполняется {parser}...")
        try:
            os.system(f"python ../parsers/{parser}")
        except Exception as e:
            logger.error(f"Ошибка при запуске {parser}: {e}")


def load_to_database(df):
    """Загрузка данных в БД"""
    logger.info("Загрузка данных в БД")
    conn = sqlite3.connect('websites.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS AllArticles')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllArticles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT,
            time_author TEXT,
            description TEXT,
            link TEXT,
            category TEXT,
            source TEXT
        )
    ''')

    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO AllArticles (headline, time_author, description, link, category, source) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['Заголовок'], row['Время публикации'], row['Описание'], row['Ссылка'],
            row['Категория'], row['Источник']
        ))

    conn.commit()
    conn.close()
    logger.info("Данные успешно добавлены в таблицу")


def main():
    """Основная функция запуска"""
    logger.info("Запуск Executor'a")

    update_parsers = input("Обновить парсеры? (y/n): ").lower() == "y"
    fast_mode = input("Включить быстрый режим? (y/n): ").lower() == "y"
    debug_mode = input("Включить режим отладки? (y/n): ").lower() == "y"

    if update_parsers:
        run_parsers(debug=debug_mode)

    # Проверка наличия файлов
    for name, path in CSV_PATHS.items():
        if not os.path.exists(path):
            logger.error(f"Файл {path} не найден.")
            return

    # Чтение CSV
    dfs = [pd.read_csv(path) for path in CSV_PATHS.values()]
    combined_df = pd.concat(dfs, ignore_index=True)

    # Обработка
    processed_df = all_nlp(combined_df, fast_mode=fast_mode, debug=debug_mode)

    # Сохранение
    processed_df.to_csv("svmain.csv", index=False)
    logger.info("Результаты сохранены в svmain.csv")

    # Загрузка в БД
    load_to_database(processed_df)


if __name__ == "__main__":
    main()
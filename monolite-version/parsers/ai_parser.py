# parsers/parser_ai_news.py

import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from config.parser_config import URL_AI_NEWS, OUTPUT_CSV_PATH
from utils.scraper_utils import setup_driver, scroll_page, get_page_soup
from utils.data_utils import parse_date, clean_description, remove_duplicates, save_to_csv

logger = logging.getLogger(__name__)

def extract_headings(soup):
    """Извлечение заголовков статей"""
    headings = soup.find_all("h1", class_="elementor-heading-title elementor-size-default")
    return [h.get_text(strip=True) for h in headings[1:]]

def extract_dates(soup):
    """Извлечение и форматирование дат"""
    time_elements = soup.find_all("span", class_="elementor-icon-list-text")
    return [parse_date(t.get_text(strip=True)) for t in time_elements]

def extract_links(soup):
    """Извлечение ссылок на статьи"""
    headings = soup.find_all("h1", class_="elementor-heading-title elementor-size-default")
    links = []
    for h in headings[1:]:
        link = h.find("a", href=True)
        if link:
            links.append(link["href"])
    return links

def extract_descriptions(links):
    """Получение описаний статей по их ссылкам"""
    descriptions = []
    driver = setup_driver()
    for link in links:
        try:
            soup = get_page_soup(link, driver)
            if not soup:
                descriptions.append("")
                continue

            article_content = soup.find("div", class_="elementor-widget-theme-post-content")
            if article_content:
                paragraphs = article_content.find_all("p")
                description = " ".join([p.get_text(strip=True) for p in paragraphs])
            else:
                description = ""
            descriptions.append(clean_description(description))
        except Exception as e:
            logger.error(f"Ошибка при обработке {link}: {e}")
            descriptions.append("")
    driver.quit()
    return descriptions

def run_parser():
    """Основная функция парсера"""
    logger.info("Запуск парсера AI News")
    driver = setup_driver()
    driver.get(URL_AI_NEWS)
    scroll_page(driver)

    soup = get_page_soup(None, driver)
    if not soup:
        logger.error("Не удалось получить HTML-страницу")
        return

    headings = extract_headings(soup)
    dates = extract_dates(soup)
    links = extract_links(soup)
    descriptions = extract_descriptions(links)

    logger.info(f"Найдено {len(headings)} статей")

    # Создание DataFrame
    df = pd.DataFrame({
        "Заголовок": headings,
        "Время публикации": dates,
        "Описание": descriptions,
        "Ссылка": links
    })

    df = remove_duplicates(df)
    save_to_csv(df, OUTPUT_CSV_PATH)
    driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run_parser()

# parsers/parser_nature.py

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from config.parser_config import URL_NATURE, OUTPUT_CSV_PATH_NATURE
from utils.scraper_utils import setup_driver, scroll_page, get_page_soup
from utils.data_utils import clean_description, remove_duplicates, save_to_csv
import logging
import time

logger = logging.getLogger(__name__)

def extract_headings(soup):
    """Извлечение заголовков статей"""
    headings = []
    for item in soup.find_all("div", class_="c-article-item__copy"):
        h3 = item.find("h3")
        if h3:
            headings.append(h3.get_text(strip=True))
    logger.info(f"Найдено {len(headings)} заголовков")
    return headings

def extract_dates(soup):
    """Извлечение дат публикации"""
    dates = []
    for item in soup.find_all("div", class_="c-article-item__footer"):
        date_span = item.find("span", class_="c-article-item__date")
        if date_span:
            dates.append(date_span.get_text(strip=True))
    return dates

def extract_links(soup):
    """Извлечение ссылок на статьи"""
    links = []
    base_url = "https://www.nature.com" 
    for item in soup.find_all("div", class_="c-article-item__content c-article-item--with-image"):
        a_tag = item.find("a", href=True)
        if a_tag:
            links.append(base_url + a_tag["href"])
    return links

def extract_descriptions(links):
    """Получение описаний по ссылкам"""
    descriptions = []
    driver = setup_driver()
    for link in links:
        try:
            # Открытие страницы
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Принятие cookie-политики
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        ".cc-button.cc-button--secondary.cc-button--contrast.cc-banner__button.cc-banner__button-accept"
                    ))
                )
                cookie_button.click()
                time.sleep(1)
            except Exception as e:
                logger.debug(f"Cookie banner не найден или ошибка при клике: {e}")

            # Парсинг описания
            paragraphs = driver.find_elements(By.CLASS_NAME, "article__teaser")
            description = " ".join([p.text.strip() for p in paragraphs])
            descriptions.append(clean_description(description))

        except Exception as e:
            logger.error(f"Ошибка при обработке {link}: {e}")
            descriptions.append("")
    driver.quit()
    return descriptions

def run_parser():
    """Основная функция парсера для Nature.com"""
    logger.info("Запуск парсера Nature.com")

    # Настройка драйвера и загрузка страницы
    driver = setup_driver()
    driver.get(URL_NATURE)

    # Прокрутка страницы
    scroll_page(driver)

    # Получение HTML
    soup = get_page_soup(None, driver)
    if not soup:
        logger.error("Не удалось получить HTML-страницу")
        return

    # Извлечение данных
    headings = extract_headings(soup)
    dates = extract_dates(soup)
    links = extract_links(soup)
    descriptions = extract_descriptions(links)

    # Создание DataFrame
    df = pd.DataFrame({
        "Заголовок": headings,
        "Время публикации": dates,
        "Описание": descriptions,
        "Ссылка": links
    })

    # Очистка от дубликатов и сохранение
    df = remove_duplicates(df)
    save_to_csv(df, OUTPUT_CSV_PATH_NATURE)
    driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run_parser()
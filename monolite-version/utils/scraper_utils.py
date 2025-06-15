# utils/scraper_utils.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import logging
from config.parser_config import CHROME_OPTIONS, SCROLL_REPEAT, SCROLL_PAUSE, WAIT_TIMEOUT

logger = logging.getLogger(__name__)

def setup_driver():
    """Создание и настройка WebDriver"""
    options = Options()
    for arg, value in CHROME_OPTIONS.items():
        if value:
            options.add_argument(f"--{arg}")
    return webdriver.Chrome(options=options)

def scroll_page(driver):
    """Прокрутка страницы для загрузки всех статей"""
    try:
        for _ in range(SCROLL_REPEAT):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE)
        logger.info("Страница успешно прокручена")
    except Exception as e:
        logger.warning(f"Ошибка при прокрутке: {e}")

def get_page_soup(url, driver=None):
    """Получение BeautifulSoup объекта по URL"""
    own_driver = False
    if not driver:
        driver = setup_driver()
        own_driver = True
    try:
        driver.get(url)
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html = driver.page_source
        if own_driver:
            driver.quit()
        return BeautifulSoup(html, "lxml")
    except Exception as e:
        logger.error(f"Ошибка при получении страницы: {e}")
        if own_driver:
            driver.quit()
        return None
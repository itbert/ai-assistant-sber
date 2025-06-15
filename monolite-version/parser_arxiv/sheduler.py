# parser/scheduler.py

import time
import logging
from typing import Optional

from config import Config
from parser.arxiv_parser import ArxivParser

logger = logging.getLogger(__name__)


class ParserScheduler:
    """Запускает парсинг arXiv периодически."""

    def __init__(self):
        self.parser = ArxivParser()
        self.running = False

    def start(self) -> None:
        """Запускает бесконечный цикл парсинга."""
        self.running = True
        logger.info("Starting periodic parser with interval %d sec", Config.PARSE_INTERVAL)

        try:
            while self.running:
                try:
                    self.parser.parse_and_process()
                except Exception as e:
                    logger.error("Error during parsing: %s", e, exc_info=True)
                self._wait_with_shutdown_check()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Останавливает выполнение планировщика."""
        logger.info("Stopping parser scheduler...")
        self.running = False

    def _wait_with_shutdown_check(self, chunk: int = 10) -> None:
        """
        Позволяет прервать sleep при остановке.
        Разбивает ожидание на части, чтобы проверять running флаг.
        """
        total_wait = 0
        while self.running and total_wait < Config.PARSE_INTERVAL:
            time.sleep(chunk)
            total_wait += chunk
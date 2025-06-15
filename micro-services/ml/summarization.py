# ml/summarization.py

from transformers import pipeline, Pipeline
from typing import Optional
import logging

from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TextSummarizer:
    def __init__(self, model_name: str = Config.SUMMARIZATION_MODEL):
        self.model_name = model_name
        self.summarizer_pipeline: Optional[Pipeline] = None
        self.max_input_length = 1024
        self.init_pipeline()

    def init_pipeline(self) -> None:
        """Инициализирует пайплайн суммаризатора."""
        if not self.summarizer_pipeline:
            try:
                logger.info(f"Loading summarization model '{self.model_name}'")
                self.summarizer_pipeline = pipeline("summarization", model=self.model_name)
                logger.info("Summarization model successfully loaded")
            except Exception as e:
                logger.error(f"Failed to load summarization model: {e}", exc_info=True)
                raise

    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30
    ) -> str:
        """
        Суммирует входной текст.
        
        :param text: исходный текст для суммаризации
        :param max_length: максимальная длина суммы
        :param min_length: минимальная длина суммы
        :return: суммированный текст
        """
        if not self.summarizer_pipeline:
            raise RuntimeError("Summarizer not initialized. Call init_pipeline() first.")

        try:
            if len(text) > self.max_input_length:
                logger.warning(f"Input text is longer than {self.max_input_length}, truncating...")
                text = text[:self.max_input_length] + " [truncated]"

            result = self.summarizer_pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return result[0]['summary_text']
        except Exception as e:
            logger.error(f"Error during summarization: {e}", exc_info=True)
            return "[Error: failed to generate summary]"
# utils/ner_preprocessing.py

from flair.models import SequenceTagger
from flair.data import Sentence
from typing import Optional
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class NERTagger:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tagger: Optional[SequenceTagger] = None
        self.load_model()

    def load_model(self) -> None:
        """Загружает модель NER."""
        if self.tagger is None:
            try:
                logger.info(f"Loading NER model '{self.model_name}'")
                self.tagger = SequenceTagger.load(self.model_name)
                logger.info("NER model successfully loaded")
            except Exception as e:
                logger.error(f"Failed to load NER model '{self.model_name}': {e}", exc_info=True)
                raise

    def mask_entities(self, text: str) -> str:
        """Маскирует сущности в тексте."""
        if not self.tagger:
            raise RuntimeError("NER tagger is not initialized. Call load_model() first.")

        sentence = Sentence(text)
        self.tagger.predict(sentence)

        masked_tokens = []
        for token in sentence:
            ner_tag = token.get_tag('ner').value
            if ner_tag != 'O':
                try:
                    entity_type = ner_tag.split('-')[1]
                    masked_tokens.append(f"[{entity_type}]")
                except IndexError:
                    masked_tokens.append("[UNKNOWN]")
            else:
                masked_tokens.append(token.text)

        return " ".join(masked_tokens)


# Глобальный экземпляр для удобства использования
ner_tagger: Optional[NERTagger] = None

def init_ner_tagger(model_name: str) -> None:
    """Инициализирует глобальный NER-теггер."""
    global ner_tagger
    if ner_tagger is None:
        ner_tagger = NERTagger(model_name)

def mask_entities(text: str) -> str:
    """Маскирует сущности в тексте с использованием глобального теггера."""
    if ner_tagger is None:
        raise RuntimeError("NER tagger not initialized. Call init_ner_tagger() first.")
    return ner_tagger.mask_entities(text)
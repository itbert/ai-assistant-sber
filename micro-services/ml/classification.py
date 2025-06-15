# ml/classification.py

import torch
from transformers import MPNetPreTrainedModel, MPNetModel, AutoTokenizer
from collections import OrderedDict
from typing import List, Tuple, Dict, Any, Optional

from config import Config
from utils.ner_preprocessing import init_ner_tagger, mask_entities

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class ESGify(MPNetPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.mpnet = MPNetModel(config, add_pooling_layer=False)
        self.id2label = config.id2label
        self.label2id = config.label2id
        self.classifier = torch.nn.Sequential(OrderedDict([
            ('norm', torch.nn.BatchNorm1d(768)),
            ('linear', torch.nn.Linear(768, 512)),
            ('act', torch.nn.ReLU()),
            ('batch_n', torch.nn.BatchNorm1d(512)),
            ('drop_class', torch.nn.Dropout(0.2)),
            ('class_l', torch.nn.Linear(512, 47))
        ]))

    def forward(self, input_ids, attention_mask):
        outputs = self.mpnet(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.classifier(mean_pooling(outputs.last_hidden_state, attention_mask))
        return torch.sigmoid(logits)


class ESGClassifier:
    def __init__(self, model_name: str = Config.ESGIFY_MODEL_NAME):
        logger.info(f"Loading ESG classifier from {model_name}")
        try:
            self.model = ESGify.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model.eval()
            init_ner_tagger(Config.NER_MODEL)
            logger.info("ESG classifier successfully initialized")
        except Exception as e:
            logger.error(f"Failed to load ESG classifier: {e}", exc_info=True)
            raise

    def predict(
        self,
        texts: List[str],
        top_k: int = 3,
        threshold: float = Config.CLASSIFICATION_THRESHOLD
    ) -> List[List[Tuple[str, float]]]:
        """
        Предсказывает теги для списка текстов.
        
        :param texts: список текстов
        :param top_k: количество топ-тегов
        :param threshold: порог вероятности для фильтрации
        :return: список списков пар (тег, вероятность)
        """
        processed_texts = [self._mask_entities(text) for text in texts]
        inputs = self._tokenize(processed_texts)
        predictions = self._run_model(inputs)
        return self._process_predictions(predictions, top_k, threshold)

    def _mask_entities(self, text: str) -> str:
        """Применяет маскирование сущностей к тексту."""
        return mask_entities(text)

    def _tokenize(self, texts: List[str]) -> Dict[str, torch.Tensor]:
        """Токенизирует входные тексты."""
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
            return_attention_mask=True
        )

    def _run_model(self, inputs: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Запускает модель на предикт."""
        with torch.no_grad():
            return self.model(**inputs)

    def _process_predictions(
        self,
        outputs: torch.Tensor,
        top_k: int,
        threshold: float
    ) -> List[List[Tuple[str, float]]]:
        """Обрабатывает вывод модели: извлекает теги выше порога."""
        results = []
        for probs in outputs:
            top_probs, top_indices = torch.topk(probs, k=top_k)
            labels = [
                (self.model.id2label[idx.item()], prob.item())
                for idx, prob in zip(top_indices, top_probs)
                if prob > threshold
            ]
            results.append(labels)
        return results
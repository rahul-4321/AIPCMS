from app.core.config import settings
from transformers import pipeline
import torch
from typing import List, Dict

class NLPServices:

    def __init__(self, model_name: str = settings.NLP_MODEL_NAME):
        device = 0 if torch.cuda.is_available() else -1
        self.pipe = pipeline("text-classification", model=model_name, device=device)

    def analyze_text(self, text: str) -> Dict[str, float]:
        results = self.pipe(text, top_k=None)
        scores ={res['label']: res['score'] for res in results}
        return scores

    def is_toxic(self, text:str, threshold: float=settings.MODERATION_THRESHOLD) -> bool:
        scores=self.analyze_text(text)
        toxic_labels=['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        for label in toxic_labels:
            if scores.get(label, 0) > threshold:
                return True
        return False

nlp_service = NLPServices()
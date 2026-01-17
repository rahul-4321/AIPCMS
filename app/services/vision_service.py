from transformers import pipeline
import torch
from typing import List, Dict
from app.core.config import settings
import io
from PIL import Image

class VisionService:
    def __init__(self, model_name: str =settings.VISION_MODEL_NAME):
        device =0 if torch.cuda.is_available() else -1
        self.pipe = pipeline("image-classification", model=model_name, device=device)
    
    def analyze_image(self, image_bytes: bytes) -> Dict[str, float]:

        image = Image.open(io.BytesIO(image_bytes))
        results = self.pipe(image)
        scores = {res['label']: res['score'] for res in results}
        return scores
    
    def is_unsafe(self, image_bytes:bytes, threshold=settings.MODERATION_THRESHOLD) -> bool:
        scores = self.analyze_image(image_bytes)
        return scores.get('nsfw',0) > threshold

vision_service=VisionService()
from fastapi import APIRouter, Depends, HTTPException
from app.services.nlp_service import nlp_service
from app.database import get_db
from app.models import ModerationLog
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.services.user_service import user_service

router = APIRouter()

class TextRequest(BaseModel):
    text: str
    user_id: str

@router.post("/analyze")
async def analyze_text(request: TextRequest, db: Session = Depends(get_db)):
    # Check if user is blocked
    user_service.check_if_blocked(db, request.user_id)
    
    scores = nlp_service.analyze_text(request.text)
    is_safe = not nlp_service.is_toxic(request.text)
    
    log = ModerationLog(
        user_id=request.user_id,
        content_type="text",
        original_content=request.text[:200],  # Shortened
        is_safe=1 if is_safe else 0,
        scores=scores
    )
    db.add(log)
    db.commit()
    
    if not is_safe:
        user_service.record_violation(db, request.user_id, "text")
    
    return {
        "is_safe": is_safe,
        "scores": scores
    }

from fastapi import APIRouter, Depends, HTTPException
from app.services.url_service import url_service
from app.services.user_service import user_service
from app.database import get_db
from app.models import ModerationLog
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

router = APIRouter()

class URLRequest(BaseModel):
    urls: List[str]
    user_id: str

@router.post("/analyze")
async def analyze_urls(request: URLRequest, db: Session = Depends(get_db)):
    # Check if user is blocked
    user_service.check_if_blocked(db, request.user_id)
    
    results = url_service.check_urls(request.urls)
    
    # Log the request
    is_safe = all(res["is_safe"] for res in results)
    
    log = ModerationLog(
        user_id=request.user_id,
        content_type="url",
        original_content=", ".join(request.urls)[:500],
        is_safe=1 if is_safe else 0,
        scores=results
    )
    db.add(log)
    db.commit()
    
    return {
        "is_safe": is_safe,
        "results": results
    }

from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.vision_service import vision_service
from app.services.user_service import user_service
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import ModerationLog

router = APIRouter()

@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    user_id: str =Form(...),
    db: Session = Depends(get_db)
):
    
    user_service.check_if_blocked(db, user_id)

    image_bytes = await file.read()
    scores = vision_service.analyze_image(image_bytes)
    is_safe = not vision_service.is_unsafe(image_bytes)

    log= ModerationLog(
        user_id=user_id,
        content_type="image",
        original_content=file.filename,
        is_safe=1 if is_safe else 0,
        scores=scores
    )
    db.add(log) #add log to db
    db.commit()
    
    if not is_safe:
        user_service.record_violation(db, user_id, "image")
    
    return {
        "filename": file.filename,
        "is_safe": is_safe,
        "scores": scores
    }
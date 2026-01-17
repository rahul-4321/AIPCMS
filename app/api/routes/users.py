from fastapi import APIRouter, Depemds, HTTPException
from app.models import BlockedUser
from app.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

router = APIRouter()

class BlockRequest(BaseModel):
    user_id: str
    reason: str

@router.post("block")
async def block_user(request: BlockRequest, db: Session = Depends(get_db)):
    exists = db.query(BlockedUser).filter(BlockedUser.user_id == request.user_id).first()

    if exists:
        return {"message": f"User {request.user_id} is already blocked"}
    
    db.add(BlockedUser(
        user_id=request.user_id, 
        reason=request.reason)
        )
    db.commit()
    return {"message": f"User {request.user_id} has been blocked"}


@router.post("unblock/{user_id}")
async def unblock_user(user_id: str, db: Session = Depends(get_db)):
    blocked = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
    if not blocked:
        raise HTTPException(status_code==404, detail="User not found in block list")
    
    db.delete(blocked)
    db.commit()
    return {"message": f"User {user_id} has been unblocked"}

@router.get("/blocked", response_model=List[str])
async def list_blocked_users(db: Session = Depends(get_db)):
    users=db.query(BlockedUser).all()
    return [user.user_id for user in users]
    
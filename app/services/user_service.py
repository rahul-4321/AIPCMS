from sqlalchemy.orm import Session
from app.models import BlockedUser
from fastapi import HTTPException

class UserService:
    @staticmethod
    def check_if_blocked(db: Session, user_id:str):
        if not user_id:
            return
        
        is_blocked = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
        
        if is_blocked:
            raise HTTPException(
                status_code = 403,
                detail = f'User {user_id} is blockeed. Reason: {is_blocked.reason}'
            )

    @staticmethod
    def record_violation(db:Session, user_id:str, content_type:str):

        if not user_id:
            return
        
        from app.models import ModerationLog, BlockedUser

        toxic_count = db.query(ModerationLog).filter(
            ModerationLog.user_id ==user_id,
            ModerationLog.is_safe == 0
        ).count()

        if toxic_count >= settings.MAX_TOXIC_CONTENT:
            existing = db.query(BlockedUser).filter(BlockedUser.user_id ==user_id).first()

            if not existing:
                new_block = BlockedUser(
                    user_id = user_id,
                    reason = f'Auto-blocked after {toxic_count} toxic {content_type} posts'
                )
                db.add(new_block)
                db.commit()

                return True
        return False

user_service = UserService()
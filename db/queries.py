from sqlalchemy.orm import Session
from api.models.user import User

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()
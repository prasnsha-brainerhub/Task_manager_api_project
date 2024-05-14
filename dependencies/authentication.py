from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.session import get_db
from passlib.context import CryptContext
from db.crud import get_user_by_username, get_admin_by_username
import jwt
from db.models import Admin, User

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

print(oauth2_scheme, "oauth2_scheme")

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin_by_username(db, username)

    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

async def get_current_access_token(token: str = Depends(oauth2_scheme)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_token(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow() > datetime.fromtimestamp(payload.get("exp")):
            return False
        return True
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(token, "token--")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload, "payload")
        username: str = payload.get("sub")
        role: str = payload.get("role")
        print(username, "username-", role, "role")
    except:
        raise credentials_exception
    
    if role == "User":
        print(role, "user role")
        user = get_user_by_username(db, username=username) 
        print("user")
    else:
        print(role, "admin role")
        user = get_admin_by_username(db, username=username)


    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


def is_admin(admin: Admin, db: Session):
    return get_admin_by_username(db=db, username=admin.username) is not None


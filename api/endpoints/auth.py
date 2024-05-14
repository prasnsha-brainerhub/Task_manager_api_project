from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from db.session import get_db
from utils.security import create_access_token
from dependencies.authentication import authenticate_user,authenticate_admin, get_current_user
from api.models.user import UserCreate
from db.crud import get_user_by_username, create_user, get_admin_by_username, create_admin
from passlib.context import CryptContext

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/user/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = pwd_context.hash(user.password)
    db_user = create_user(db=db, user=user, hashed_password=hashed_password)
    return db_user

@router.post("/admin/register")
async def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_admin_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = pwd_context.hash(user.password)
    db_admin = create_admin(db=db, user=user, hashed_password=hashed_password)
    return db_admin

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role" : "User"},
            expires_delta=access_token_expires
        )
        return {"token_type": "bearer", "access_token": access_token}
    
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if admin:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": admin.username, "role" : "Admin"},
            expires_delta=access_token_expires
        )
        return {"token_type": "bearer", "access_token": access_token, "message": "Admin login successful", "user_type": "admin"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

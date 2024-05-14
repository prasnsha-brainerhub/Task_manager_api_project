from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password : str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRegistration(BaseModel):
    username: str
    password: str
    

class Task(BaseModel):
    username: str
    tasks: list

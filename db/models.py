from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:12345@db:5432/Task_manager")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    task_id =  Column(Integer, ForeignKey("tasks.task_id"))
    tasks = relationship("Task")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    

Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session
from api.models.task import Task, TaskCreate, TaskUpdate
from db.models import Task as TaskModel, User, Admin
from api.models.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()


def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, user: UserCreate, hashed_password: str):
    db_admin = Admin(username=user.username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


async def create_task(db: Session, task_data: TaskCreate):
    db_task = TaskModel( **task_data.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Task:
    return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()


def get_all_task(db: Session):
    return db.query(TaskModel).all()  


def update_task_in_db(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        return None


def delete_task_in_db(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.models.task import TaskCreate, TaskUpdate
from db.session import get_db
from db.crud import get_all_task, create_task,update_task_in_db, delete_task_in_db
from db.models import User, Admin
from dependencies.authentication import get_current_active_user, oauth2_scheme, is_admin,verify_token, get_current_access_token


router = APIRouter()


@router.get("/get")
async def get_tasks(db: Session = Depends(get_db), user: User = Depends(oauth2_scheme)):
    tasks = get_all_task(db)
    return tasks

@router.post("/create")
async def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return await create_task(db=db, task_data=task)

@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user: Admin = Depends(get_current_active_user),
):
    if not is_admin(user, db):
        raise HTTPException(status_code=403, detail="Only admin can update tasks.")
    db_task = update_task_in_db(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: Admin = Depends(get_current_active_user),
):
    if not is_admin(user, db):
        raise HTTPException(status_code=403, detail="Only admin can delete tasks.")
    db_task = delete_task_in_db(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

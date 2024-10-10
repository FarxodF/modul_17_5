from fastapi import APIRouter, Depends, status, HTTPException
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from app.backend.db_depends import get_db
from app.backend import db
from typing import Annotated
from app.models.user_2 import User
from app.models.task_2 import Task
from app.schemas import CreateUser, UpdateUser, CreateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from app.backend.db_depends import get_db



router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
def all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@router.get("/{task_id}")
def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task was not found"
    )
    return task


@router.post("/create")
def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    new_task = Task(task.dict(),
                    user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put("/update/{task_id}")
def update_task(task_id: int, task: CreateTask, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    for key, value in task.dict().items():
        setattr(existing_task, key, value)
    db.commit()
    db.refresh(existing_task)
    return existing_task


@router.delete("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    db.delete(task)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successful'
    }

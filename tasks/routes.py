from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from enum import Enum
from datetime import date
from database.database import SessionLocal
from database.models import (
    Task,
    KanbanColumn,
    Board,
    Workspace,
    ActivityLog
)

from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =========================
# ENUM VALIDATION
# =========================

class PriorityEnum(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class StatusEnum(str, Enum):
    todo = "To Do"
    progress = "In Progress"
    done = "Done"



# =========================
# DATABASE CONNECTION
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# =========================
# CREATE TASK
# =========================

@router.post("/")
def create_task(
    title: str,
    description: str = "",
    priority: PriorityEnum = PriorityEnum.Medium,
    status: StatusEnum = StatusEnum.todo,
    due_date: date | None = None,
    assigned_user_id: int | None = None,
    column_id: int = 0,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    column = db.query(KanbanColumn).filter(
        KanbanColumn.id == column_id
    ).first()

    if not column:
        return {"message": "Column not found"}


    board = db.query(Board).filter(
        Board.id == column.board_id
    ).first()


    if not board:
        return {"message": "Board not found"}


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()


    if not workspace:
        return {"message": "Access denied"}



    task = Task(
        title=title,
        description=description,
        priority=priority.value,
        status=status.value,
        due_date=due_date,
        assigned_user_id=assigned_user_id,
        column_id=column_id
    )


    db.add(task)
    db.commit()
    db.refresh(task)



    activity = ActivityLog(
        action=f"Created task: {task.title}",
        workspace_id=workspace.id,
        board_id=board.id,
        task_id=task.id,
        user_id=current_user.id
    )


    db.add(activity)
    db.commit()



    return {
        "message": "Task created successfully",
        "task_id": task.id,
        "title": task.title,
        "priority": task.priority,
        "status": task.status
    }




# =========================
# GET TASKS
# =========================

@router.get("/")
def get_tasks(
    column_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).filter(
        Task.column_id == column_id
    ).all()


    return tasks




# =========================
# GET ONE TASK
# =========================

@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()


    if not task:
        return {
            "message": "Task not found"
        }


    return task





# =========================
# UPDATE TASK
# =========================

@router.put("/{task_id}")
def update_task(
    task_id: int,
    title: str,
    description: str,
    priority: PriorityEnum,
    status: StatusEnum,
    due_date: str,
    assigned_user_id: int | None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()


    if not task:
        return {
            "message": "Task not found"
        }



    task.title = title
    task.description = description
    task.priority = priority.value
    task.status = status.value
    task.due_date = due_date
    task.assigned_user_id = assigned_user_id



    column = db.query(KanbanColumn).filter(
        KanbanColumn.id == task.column_id
    ).first()


    board = db.query(Board).filter(
        Board.id == column.board_id
    ).first()


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id
    ).first()



    db.commit()
    db.refresh(task)



    activity = ActivityLog(
        action=f"Updated task: {task.title}",
        workspace_id=workspace.id,
        board_id=board.id,
        task_id=task.id,
        user_id=current_user.id
    )


    db.add(activity)
    db.commit()



    return {
        "message": "Task updated successfully"
    }





# =========================
# MOVE TASK
# =========================

@router.put("/{task_id}/move")
def move_task(
    task_id: int,
    new_column_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()


    if not task:
        return {
            "message": "Task not found"
        }



    old_column = task.column_id



    new_column = db.query(KanbanColumn).filter(
        KanbanColumn.id == new_column_id
    ).first()


    if not new_column:
        return {
            "message": "Column not found"
        }



    board = db.query(Board).filter(
        Board.id == new_column.board_id
    ).first()


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id
    ).first()



    task.column_id = new_column_id

    db.commit()



    activity = ActivityLog(
        action=f"Moved task {task.title} from column {old_column} to {new_column_id}",
        workspace_id=workspace.id,
        board_id=board.id,
        task_id=task.id,
        user_id=current_user.id
    )


    db.add(activity)
    db.commit()



    return {
        "message": "Task moved successfully"
    }





# =========================
# DELETE TASK
# =========================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()


    if not task:
        return {
            "message": "Task not found"
        }



    title = task.title



    column = db.query(KanbanColumn).filter(
        KanbanColumn.id == task.column_id
    ).first()


    board = db.query(Board).filter(
        Board.id == column.board_id
    ).first()


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id
    ).first()



    db.delete(task)
    db.commit()



    activity = ActivityLog(
        action=f"Deleted task: {title}",
        workspace_id=workspace.id,
        board_id=board.id,
        user_id=current_user.id
    )


    db.add(activity)
    db.commit()



    return {
        "message": "Task deleted successfully"
    }
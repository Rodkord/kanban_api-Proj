from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.database import get_db
from database.models import Task, Board, Workspace


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Dashboard Statistics
@router.get("/stats")
def dashboard_statistics(
    db: Session = Depends(get_db)
):

    total_tasks = db.query(Task).count()

    completed_tasks = (
        db.query(Task)
        .filter(Task.status == "Done")
        .count()
    )

    pending_tasks = (
        db.query(Task)
        .filter(Task.status != "Done")
        .count()
    )

    total_boards = db.query(Board).count()

    total_workspaces = db.query(Workspace).count()


    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_boards": total_boards,
        "total_workspaces": total_workspaces
    }



# Task Analytics
@router.get("/task-analytics")
def task_analytics(
    db: Session = Depends(get_db)
):

    status_result = (
        db.query(
            Task.status,
            func.count(Task.id)
        )
        .group_by(Task.status)
        .all()
    )


    priority_result = (
        db.query(
            Task.priority,
            func.count(Task.id)
        )
        .group_by(Task.priority)
        .all()
    )


    return {

        "status_distribution": [
            {
                "status": status,
                "count": count
            }
            for status, count in status_result
        ],

        "priority_distribution": [
            {
                "priority": priority,
                "count": count
            }
            for priority, count in priority_result
        ]
    }
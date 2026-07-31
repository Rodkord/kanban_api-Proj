from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import ActivityLog, Workspace
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


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
# GET ALL ACTIVITIES
# =========================

@router.get("/")
def get_activities(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    activities = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).all()


    return activities



# =========================
# GET WORKSPACE ACTIVITIES
# =========================

@router.get("/workspace/{workspace_id}")
def get_workspace_activities(
    workspace_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()


    if not workspace:
        return {
            "message": "Access denied"
        }


    activities = db.query(ActivityLog).filter(
        ActivityLog.workspace_id == workspace_id
    ).all()


    return activities



# =========================
# GET TASK HISTORY
# =========================

@router.get("/task/{task_id}")
def get_task_history(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    activities = db.query(ActivityLog).filter(
        ActivityLog.task_id == task_id
    ).all()


    return {
        "task_id": task_id,
        "history": activities
    }
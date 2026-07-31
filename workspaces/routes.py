from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import Workspace
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
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
# CREATE WORKSPACE
# =========================

@router.post("/")
def create_workspace(
    name: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    workspace = Workspace(
        name=name,
        owner_id=current_user.id
    )

    db.add(workspace)

    db.commit()

    db.refresh(workspace)

    return {

        "message": "Workspace created successfully",

        "workspace_id": workspace.id,

        "name": workspace.name

    }
@router.get("/")
def get_workspaces(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    workspaces = db.query(Workspace).filter(
        Workspace.owner_id == current_user.id
    ).all()

    return workspaces


@router.get("/{workspace_id}")
def get_workspace(
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
            "message": "Workspace not found"
        }

    return workspace

@router.delete("/{workspace_id}")
def delete_workspace(
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
            "message": "Workspace not found"
        }

    db.delete(workspace)
    db.commit()

    return {
        "message": "Workspace deleted successfully"
    }
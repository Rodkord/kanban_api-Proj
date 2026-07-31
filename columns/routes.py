from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import KanbanColumn, Board, Workspace
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/columns",
    tags=["Columns"]
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
# CREATE COLUMN
# =========================

@router.post("/")
def create_column(
    name: str,
    board_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    board = db.query(Board).filter(
        Board.id == board_id
    ).first()

    if not board:
        return {
            "message": "Board not found"
        }


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if not workspace:
        return {
            "message": "Board not found"
        }


    column = KanbanColumn(
        name=name,
        board_id=board_id
    )

    db.add(column)
    db.commit()
    db.refresh(column)


    return {
        "message": "Column created successfully",
        "column_id": column.id,
        "name": column.name,
        "board_id": column.board_id
    }


# =========================
# GET COLUMNS
# =========================

@router.get("/")
def get_columns(
    board_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    board = db.query(Board).filter(
        Board.id == board_id
    ).first()

    if not board:
        return {
            "message": "Board not found"
        }


    workspace = db.query(Workspace).filter(
        Workspace.id == board.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if not workspace:
        return {
            "message": "Board not found"
        }


    columns = db.query(KanbanColumn).filter(
        KanbanColumn.board_id == board_id
    ).all()


    return columns
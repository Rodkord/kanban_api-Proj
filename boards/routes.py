from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import Board
from auth.dependencies import get_current_user
from auth.permissions import require_member, require_admin


router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
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
# CREATE BOARD
# =========================

@router.post("/")
def create_board(
    name: str,
    workspace_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not require_member(workspace_id, current_user, db):
        return {
            "message": "Access denied"
        }

    board = Board(
        name=name,
        workspace_id=workspace_id
    )

    db.add(board)
    db.commit()
    db.refresh(board)

    return {
        "message": "Board created successfully",
        "board_id": board.id,
        "name": board.name,
        "workspace_id": board.workspace_id
    }


# =========================
# GET BOARDS
# =========================

@router.get("/")
def get_boards(
    workspace_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not require_member(workspace_id, current_user, db):
        return {
            "message": "Access denied"
        }

    boards = db.query(Board).filter(
        Board.workspace_id == workspace_id
    ).all()

    return boards


# =========================
# GET ONE BOARD
# =========================

@router.get("/{board_id}")
def get_board(
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

    if not require_member(board.workspace_id, current_user, db):
        return {
            "message": "Access denied"
        }

    return board


# =========================
# DELETE BOARD
# =========================

@router.delete("/{board_id}")
def delete_board(
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

    if not require_admin(board.workspace_id, current_user, db):
        return {
            "message": "Access denied"
        }

    db.delete(board)
    db.commit()

    return {
        "message": "Board deleted successfully"
    }
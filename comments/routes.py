from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import Comment, Task , User
from auth.dependencies import get_current_user
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
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
# CREATE COMMENT
# =========================

@router.post("/")
def create_comment(
    content: str,
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


    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=current_user.id
    )


    db.add(comment)
    db.commit()
    db.refresh(comment)


    return {
        "message": "Comment created successfully",
        "comment_id": comment.id,
        "content": comment.content,
        "task_id": comment.task_id,
        "user_id": comment.user_id
    }



# =========================
# GET COMMENTS OF TASK
# =========================

@router.get("/{task_id}")
def get_comments(
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


    comments = db.query(Comment).filter(
        Comment.task_id == task_id
    ).all()


    result = []

    for comment in comments:

        user = db.query(User).filter(
            User.id == comment.user_id
        ).first()


        result.append({

            "comment_id": comment.id,

            "content": comment.content,

            "user": user.username if user else "Unknown",

            "created_at": comment.created_at

        })


    return result


# =========================
# DELETE COMMENT
# =========================

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()


    if not comment:
        return {
            "message": "Comment not found"
        }


    if comment.user_id != current_user.id:
        return {
            "message": "You cannot delete this comment"
        }


    db.delete(comment)
    db.commit()


    return {
        "message": "Comment deleted successfully"
    }
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import WorkspaceMember, Workspace, User
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/members",
    tags=["Members"]
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
# ADD MEMBER TO WORKSPACE
# =========================

@router.post("/")
def add_member(
    workspace_id: int,
    user_id: int,
    role: str = "Member",
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Check workspace owner
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()


    if not workspace:
        return {
            "message": "Workspace not found or access denied"
        }


    # Check user exists
    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if not user:
        return {
            "message": "User not found"
        }


    # Check if already member
    existing = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first()


    if existing:
        return {
            "message": "User already a member"
        }


    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role=role
    )


    db.add(member)
    db.commit()
    db.refresh(member)


    return {

        "message": "Member added successfully",

        "member_id": member.id,

        "user_id": member.user_id,

        "workspace_id": member.workspace_id,

        "role": member.role

    }



# =========================
# GET WORKSPACE MEMBERS
# =========================

@router.get("/{workspace_id}")
def get_members(
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
            "message": "Workspace not found or access denied"
        }


    members = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id
    ).all()


    result = []


    for member in members:

        user = db.query(User).filter(
            User.id == member.user_id
        ).first()


        result.append({

            "member_id": member.id,

            "username": user.username if user else "Unknown",

            "user_id": member.user_id,

            "role": member.role

        })


    return result



# =========================
# REMOVE MEMBER
# =========================

@router.delete("/{member_id}")
def remove_member(
    member_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.id == member_id
    ).first()


    if not member:
        return {
            "message": "Member not found"
        }


    workspace = db.query(Workspace).filter(
        Workspace.id == member.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()


    if not workspace:
        return {
            "message": "Access denied"
        }


    db.delete(member)
    db.commit()


    return {
        "message": "Member removed successfully"
    }
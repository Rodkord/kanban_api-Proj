from database.models import Workspace, WorkspaceMember


# =========================
# OWNER ONLY
# =========================

def require_owner(workspace_id, current_user, db):

    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

    if not workspace:
        return False

    return workspace.owner_id == current_user.id


# =========================
# OWNER OR ADMIN
# =========================

def require_admin(workspace_id, current_user, db):

    # Owner
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if workspace:
        return True

    # Admin
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
        WorkspaceMember.role == "Admin"
    ).first()

    return member is not None


# =========================
# OWNER / ADMIN / MEMBER
# =========================

def require_member(workspace_id, current_user, db):

    # Owner
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if workspace:
        return True

    # Admin or Member
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not member:
        return False

    return member.role in ["Admin", "Member"]


# =========================
# ANYONE IN WORKSPACE
# =========================

def require_viewer(workspace_id, current_user, db):

    # Owner
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()

    if workspace:
        return True

    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    return member is not None
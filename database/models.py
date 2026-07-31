from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime


# =========================
# USER
# =========================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    workspaces = relationship(
            "Workspace",
        back_populates="owner"
    )
    
    memberships = relationship(
            "WorkspaceMember",
    back_populates="user"
    )
    activities = relationship(
            "ActivityLog",
       back_populates="user"
    )

# =========================
# WORKSPACE
# =========================

class Workspace(Base):

    __tablename__ = "workspaces"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    owner = relationship(
            "User",
        back_populates="workspaces"
    )


    boards = relationship(
        "Board",
        back_populates="workspace"
    )


    members = relationship(
        "WorkspaceMember",
        back_populates="workspace"
    )



# =========================
# WORKSPACE MEMBERS
# =========================

class WorkspaceMember(Base):

    __tablename__ = "workspace_members"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    role = Column(
        String,
        default="Member"
    )


    workspace = relationship(
        "Workspace",
        back_populates="members"
    )

    
    user = relationship(
            "User",
    back_populates="memberships"
       )


# =========================
# BOARD
# =========================

class Board(Base):

    __tablename__ = "boards"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )


    workspace = relationship(
        "Workspace",
        back_populates="boards"
    )


    columns = relationship(
        "KanbanColumn",
        back_populates="board"
    )



# =========================
# COLUMN
# =========================

class KanbanColumn(Base):

    __tablename__ = "columns"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    board_id = Column(
        Integer,
        ForeignKey("boards.id"),
        nullable=False
    )


    board = relationship(
        "Board",
        back_populates="columns"
    )


    tasks = relationship(
        "Task",
        back_populates="column"
    )



# =========================
# TASK
# =========================

class Task(Base):

    __tablename__ = "tasks"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    description = Column(
        String,
        nullable=True
    )


    priority = Column(
        String,
        default="Medium"
    )


    status = Column(
        String,
        default="To Do"
    )


    due_date = Column(
        String,
        nullable=True
    )


    assigned_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    comments = relationship(
          "Comment",
        back_populates="task",
        cascade="all, delete"
    )
    column_id = Column(
        Integer,
        ForeignKey("columns.id"),
        nullable=False
    )


    column = relationship(
        "KanbanColumn",
        back_populates="tasks"
    )


    assigned_user = relationship(
        "User"
    )
    activities = relationship(
        "ActivityLog"
    )


# =========================
# COMMENT
# =========================

class Comment(Base):

    __tablename__ = "comments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    content = Column(
        String,
        nullable=False
    )


    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=False
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    task = relationship(
         "Task",
      back_populates="comments"
    )

    user = relationship(
        "User"
    )
# =========================
# ACTIVITY LOG
# =========================

class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action = Column(
        String,
        nullable=False
    )

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )

    board_id = Column(
        Integer,
        ForeignKey("boards.id"),
        nullable=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workspace = relationship(
        "Workspace"
    )

    board = relationship(
        "Board"
    )

    task = relationship(
        "Task",
        back_populates="activities"
    )

    user = relationship(
        "User",
        back_populates="activities"
    )
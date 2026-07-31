from workspaces.routes import router as workspace_router
from boards.routes import router as board_router
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from columns.routes import router as column_router
from tasks.routes import router as task_router
from database.database import engine, Base
from database import models
from comments.routes import router as comments_router
from auth.routes import router as auth_router
from users.routes import router as users_router
from members.routes import router as members_router
from activity.routes import router as activity_router
from dashboard.routes import router as dashboard_router
# =========================
# CREATE DATABASE TABLES
# =========================

Base.metadata.create_all(
    bind=engine
)


# =========================
# CREATE FASTAPI APP
# =========================

app = FastAPI(
    title="Kanban Project Management API",
    docs_url="/api-docs"
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workspace_router)
app.include_router(board_router)
app.include_router(column_router)
app.include_router(task_router)
app.include_router(comments_router)
app.include_router(members_router)
app.include_router(activity_router)
app.include_router(dashboard_router)
# =========================
# CUSTOM SWAGGER DOCS
# =========================

@app.get(
    "/api-docs",
    include_in_schema=False
)
async def custom_swagger_ui():

    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Kanban Project Management API"
    )


# =========================
# AUTHENTICATION ROUTES
# =========================

app.include_router(
    auth_router
)


# =========================
# USER ROUTES
# =========================

app.include_router(
    users_router
)


# =========================
# ROOT ROUTE
# =========================

@app.get("/")
def root():

    return {
        "message": "Kanban API is running"
    }
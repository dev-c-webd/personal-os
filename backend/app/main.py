from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.workspaces.router import router as workspaces_router
from app.modules.nodes.router import router as nodes_router
from app.modules.components.router import router as components_router

app = FastAPI(title="Personal OS")


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(nodes_router)
app.include_router(components_router)



# @app.get("/api/v1/health")
# def health_check():
#     with engine.connect() as connection:
#         connection.execute(text("SELECT 1"))

#     return {"status": "ok"}


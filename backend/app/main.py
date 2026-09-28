from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI(title="Personal OS")


@app.get("/api/v1/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok"}
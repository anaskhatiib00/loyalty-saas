from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loyalty SaaS API",
    description="Backend API for digital loyalty cards and wallet integration",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Loyalty SaaS API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/db-health")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}
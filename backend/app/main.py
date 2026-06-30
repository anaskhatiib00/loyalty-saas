from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.api.v1.business import router as business_router

from app.db.database import engine

from app.api.v1.location import router as location_router

from app.api.v1.loyalty_program import router as loyalty_program_router

from app.api.v1.reward import router as reward_router

from app.api.v1.customer import router as customer_router

from app.api.v1.progress_ledger import router as progress_ledger_router

from app.api.v1.loyalty_card import router as loyalty_card_router

from app.api.v1.employee import router as employee_router

from app.api.v1.loyalty_activity import router as loyalty_activity_router

from app.api.v1.scan import router as scan_router

from app.api.v1.credential import router as credential_router

#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loyalty SaaS API",
    description="Backend API for digital loyalty cards and wallet integration",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(business_router)
app.include_router(location_router)
app.include_router(loyalty_program_router)
app.include_router(reward_router)
app.include_router(customer_router)
app.include_router(progress_ledger_router)
app.include_router(loyalty_card_router)
app.include_router(employee_router)
app.include_router(loyalty_activity_router)
app.include_router(scan_router)
app.include_router(credential_router)

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
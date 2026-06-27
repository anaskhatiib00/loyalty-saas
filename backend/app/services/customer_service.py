from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.customer_repository import (
    create_customer,
    get_customers_by_business_id,
    get_customer_by_id,
    update_customer,
    delete_customer,
)
from app.repositories.location_repository import get_location_by_id
from app.schemas.customer import CustomerCreate, CustomerUpdate


def get_current_user_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


def create_customer_service(
    db: Session,
    current_user: User,
    customer_data: CustomerCreate,
):
    business = get_current_user_business(db, current_user)

    location = get_location_by_id(db, customer_data.location_id)

    if not location or location.business_id != business.id:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return create_customer(db, business.id, customer_data)


def list_customers_service(db: Session, current_user: User):
    business = get_current_user_business(db, current_user)

    return get_customers_by_business_id(db, business.id)


def get_customer_service(db: Session, current_user: User, customer_id: int):
    business = get_current_user_business(db, current_user)

    customer = get_customer_by_id(db, customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


def update_customer_service(
    db: Session,
    current_user: User,
    customer_id: int,
    customer_data: CustomerUpdate,
):
    customer = get_customer_service(db, current_user, customer_id)

    return update_customer(db, customer, customer_data)


def delete_customer_service(db: Session, current_user: User, customer_id: int):
    customer = get_customer_service(db, current_user, customer_id)

    delete_customer(db, customer)

    return {"message": "Customer deleted successfully"}
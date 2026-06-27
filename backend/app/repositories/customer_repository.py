from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, business_id: int, customer_data: CustomerCreate):
    customer = Customer(
        business_id=business_id,
        **customer_data.model_dump(),
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers_by_business_id(db: Session, business_id: int):
    return db.query(Customer).filter(Customer.business_id == business_id).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(db: Session, customer: Customer, customer_data: CustomerUpdate):
    update_data = customer_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()
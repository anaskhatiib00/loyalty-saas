from sqlalchemy.orm import Session

from app.models.loyalty_card import LoyaltyCard


def create_loyalty_card(
    db: Session,
    customer_id: int,
    card_number: str,
    public_id: str,
):
    card = LoyaltyCard(
        customer_id=customer_id,
        card_number=card_number,
        public_id=public_id,
    )

    db.add(card)
    db.commit()
    db.refresh(card)

    return card


def get_loyalty_card_by_customer_id(db: Session, customer_id: int):
    return (
        db.query(LoyaltyCard)
        .filter(LoyaltyCard.customer_id == customer_id)
        .first()
    )


def get_loyalty_card_by_public_id(db: Session, public_id: str):
    return (
        db.query(LoyaltyCard)
        .filter(LoyaltyCard.public_id == public_id)
        .first()
    )


def get_loyalty_card_by_card_number(db: Session, card_number: str):
    return (
        db.query(LoyaltyCard)
        .filter(LoyaltyCard.card_number == card_number)
        .first()
    )
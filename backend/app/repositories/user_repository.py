from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    normalized_email = email.strip().lower()

    return (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )


def create_user(
    db: Session,
    full_name: str,
    email: str,
    hashed_password: str,
):
    user = User(
        full_name=full_name,
        email=email.strip().lower(),
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_user_in_transaction(
    db: Session,
    *,
    full_name: str,
    email: str,
    hashed_password: str,
    role: str,
) -> User:
    """
    Create a user without committing the transaction.

    The calling service is responsible for committing or rolling back.
    This is used for multi-step identity workflows such as accepting an
    employee invitation.
    """
    user = User(
        full_name=full_name.strip(),
        email=email.strip().lower(),
        hashed_password=hashed_password,
        role=role,
    )

    db.add(user)
    db.flush()

    return user

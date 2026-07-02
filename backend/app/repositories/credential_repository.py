from sqlalchemy.orm import Session

from app.models.credential import Credential


def create_credential(db: Session, credential: Credential):
    db.add(credential)
    db.commit()
    db.refresh(credential)
    return credential


def update_credential(db: Session, credential: Credential):
    db.commit()
    db.refresh(credential)
    return credential


def get_credentials_by_card_id(db: Session, loyalty_card_id: int):
    return (
        db.query(Credential)
        .filter(Credential.loyalty_card_id == loyalty_card_id)
        .all()
    )


def get_credential_by_provider_reference(
    db: Session,
    provider_reference: str,
):
    return (
        db.query(Credential)
        .filter(Credential.provider_reference == provider_reference)
        .first()
    )


def get_credential_by_provider_reference(db: Session, provider_reference: str):
    return (
        db.query(Credential)
        .filter(Credential.provider_reference == provider_reference)
        .first()
    )


def get_credential_by_card_and_provider(
    db: Session,
    loyalty_card_id: int,
    provider: str,
):
    return (
        db.query(Credential)
        .filter(
            Credential.loyalty_card_id == loyalty_card_id,
            Credential.provider == provider,
        )
        .first()
    )
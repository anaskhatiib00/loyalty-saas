from sqlalchemy.orm import Session

from app.models.apple_wallet_registration import AppleWalletRegistration


def get_registration(
    db: Session,
    credential_id: int,
    device_library_identifier: str,
):
    return (
        db.query(AppleWalletRegistration)
        .filter(
            AppleWalletRegistration.credential_id == credential_id,
            AppleWalletRegistration.device_library_identifier == device_library_identifier,
        )
        .first()
    )


def create_registration(
    db: Session,
    credential_id: int,
    device_library_identifier: str,
    push_token: str,
):
    registration = AppleWalletRegistration(
        credential_id=credential_id,
        device_library_identifier=device_library_identifier,
        push_token=push_token,
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


def delete_registration(db: Session, registration: AppleWalletRegistration):
    db.delete(registration)
    db.commit()


def get_registrations_by_device(
    db: Session,
    device_library_identifier: str,
):
    return (
        db.query(AppleWalletRegistration)
        .filter(
            AppleWalletRegistration.device_library_identifier
            == device_library_identifier
        )
        .all()
    )


def get_registrations_by_device_updated_since(
    db: Session,
    device_library_identifier: str,
    updated_since,
):
    query = db.query(AppleWalletRegistration).filter(
        AppleWalletRegistration.device_library_identifier
        == device_library_identifier
    )

    if updated_since:
        query = query.filter(
            AppleWalletRegistration.last_updated_at > updated_since
        )

    return query.all()
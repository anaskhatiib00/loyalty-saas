from sqlalchemy.orm import Session

from app.models.credential import Credential


def create_credential(db: Session, credential: Credential):
    db.add(credential)
    db.commit()
    db.refresh(credential)
    return credential
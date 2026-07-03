from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.models.user import User


class BaseWalletProvider(ABC):

    @abstractmethod
    def issue(self, db: Session, current_user: User, customer_id: int):
        pass
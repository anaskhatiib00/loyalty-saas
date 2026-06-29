from abc import ABC, abstractmethod

from app.models.credential import Credential
from app.models.loyalty_card import LoyaltyCard


class BaseCredentialProvider(ABC):

    @abstractmethod
    def issue(self, loyalty_card: LoyaltyCard) -> Credential:
        pass

    @abstractmethod
    def update(self, credential: Credential) -> None:
        pass

    @abstractmethod
    def revoke(self, credential: Credential) -> None:
        pass
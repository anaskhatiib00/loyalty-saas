from abc import ABC, abstractmethod


class BaseLoyaltyStrategy(ABC):
    @abstractmethod
    def calculate(
        self,
        earn_rate: float,
        amount_spent: float = 0,
        quantity: int = 1,
    ) -> int:
        pass
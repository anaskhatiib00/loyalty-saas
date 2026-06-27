from app.loyalty.strategies.base import BaseLoyaltyStrategy


class SpendStrategy(BaseLoyaltyStrategy):
    def calculate(
        self,
        earn_rate: float,
        amount_spent: float = 0,
        quantity: int = 1,
    ) -> int:
        return int(amount_spent)
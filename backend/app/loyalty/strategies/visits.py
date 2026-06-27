from app.loyalty.strategies.base import BaseLoyaltyStrategy


class VisitsStrategy(BaseLoyaltyStrategy):
    def calculate(
        self,
        earn_rate: float,
        amount_spent: float = 0,
        quantity: int = 1,
    ) -> int:
        return int(earn_rate)
from app.loyalty.strategies.base import BaseLoyaltyStrategy


class ProductStrategy(BaseLoyaltyStrategy):
    def calculate(
        self,
        earn_rate: float,
        amount_spent: float = 0,
        quantity: int = 1,
    ) -> int:
        return int(quantity * earn_rate)
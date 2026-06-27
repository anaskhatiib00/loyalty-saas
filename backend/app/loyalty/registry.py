from app.core.enums import ProgramType
from app.loyalty.strategies.points import PointsStrategy
from app.loyalty.strategies.stamps import StampsStrategy
from app.loyalty.strategies.visits import VisitsStrategy
from app.loyalty.strategies.spend import SpendStrategy
from app.loyalty.strategies.product import ProductStrategy


class LoyaltyStrategyRegistry:
    strategies = {
        ProgramType.POINTS: PointsStrategy(),
        ProgramType.STAMPS: StampsStrategy(),
        ProgramType.VISITS: VisitsStrategy(),
        ProgramType.SPEND: SpendStrategy(),
        ProgramType.PRODUCT: ProductStrategy(),
    }

    @classmethod
    def get_strategy(cls, program_type: str):
        strategy = cls.strategies.get(program_type)

        if not strategy:
            raise ValueError(f"Unsupported loyalty program type: {program_type}")

        return strategy
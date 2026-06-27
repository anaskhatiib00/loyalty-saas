from app.loyalty.registry import LoyaltyStrategyRegistry


def calculate_loyalty_progress(
    program,
    current_progress: int,
    amount_spent: float = 0,
    quantity: int = 1,
):
    strategy = LoyaltyStrategyRegistry.get_strategy(program.program_type)

    earned_progress = strategy.calculate(
        earn_rate=program.earn_rate,
        amount_spent=amount_spent,
        quantity=quantity,
    )

    new_progress = current_progress + earned_progress

    return {
        "program_type": program.program_type,
        "current_progress": current_progress,
        "earned_progress": earned_progress,
        "new_progress": new_progress,
    }
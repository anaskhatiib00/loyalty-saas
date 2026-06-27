from app.core.enums import ProgramType


def calculate_earned_progress(
    program_type: str,
    earn_rate: float,
    amount_spent: float = 0,
    quantity: int = 1,
) -> int:
    if program_type == ProgramType.POINTS:
        return int(amount_spent * earn_rate)

    if program_type == ProgramType.STAMPS:
        return int(quantity * earn_rate)

    if program_type == ProgramType.VISITS:
        return int(earn_rate)

    if program_type == ProgramType.SPEND:
        return int(amount_spent)

    if program_type == ProgramType.PRODUCT:
        return int(quantity * earn_rate)

    return 0
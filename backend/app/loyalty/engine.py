from app.loyalty.calculators import calculate_earned_progress


def calculate_loyalty_progress(
    program,
    current_progress: int,
    amount_spent: float = 0,
    quantity: int = 1,
):
    earned_progress = calculate_earned_progress(
        program_type=program.program_type,
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
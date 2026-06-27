from app.core.enums import RedemptionBehavior


def calculate_progress_after_redemption(current_progress: int, reward):
    behavior = reward.redemption_behavior

    if behavior == RedemptionBehavior.RESET:
        return 0

    if behavior == RedemptionBehavior.DEDUCT:
        return max(current_progress - reward.required_value, 0)

    if behavior == RedemptionBehavior.CARRY_OVER:
        return current_progress % reward.required_value

    if behavior == RedemptionBehavior.KEEP:
        return current_progress

    return current_progress
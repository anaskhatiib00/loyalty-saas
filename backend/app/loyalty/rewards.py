def evaluate_unlocked_rewards(rewards, new_progress: int):
    unlocked_rewards = []

    for reward in rewards:
        if reward.is_active and new_progress >= reward.required_value:
            unlocked_rewards.append(
                {
                    "id": reward.id,
                    "name": reward.name,
                    "description": reward.description,
                    "required_value": reward.required_value,
                    "reward_type": reward.reward_type,
                    "reward_value": reward.reward_value,
                }
            )

    return unlocked_rewards
from models import Reward


def compute_reward(old_quality: float, new_quality: float, df_len: int) -> Reward:
    """
    Compute reward based on data quality improvement.

    Args:
        old_quality: Quality score before action
        new_quality: Quality score after action
        df_len: Number of rows remaining in the dataset

    Returns:
        Reward object with score and reason
    """
    reward = 0.0
    reason = ""

    # Reward for quality improvement
    improvement = new_quality - old_quality
    if improvement > 0:
        reward += improvement
        reason += f"Quality improved by {round(improvement, 2)}"
    elif improvement == 0:
        reward -= 0.05
        reason += "No improvement penalty"
    else:
        reward += improvement  # negative reward for making things worse
        reason += f"Quality worsened by {round(abs(improvement), 2)}"

    # Penalty for removing too much data
    if df_len < 3:
        reward -= 0.2
        reason += " | Too much data removed"

    return Reward(score=round(reward, 3), reason=reason)

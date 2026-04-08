from grader import grade_dataset
import pandas as pd
from models import Observation, Action, Reward


class FinancialDataEnv:

    def __init__(self, data_path, task=None):
        self.data_path = data_path
        self.task = task
        self.max_steps = 10
        self.reset()

    def reset(self):
        self.df = pd.read_csv(self.data_path)
        self.step_count = 0
        return self._get_observation()

    def state(self):
        return self.df.copy()

    def step(self, action: Action):
        self.step_count += 1

        # STEP 1: measure OLD quality
        old_quality = self._compute_quality()

        reward = 0.0
        reason = ""

        # STEP 2: apply action
        if action.action_type == "remove_duplicates":
            self.df = self.df.drop_duplicates()
            reason = "Removed duplicates"

        elif action.action_type == "fix_negative_amount":
            self.df.loc[self.df["amount"] < 0, "amount"] *= -1
            reason = "Fixed negative values"

        elif action.action_type == "drop_missing_customer":
            self.df = self.df.dropna(subset=["customer"])
            reason = "Dropped missing customers"

        # STEP 3: measure NEW quality
        new_quality = self._compute_quality()

        # STEP 4: reward based on improvement
        reward += (new_quality - old_quality)

        # STEP 5: penalty if no improvement
        if new_quality == old_quality:
            reward -= 0.05
            reason += " | No improvement penalty"

        # STEP 6: penalty if too much data removed
        if len(self.df) < 3:
            reward -= 0.2
            reason += " | Too much data removed"

        # STEP 7: done condition
        done = self.step_count >= self.max_steps

        # STEP 8: final score
        final_score = grade_dataset(self.df)

        return (
            self._get_observation(),
            Reward(score=round(reward, 3), reason=reason),
            done,
            {"final_score": final_score}
        )

    def _get_observation(self):
        return Observation(
            dataset=self.df.to_dict(orient="records"),
            step_count=self.step_count,
            quality_score=self._compute_quality()
        )

    def _compute_quality(self):
        score = 1.0

        if self.df["amount"].lt(0).any():
            score -= 0.2

        if self.df["customer"].isnull().any():
            score -= 0.2

        if self.df.duplicated().any():
            score -= 0.2

        if self.task:
            if self.task.name in ["medium", "hard"]:
                try:
                    pd.to_datetime(self.df["date"], errors="raise")
                except Exception:
                    score -= 0.2

            if self.task.name == "hard":
                if (self.df["amount"] > 100000).any():
                    score -= 0.2

        return max(score, 0.0)

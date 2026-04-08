from env import FinancialDataEnv
from models import Action
from tasks import EASY_TASK

env = FinancialDataEnv("datasets/sample.csv", task=EASY_TASK)

obs = env.reset()
print("Task:", env.task.description)
print("Initial Observation:\n", obs)

# Step 1 - Remove duplicates
action = Action(action_type="remove_duplicates")
obs, reward, done, info = env.step(action)
print("\nAfter Action 1 (remove_duplicates):")
print(obs)
print("Reward:", reward)

# Step 2 - Fix negative amounts
action = Action(action_type="fix_negative_amount")
obs, reward, done, info = env.step(action)
print("\nAfter Action 2 (fix_negative_amount):")
print(obs)
print("Reward:", reward)

# Step 3 - Drop missing customers
action = Action(action_type="drop_missing_customer")
obs, reward, done, info = env.step(action)
print("\nAfter Action 3 (drop_missing_customer):")
print(obs)
print("Reward:", reward)
print("Final Score:", info["final_score"])
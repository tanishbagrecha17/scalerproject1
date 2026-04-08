import os
from openai import OpenAI
from env import FinancialDataEnv
from models import Action
from tasks import EASY_TASK

# 🔥 Load environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

# 🔥 Initialize client safely (NO CRASH)
if HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )
else:
    client = None


def run():
    print("[START]")

    env = FinancialDataEnv("datasets/sample.csv", task=EASY_TASK)
    obs = env.reset()

    done = False
    step_count = 0

    while not done:
        # 🔥 TRY API (OR FALLBACK)
        try:
            if client is None:
                raise Exception("No API key provided")

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data cleaning agent. Choose one action: remove_duplicates, fix_negative_amount, drop_missing_customer."
                    },
                    {
                        "role": "user",
                        "content": str(obs)
                    }
                ]
            )

            action_text = response.choices[0].message.content.lower()

        except Exception as e:
            print(f"[STEP] fallback triggered: {str(e)}")
            action_text = "remove duplicates"

        # 🔥 Convert text → action
        if "duplicate" in action_text:
            action = Action(action_type="remove_duplicates")
        elif "negative" in action_text:
            action = Action(action_type="fix_negative_amount")
        else:
            action = Action(action_type="drop_missing_customer")

        # 🔥 Step environment
        obs, reward, done, info = env.step(action)

        print(f"[STEP] step={step_count} action={action.action_type} reward={reward.score}")

        step_count += 1

    print(f"[END] final_score={info['final_score']}")


if __name__ == "__main__":
    run()
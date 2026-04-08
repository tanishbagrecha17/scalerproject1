from flask import Flask, jsonify, request
from env import FinancialDataEnv
from models import Action
from tasks import EASY_TASK, MEDIUM_TASK, HARD_TASK

app = Flask(__name__)

# Global environment instance
env = None
TASKS = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK
}

# ──────────────────────────────────────────────
# OpenEnv Required Endpoints
# ──────────────────────────────────────────────

@app.route("/reset", methods=["POST"])
def reset():
    global env
    data = request.get_json(silent=True) or {}
    task_name = data.get("task", "easy")
    task = TASKS.get(task_name, EASY_TASK)
    env = FinancialDataEnv("datasets/sample.csv", task=task)
    obs = env.reset()
    return jsonify({"observation": obs.dict(), "task": task_name})


@app.route("/step", methods=["POST"])
def step():
    global env
    if env is None:
        return jsonify({"error": "Environment not initialized. Call /reset first."}), 400
    data = request.get_json(silent=True) or {}
    action_type = data.get("action_type", "remove_duplicates")
    action = Action(
        action_type=action_type,
        column=data.get("column"),
        value=data.get("value"),
        row_id=data.get("row_id")
    )
    obs, reward, done, info = env.step(action)
    return jsonify({
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    })


@app.route("/validate", methods=["GET"])
def validate():
    return jsonify({
        "name": "financial-data-cleaning-env",
        "version": "1.0.0",
        "observation_space": {
            "type": "dict",
            "fields": {"dataset": "list", "step_count": "int", "quality_score": "float"}
        },
        "action_space": {
            "type": "dict",
            "fields": {"action_type": "string", "column": "optional", "value": "optional", "row_id": "optional"}
        },
        "reward": {"type": "float", "range": [0.0, 1.0]},
        "tasks": ["easy", "medium", "hard"],
        "status": "ok"
    })


@app.route("/")
def home():
    return """
    <h2>💼 Financial Data Cleaning Agent</h2>
    <p><b>OpenEnv Endpoints:</b></p>
    <ul>
        <li>POST /reset — Initialize environment</li>
        <li>POST /step — Take an action</li>
        <li>GET /validate — Validate environment spec</li>
    </ul>
    <p><b>Demo Endpoints:</b></p>
    <ul>
        <li><a href='/run/easy'>/run/easy</a></li>
        <li><a href='/run/medium'>/run/medium</a></li>
        <li><a href='/run/hard'>/run/hard</a></li>
    </ul>
    """


@app.route("/run/<task_name>")
def run(task_name):
    if task_name not in TASKS:
        return jsonify({"error": "Invalid task. Use easy, medium, or hard"}), 400
    task = TASKS[task_name]
    local_env = FinancialDataEnv("datasets/sample.csv", task=task)
    local_env.reset()
    actions = ["remove_duplicates", "fix_negative_amount", "drop_missing_customer"]
    logs = []
    done = False
    step_num = 0
    while not done:
        action_type = actions[step_num % len(actions)]
        action = Action(action_type=action_type)
        obs, reward, done, info = local_env.step(action)
        logs.append({"step": step_num, "action": action_type, "reward": reward.score, "reason": reward.reason})
        step_num += 1
    return jsonify({"task": task_name, "final_score": info["final_score"], "steps": logs})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
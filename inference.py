import json
import sys
import os
from openai import OpenAI
from environment import BudgetTrackerEnv

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN if HF_TOKEN else "dummy")

ACTIONS = ["allocate_food", "allocate_transport", "allocate_savings", 
           "allocate_entertainment", "skip"]

TASKS = [
    {"id": "easy",   "goal": "Save at least 10% of the total budget (100 out of 1000)"},
    {"id": "medium", "goal": "Save 20% and keep food spending under 30%"},
    {"id": "hard",   "goal": "Save 30%, food under 25%, entertainment under 10%"},
]

def get_agent_action(state: dict, task_goal: str) -> str:
    prompt = f"""You are a budget management AI agent.
Current state: {json.dumps(state)}
Task goal: {task_goal}
Available actions: {ACTIONS}
Choose ONE action from the list that best helps achieve the goal.
Respond with ONLY the action name, nothing else."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.1
        )
        action = response.choices[0].message.content.strip().lower()
        if action not in ACTIONS:
            action = "allocate_savings"
    except Exception:
        action = "allocate_savings"
    return action

def run_task(task: dict) -> float:
    env = BudgetTrackerEnv()
    state = env.reset()
    total_reward = 0.0
    steps = 0

    print(json.dumps({"type": "[START]", "task_id": task["id"], "state": state}))

    done = False
    while not done and steps < 30:
        action = get_agent_action(state, task["goal"])
        next_state, reward, done, info = env.step(action)

        print(json.dumps({
            "type": "[STEP]",
            "task_id": task["id"],
            "step": steps,
            "action": action,
            "reward": reward,
            "done": done,
            "state": next_state
        }))

        total_reward += reward
        state = next_state
        steps += 1

    score = round(total_reward / max(steps, 1), 4)
    print(json.dumps({"type": "[END]", "task_id": task["id"], "score": score, "reward": score}))
    return score

if __name__ == "__main__":
    scores = {}
    for task in TASKS:
        score = run_task(task)
        scores[task["id"]] = score
    print(json.dumps({"final_scores": scores}))
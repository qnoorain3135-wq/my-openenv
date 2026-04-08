import os
import json
import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import uvicorn
from environment import BudgetTrackerEnv

app = FastAPI()
env = BudgetTrackerEnv()

class Action(BaseModel):
    action: str

@app.post("/reset")
def reset():
    state = env.reset()
    return state

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(body: Action):
    obs, reward, done, info = env.step(body.action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

"""
Email Reply OpenEnv - FastAPI Server
Exposes: /reset, /step, /state, /tasks, /grader, /baseline
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from models import EmailAction, EmailObservation, EpisodeState
from environment import EmailReplyEnvironment
from tasks import TASKS, grade_reply

app = FastAPI(
    title="Email Reply OpenEnv",
    description="An OpenEnv environment where an AI agent replies to emails.",
    version="1.0.0",
)

# Global environment instance
env = EmailReplyEnvironment()


# ──────────────────────────────────────────────
# Core OpenEnv Endpoints
# ──────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: Optional[str] = "task_1_easy"


class StepRequest(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"status": "ok", "env": "Email Reply OpenEnv"}


@app.post("/reset")
def reset(request: ResetRequest):
    """Reset the environment and start a new episode."""
    obs = env.reset(task_id=request.task_id)
    return obs.model_dump()


@app.post("/step")
def step(request: StepRequest):
    """Submit the agent's reply and get a score."""
    try:
        action = EmailAction(reply=request.reply)
        obs, reward, done = env.step(action)
        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "done": done,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    """Get current episode state/metadata."""
    return env.state().model_dump()


# ──────────────────────────────────────────────
# Required Additional Endpoints
# ──────────────────────────────────────────────

@app.get("/tasks")
def get_tasks():
    """Return list of tasks and the action schema."""
    task_list = []
    for task_id, task in TASKS.items():
        task_list.append({
            "task_id": task_id,
            "difficulty": task["difficulty"],
            "subject": task["subject"],
            "instruction": task["instruction"],
        })
    return {
        "tasks": task_list,
        "action_schema": {
            "reply": {
                "type": "string",
                "description": "The agent's email reply text",
                "required": True,
            }
        },
    }


@app.get("/grader")
def grader(task_id: str, reply: str):
    """Grade a reply for a given task. Returns score 0.0–1.0."""
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")
    score, feedback = grade_reply(task_id, reply)
    return {
        "task_id": task_id,
        "score": score,
        "feedback": feedback,
    }


@app.get("/baseline")
def baseline():
    """
    Run baseline inference (simple rule-based agent) on all 3 tasks.
    Returns scores for each task.
    """
    baseline_replies = {
        "task_1_easy": (
            "Hello,\n\nThank you so much for the warm welcome! "
            "I'm really happy and excited to be part of this service. "
            "Looking forward to a great experience!\n\nBest regards"
        ),
        "task_2_medium": (
            "Dear Customer,\n\nI sincerely apologize for the delay with your order #45231. "
            "This is not the experience we want for you. "
            "I will immediately look into this and help resolve the issue. "
            "Could you please share your contact details so we can assist you further?\n\n"
            "Best regards,\nSupport Team"
        ),
        "task_3_hard": (
            "Dear Customer,\n\nI sincerely apologize for the extremely poor experience with order #78932. "
            "We take full ownership of this situation — the damaged product, wrong item, and delay are "
            "completely unacceptable. I am escalating this to our priority team immediately. "
            "You will receive a full refund within 48 hours, along with compensation credit for the "
            "inconvenience caused. We deeply value your patience and will ensure this is resolved urgently.\n\n"
            "Sincerely,\nEscalations Team"
        ),
    }

    results = []
    total_score = 0.0

    for task_id, reply in baseline_replies.items():
        score, feedback = grade_reply(task_id, reply)
        total_score += score
        results.append({
            "task_id": task_id,
            "difficulty": TASKS[task_id]["difficulty"],
            "baseline_reply": reply,
            "score": score,
            "feedback": feedback,
        })

    return {
        "baseline_results": results,
        "average_score": round(total_score / len(results), 2),
    }


# In-memory leaderboard (resets on server restart)
_leaderboard: list = []

class LeaderboardEntry(BaseModel):
    agent_name: str
    task_id: str
    score: float
    turns_taken: int

@app.post("/leaderboard")
def submit_score(entry: LeaderboardEntry):
    """Submit a score to the in-memory leaderboard."""
    _leaderboard.append(entry.model_dump())
    return {"status": "recorded", "entry": entry.model_dump()}

@app.get("/leaderboard")
def get_leaderboard():
    """Get top scores sorted by score descending."""
    sorted_board = sorted(_leaderboard, key=lambda x: x["score"], reverse=True)
    return {"leaderboard": sorted_board[:20]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=False)

"""CloudSense API routes."""

import threading

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from env.environment import CloudSenseEnv
from env.tasks import TASKS

router = APIRouter()
env = CloudSenseEnv()
_env_lock = threading.Lock()


class ActionRequest(BaseModel):
    action_type: str
    resource_id: str
    new_config: dict | None = None
    reasoning: str = ""


@router.get("/")
def root():
    return {"status": "ok", "name": "cloudsense", "version": "1.0.0"}


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/reset")
def reset(task_id: str = Query(...)):
    with _env_lock:
        try:
            obs = env.reset(task_id)
            return obs.model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.post("/step")
def step(action: ActionRequest):
    with _env_lock:
        try:
            result = env.step(action.model_dump())
            return {
                "observation": result.observation.model_dump(),
                "reward": result.reward,
                "done": result.done,
                "info": result.info,
            }
        except RuntimeError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/state")
def state():
    with _env_lock:
        try:
            return env.state()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks")
def tasks():
    result = []
    for tid, tcls in TASKS.items():
        t = tcls()
        result.append({
            "id": t.task_id,
            "difficulty": t.difficulty,
            "max_steps": t.max_steps,
            "description": t.description,
        })
    return result


@router.post("/close")
def close():
    with _env_lock:
        env.close()
        return {"status": "closed"}

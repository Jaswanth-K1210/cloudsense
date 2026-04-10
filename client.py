"""CloudSense Python SDK — typed client for the CloudSense RL environment."""

from __future__ import annotations

import requests
from env.models import (
    ActionType,
    CloudAction,
    CloudObservation,
    CloudSenseAction,
    CloudSenseObservation,
    StepResult,
)


class CloudSenseClient:
    """Typed HTTP client for the CloudSense environment API."""

    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()

    # ── Core environment API ────────────────────────────────────────

    def reset(self, task_id: str = "startup-cleanup") -> CloudObservation:
        """Reset the environment to a new episode."""
        resp = self._session.post(
            f"{self.base_url}/reset",
            params={"task_id": task_id},
            timeout=30,
        )
        resp.raise_for_status()
        return CloudObservation(**resp.json())

    def step(self, action: CloudAction) -> StepResult:
        """Execute an action and return the result."""
        resp = self._session.post(
            f"{self.base_url}/step",
            json=action.model_dump(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return StepResult(
            observation=CloudObservation(**data["observation"]),
            reward=data["reward"],
            done=data["done"],
            info=data.get("info", {}),
        )

    def state(self) -> dict:
        """Get the current environment state."""
        resp = self._session.get(f"{self.base_url}/state", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        """Close the current episode."""
        resp = self._session.post(f"{self.base_url}/close", timeout=10)
        resp.raise_for_status()

    # ── Discovery ───────────────────────────────────────────────────

    def health(self) -> dict:
        """Check environment health."""
        resp = self._session.get(f"{self.base_url}/health", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def tasks(self) -> list[dict]:
        """List available tasks."""
        resp = self._session.get(f"{self.base_url}/tasks", timeout=10)
        resp.raise_for_status()
        return resp.json()

    # ── Convenience ─────────────────────────────────────────────────

    def rightsize(
        self, resource_id: str, instance_type: str, reasoning: str = "", **config
    ) -> StepResult:
        """Shortcut: rightsize a resource."""
        new_config = {"instance_type": instance_type, **config}
        return self.step(
            CloudAction(
                action_type=ActionType.rightsize_resource,
                resource_id=resource_id,
                new_config=new_config,
                reasoning=reasoning,
            )
        )

    def terminate(self, resource_id: str, reasoning: str = "") -> StepResult:
        """Shortcut: terminate a resource."""
        return self.step(
            CloudAction(
                action_type=ActionType.terminate_resource,
                resource_id=resource_id,
                reasoning=reasoning,
            )
        )

    def skip(self, resource_id: str, reasoning: str = "") -> StepResult:
        """Shortcut: skip a resource."""
        return self.step(
            CloudAction(
                action_type=ActionType.skip_resource,
                resource_id=resource_id,
                reasoning=reasoning,
            )
        )

"""
Review Agent — Gestisce il ciclo di revisione con il manager.
No LLM: routing puro basato sul feedback.
"""

from __future__ import annotations
import time
from state import UnchainedState
from store import update_agent_status


def review_agent(state: UnchainedState) -> dict:
    """Processa il feedback del manager e determina il routing."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Review Agent", "running")
    time.sleep(0.5)

    review_feedback = state.get("review_feedback", {})
    feedback_status = review_feedback.get("status", "pending_review")
    review_iteration = state.get("review_iteration", 0)

    update_agent_status(request_id, "Review Agent", "completed")

    return {
        "review_status": feedback_status,
        "review_iteration": review_iteration + 1,
    }

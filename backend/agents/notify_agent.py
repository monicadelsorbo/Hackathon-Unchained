"""
Notify Agent — Aggiorna la dashboard del dipendente.
No LLM: update store puro.
"""

from __future__ import annotations
import time
from state import UnchainedState
from store import update_agent_status


def notify_agent(state: UnchainedState) -> dict:
    """Marca il piano come approvato e aggiorna la dashboard."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Notify Agent", "running")
    time.sleep(0.5)

    update_agent_status(request_id, "Notify Agent", "completed")
    return {
        "dashboard_updated": True,
        "current_phase": "complete",
        "review_status": "approved",
    }

"""
Cost Agent — Calcola costi totali, ore e ROI stimato.
No LLM: calcolo puro.
"""

from __future__ import annotations
import time
from state import UnchainedState
from store import update_agent_status


def cost_agent(state: UnchainedState) -> dict:
    """Calcola il breakdown dei costi del piano formativo."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Cost Agent", "running")
    time.sleep(0.5)

    training_plan = state.get("training_plan", [])

    total_cost = 0.0
    total_hours = 0.0
    total_weeks = 0
    cost_per_module = []

    for module in training_plan:
        module_cost = 0.0
        module_hours = 0.0
        courses = module.get("courses", [])

        for course in courses:
            module_cost += course.get("cost_eur", 0)
            module_hours += course.get("duration_hours", 0)

        total_cost += module_cost
        total_hours += module_hours
        total_weeks += module.get("duration_weeks", 2)

        cost_per_module.append(
            {
                "module_id": module.get("module_id", ""),
                "module_title": module.get("title", ""),
                "cost_eur": round(module_cost, 2),
                "hours": round(module_hours, 1),
                "duration_weeks": module.get("duration_weeks", 2),
                "num_courses": len(courses),
            }
        )

    # ROI stimato (semplificato per hackathon)
    if total_cost > 0:
        roi_estimate = (
            f"Investimento di €{total_cost:.2f} in {total_hours:.0f} ore di formazione. "
            f"ROI stimato: aumento produttività del 15-25% entro 6 mesi dal completamento. "
            f"Costo orario medio: €{total_cost / max(total_hours, 1):.2f}/ora."
        )
    else:
        roi_estimate = "Nessun costo diretto per corsi. Il ROI deriva dal tempo investito nella formazione."

    update_agent_status(request_id, "Cost Agent", "completed")
    return {
        "cost_breakdown": {
            "total_course_cost_eur": round(total_cost, 2),
            "total_hours": round(total_hours, 1),
            "estimated_duration_weeks": total_weeks,
            "roi_estimate": roi_estimate,
            "cost_per_module": cost_per_module,
        }
    }

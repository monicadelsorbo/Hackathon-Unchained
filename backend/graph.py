"""
UNCHAINED - LangGraph StateGraph definitions.
Tre grafi separati per le tre fasi del flusso.
"""

from langgraph.graph import StateGraph, START, END
from state import UnchainedState
from agents.profile_agent import profile_agent
from agents.assessment_agent import generate_assessment, analyze_assessment
from agents.plan_agent import plan_agent
from agents.resource_agent import resource_agent
from agents.cost_agent import cost_agent
from agents.mentor_agent import mentor_agent
from agents.review_agent import review_agent
from agents.notify_agent import notify_agent


# ── Fase 1: Estrazione Profilo + Generazione Assessment ───────────────────

phase1 = StateGraph(UnchainedState)
phase1.add_node("profile", profile_agent)
phase1.add_node("generate_assessment", generate_assessment)
phase1.add_edge(START, "profile")
phase1.add_edge("profile", "generate_assessment")
phase1.add_edge("generate_assessment", END)

phase1_graph = phase1.compile()


# ── Fase 2: Analisi Assessment + Generazione Piano Completo ───────────────
# Flusso: analyze → plan → resource → cost → mentor

phase2 = StateGraph(UnchainedState)
phase2.add_node("analyze_assessment", analyze_assessment)
phase2.add_node("plan", plan_agent)
phase2.add_node("resource", resource_agent)
phase2.add_node("cost", cost_agent)
phase2.add_node("mentor", mentor_agent)

phase2.add_edge(START, "analyze_assessment")
phase2.add_edge("analyze_assessment", "plan")
phase2.add_edge("plan", "resource")
phase2.add_edge("resource", "cost")
phase2.add_edge("cost", "mentor")
phase2.add_edge("mentor", END)

phase2_graph = phase2.compile()


# ── Fase 3: Review Loop ──────────────────────────────────────────────────


def route_review(state: UnchainedState) -> str:
    """Routing condizionale: legge direttamente dal feedback del manager."""
    feedback = state.get("review_feedback", {})
    if feedback.get("status") == "approved":
        return "approved"
    return "changes_requested"


phase3 = StateGraph(UnchainedState)
phase3.add_node("review", review_agent)
phase3.add_node("notify", notify_agent)
phase3.add_node("revise_plan", plan_agent)
phase3.add_node("revise_resource", resource_agent)
phase3.add_node("revise_cost", cost_agent)

phase3.add_edge(START, "review")
phase3.add_conditional_edges(
    "review",
    route_review,
    {
        "approved": "notify",
        "changes_requested": "revise_plan",
    },
)
phase3.add_edge("notify", END)
phase3.add_edge("revise_plan", "revise_resource")
phase3.add_edge("revise_resource", "revise_cost")
phase3.add_edge("revise_cost", END)

phase3_graph = phase3.compile()

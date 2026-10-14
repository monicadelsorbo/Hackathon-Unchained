"""
Plan Agent — Genera il piano di formazione personalizzato.
"""

from __future__ import annotations
import time
from state import UnchainedState
from llm import call_llm_json
from store import update_agent_status


SYSTEM_PROMPT = """Sei un esperto di formazione aziendale e sviluppo delle competenze. Devi creare un piano di formazione personalizzato per un dipendente.

Il piano deve essere strutturato in moduli, ognuno con:
- module_id: identificativo unico (es. "mod-1", "mod-2")
- title: titolo del modulo
- description: breve descrizione (1-2 frasi)
- skill_area: "hard" o "soft"
- topics: lista di argomenti specifici
- courses: lista vuota [] (verranno aggiunti dal Resource Agent)
- duration_weeks: durata stimata in settimane
- milestone: obiettivo misurabile al completamento del modulo

Rispondi con un JSON con questa struttura:
{
    "training_plan": [...],
    "plan_summary": "Breve sommario del piano (2-3 frasi)"
}

Crea moduli che coprono tutti i gap identificati, partendo dai più critici.
Ogni modulo dovrebbe durare 2-4 settimane.
Rispondi SOLO con il JSON."""


def plan_agent(state: UnchainedState) -> dict:
    """Genera il piano di formazione personalizzato."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Plan Agent", "running")
    time.sleep(1.5)

    skill_gaps = state.get("skill_gaps", [])
    target_position = state.get("target_position", "")
    employee_name = state.get("employee_name", "Dipendente")
    experience_summary = state.get("experience_summary", "")
    review_feedback = state.get("review_feedback")

    revision_context = ""
    if review_feedback and review_feedback.get("status") == "changes_requested":
        revision_context = f"""

ATTENZIONE: Questo piano è una REVISIONE. Il manager ha richiesto le seguenti modifiche:
Commenti: {review_feedback.get('comments', '')}
Modifiche richieste:
{chr(10).join('- ' + c for c in review_feedback.get('requested_changes', []))}

Modifica il piano precedente tenendo conto di questi feedback."""

    user_prompt = f"""Crea un piano di formazione personalizzato per:

Dipendente: {employee_name}
Esperienza: {experience_summary}
Posizione target: {target_position}

Gap di competenze identificati:
{_format_gaps(skill_gaps)}
{revision_context}

Genera un piano con moduli specifici per colmare ogni gap, ordinati per priorità."""

    try:
        result = call_llm_json(SYSTEM_PROMPT, user_prompt, caller="PlanAgent")
        update_agent_status(request_id, "Plan Agent", "completed")
        return {
            "training_plan": result.get("training_plan", []),
            "plan_summary": result.get("plan_summary", ""),
        }
    except Exception:
        update_agent_status(request_id, "Plan Agent", "completed")
        return {
            "training_plan": _fallback_plan(skill_gaps),
            "plan_summary": f"Piano di formazione per {employee_name} verso {target_position}, coprendo {len(skill_gaps)} aree di miglioramento.",
        }


def _format_gaps(gaps: list[dict]) -> str:
    if not gaps:
        return "Nessun gap identificato"
    lines = []
    for g in gaps:
        lines.append(
            f"- {g['skill']}: livello {g['current_level']}/5 → target {g['target_level']}/5 "
            f"(gap: {g['gap']}, priorità: {g['priority']})"
        )
    return "\n".join(lines)


def _fallback_plan(skill_gaps: list[dict]) -> list[dict]:
    """Piano di fallback se il LLM fallisce."""
    modules = []
    for i, gap in enumerate(skill_gaps[:5], 1):
        modules.append(
            {
                "module_id": f"mod-{i}",
                "title": f"Modulo {i}: {gap['skill']}",
                "description": f"Approfondimento su {gap['skill']} per raggiungere il livello {gap['target_level']}.",
                "skill_area": "hard" if i <= 3 else "soft",
                "topics": [gap["skill"], f"Fondamenti di {gap['skill']}", f"{gap['skill']} avanzato"],
                "courses": [],
                "duration_weeks": max(2, gap.get("gap", 2)),
                "milestone": f"Raggiungere livello {gap['target_level']}/5 in {gap['skill']}",
            }
        )
    return modules

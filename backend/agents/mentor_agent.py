"""
Mentor Agent — Assegna il mentore più adatto.
Matching algoritmico + LLM per la motivazione.
"""

from __future__ import annotations
import time
from state import UnchainedState
from llm import call_llm_text
from store import update_agent_status
from mock_data import MENTORS


def mentor_agent(state: UnchainedState) -> dict:
    """Assegna il mentore più adatto in base ai gap del dipendente."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Mentor Agent", "running")
    time.sleep(1)

    skill_gaps = state.get("skill_gaps", [])
    target_position = state.get("target_position", "")
    employee_name = state.get("employee_name", "Dipendente")

    gap_skills = [g["skill"].lower() for g in skill_gaps]

    # Score ogni mentore
    best_mentor = None
    best_score = -1.0

    for mentor in MENTORS:
        score = 0.0
        expertise = [e.lower() for e in mentor.get("expertise", [])]

        # Match competenze
        for gap_skill in gap_skills:
            for exp in expertise:
                if gap_skill in exp or exp in gap_skill:
                    score += 3.0

        # Bonus per esperienza di mentoring
        score += mentor.get("completed_mentorships", 0) * 0.1

        if score > best_score:
            best_score = score
            best_mentor = mentor

    if best_mentor is None:
        best_mentor = MENTORS[0]
        best_score = 1.0

    # Genera motivazione con LLM
    try:
        rationale = call_llm_text(
            "Sei un esperto HR. Scrivi 2-3 frasi che spiegano perché questo mentore è la scelta migliore per il dipendente. Sii specifico e professionale.",
            f"""Mentore: {best_mentor['name']} ({best_mentor['role']})
Expertise: {', '.join(best_mentor['expertise'])}
Bio: {best_mentor['bio']}

Dipendente: {employee_name}
Posizione target: {target_position}
Gap da colmare: {', '.join(g['skill'] for g in skill_gaps[:5])}""",
            caller="MentorAgent",
        )
    except Exception:
        rationale = (
            f"{best_mentor['name']} è il mentore ideale grazie alla sua esperienza in "
            f"{', '.join(best_mentor['expertise'][:3])}. Con {best_mentor['completed_mentorships']} "
            f"mentorship completate, ha dimostrato capacità di guidare percorsi di crescita professionale."
        )

    update_agent_status(request_id, "Mentor Agent", "completed")
    return {
        "assigned_mentor": {
            "mentor_id": best_mentor["mentor_id"],
            "name": best_mentor["name"],
            "role": best_mentor["role"],
            "expertise": best_mentor["expertise"],
            "match_score": round(best_score, 2),
            "rationale": rationale,
            "availability": best_mentor["availability"],
        },
    }

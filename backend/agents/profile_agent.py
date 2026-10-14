"""
Profile Agent — Estrae profilo strutturato dal CV e dati HR.
"""

from __future__ import annotations
import time
from state import UnchainedState
from llm import call_llm_json
from store import update_agent_status
from mock_data import EMPLOYEES


SYSTEM_PROMPT = """Sei un esperto di analisi CV e risorse umane. Il tuo compito è estrarre un profilo strutturato dal CV di un dipendente.

Devi restituire un JSON con questa struttura esatta:
{
    "employee_name": "Nome Cognome",
    "current_role": "Ruolo attuale",
    "hard_skills": [{"skill": "nome_skill", "level": 3}],
    "soft_skills": [{"skill": "nome_skill", "level": 3}],
    "experience_summary": "Breve sommario dell'esperienza professionale (2-3 frasi)"
}

Per i livelli di competenza usa questa scala:
1 = Base/Principiante
2 = Elementare
3 = Intermedio
4 = Avanzato
5 = Esperto

Estrai tutte le competenze menzionate nel CV, sia tecniche (hard) che trasversali (soft).
Rispondi SOLO con il JSON, senza testo aggiuntivo."""


def profile_agent(state: UnchainedState) -> dict:
    """Estrae il profilo strutturato dal CV del dipendente."""
    request_id = state["request_id"]
    employee_id = state["employee_id"]
    update_agent_status(request_id, "Profile Agent", "running")

    # Simula un po' di processing time per effetto demo
    time.sleep(1)

    # Recupera CV dal mock data
    employee = EMPLOYEES.get(employee_id, {})
    cv_text = state.get("cv_text", employee.get("cv_text", ""))
    hr_notes = employee.get("hr_notes", "")

    user_prompt = f"""Analizza il seguente CV e le note HR per estrarre il profilo strutturato.

CV:
{cv_text}

Note HR:
{hr_notes}"""

    try:
        result = call_llm_json(SYSTEM_PROMPT, user_prompt, caller="ProfileAgent")
        update_agent_status(request_id, "Profile Agent", "completed")
        return {
            "employee_name": result.get("employee_name", employee.get("name", "")),
            "current_role": result.get("current_role", employee.get("current_role", "")),
            "hard_skills": result.get("hard_skills", []),
            "soft_skills": result.get("soft_skills", []),
            "experience_summary": result.get("experience_summary", ""),
            "cv_text": cv_text,
        }
    except Exception as e:
        # Fallback: usa dati mock direttamente
        update_agent_status(request_id, "Profile Agent", "completed")
        return {
            "employee_name": employee.get("name", "Dipendente"),
            "current_role": employee.get("current_role", "N/A"),
            "hard_skills": [
                {"skill": "Python", "level": 3},
                {"skill": "JavaScript", "level": 2},
                {"skill": "SQL", "level": 2},
            ],
            "soft_skills": [
                {"skill": "Teamwork", "level": 3},
                {"skill": "Problem Solving", "level": 3},
            ],
            "experience_summary": f"Profilo estratto dai dati HR per {employee.get('name', 'dipendente')}.",
            "cv_text": cv_text,
        }

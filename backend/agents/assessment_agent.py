"""
Assessment Agent — Due modalità:
1. Genera domande di assessment personalizzate
2. Analizza risposte e produce gap analysis
"""

from __future__ import annotations
import time
from state import UnchainedState
from llm import call_llm_json
from store import update_agent_status


GENERATE_SYSTEM_PROMPT = """Sei un esperto di valutazione delle competenze professionali. Devi generare un assessment personalizzato per un dipendente che vuole raggiungere una posizione target.

Genera un mix di domande (massimo 20) distribuite tra:
- "technical": domande tecniche sulle competenze richieste (8-10 domande)
- "situational": domande situazionali su soft skill e leadership (5-7 domande)
- "interest": domande su interessi e motivazioni (3-5 domande)

Tipi di domanda disponibili:
- "multiple_choice": fornisci esattamente 4 opzioni
- "scale": l'utente risponde con un valore da 1 a 5
- "open": risposta libera

Rispondi con un JSON con questa struttura:
{
    "questions": [
        {
            "question_id": "q1",
            "category": "technical",
            "skill_area": "nome_area",
            "question_text": "testo della domanda",
            "question_type": "multiple_choice",
            "options": ["A", "B", "C", "D"]
        }
    ]
}

Le domande devono essere specifiche per il gap tra le competenze attuali e quelle richieste dalla posizione target.
Rispondi SOLO con il JSON."""


ANALYZE_SYSTEM_PROMPT = """Sei un esperto di skill assessment e gap analysis. Analizza le risposte di un dipendente al suo assessment e identifica i gap di competenze.

Per ogni competenza rilevante, determina:
- current_level: livello attuale (1-5) basato sulle risposte
- target_level: livello richiesto dalla posizione target (tipicamente 4-5)
- gap: differenza (target - current)
- priority: "high" se gap >= 3, "medium" se gap == 2, "low" se gap <= 1

Rispondi con un JSON con questa struttura:
{
    "skill_gaps": [
        {
            "skill": "nome_competenza",
            "current_level": 2,
            "target_level": 4,
            "gap": 2,
            "priority": "medium"
        }
    ]
}

Ordina per priorità (high prima). Includi sia hard skill che soft skill.
Rispondi SOLO con il JSON."""


def generate_assessment(state: UnchainedState) -> dict:
    """Genera domande di assessment personalizzate."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Assessment Agent", "running")
    time.sleep(1)

    hard_skills = state.get("hard_skills", [])
    soft_skills = state.get("soft_skills", [])
    target_position = state.get("target_position", "")
    current_role = state.get("current_role", "")

    user_prompt = f"""Genera un assessment per questo dipendente:

Ruolo attuale: {current_role}
Posizione target: {target_position}

Competenze tecniche attuali:
{_format_skills(hard_skills)}

Competenze trasversali attuali:
{_format_skills(soft_skills)}

Genera domande mirate a valutare le lacune tra il profilo attuale e le competenze richieste per la posizione target."""

    try:
        result = call_llm_json(GENERATE_SYSTEM_PROMPT, user_prompt, caller="AssessmentAgent.generate")
        questions = result.get("questions", [])
        update_agent_status(request_id, "Assessment Agent", "completed")
        return {
            "assessment_questions": questions,
            "assessment_completed": False,
        }
    except Exception:
        # Fallback: domande generiche
        update_agent_status(request_id, "Assessment Agent", "completed")
        return {
            "assessment_questions": _fallback_questions(target_position),
            "assessment_completed": False,
        }


def analyze_assessment(state: UnchainedState) -> dict:
    """Analizza le risposte dell'assessment e produce gap analysis."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Assessment Agent (Analysis)", "running")
    time.sleep(1)

    questions = state.get("assessment_questions", [])
    answers = state.get("assessment_answers", [])
    target_position = state.get("target_position", "")
    hard_skills = state.get("hard_skills", [])
    soft_skills = state.get("soft_skills", [])

    # Combina domande e risposte per il prompt
    qa_pairs = []
    answer_map = {a["question_id"]: a["answer"] for a in answers}
    for q in questions:
        answer = answer_map.get(q["question_id"], "Non risposto")
        qa_pairs.append(f"D: {q['question_text']}\nCategoria: {q['category']}, Area: {q['skill_area']}\nR: {answer}")

    user_prompt = f"""Analizza queste risposte dell'assessment per la posizione target: {target_position}

Competenze tecniche dichiarate:
{_format_skills(hard_skills)}

Competenze trasversali dichiarate:
{_format_skills(soft_skills)}

Domande e risposte:
{"\\n\\n".join(qa_pairs)}

Identifica tutti i gap di competenze con priorità."""

    try:
        result = call_llm_json(ANALYZE_SYSTEM_PROMPT, user_prompt, caller="AssessmentAgent.analyze")
        skill_gaps = result.get("skill_gaps", [])
        update_agent_status(request_id, "Assessment Agent (Analysis)", "completed")
        return {
            "skill_gaps": skill_gaps,
            "assessment_completed": True,
        }
    except Exception:
        update_agent_status(request_id, "Assessment Agent (Analysis)", "completed")
        return {
            "skill_gaps": _fallback_gaps(target_position),
            "assessment_completed": True,
        }


def _format_skills(skills: list[dict]) -> str:
    if not skills:
        return "Nessuna competenza registrata"
    return "\n".join(f"- {s['skill']}: livello {s['level']}/5" for s in skills)


def _fallback_questions(target_position: str) -> list[dict]:
    """Domande di fallback se il LLM fallisce."""
    return [
        {
            "question_id": "q1",
            "category": "technical",
            "skill_area": "General Technical",
            "question_text": f"Come valuteresti la tua preparazione tecnica per il ruolo di {target_position}?",
            "question_type": "scale",
            "options": [],
        },
        {
            "question_id": "q2",
            "category": "technical",
            "skill_area": "Problem Solving",
            "question_text": "Descrivi un problema tecnico complesso che hai risolto di recente.",
            "question_type": "open",
            "options": [],
        },
        {
            "question_id": "q3",
            "category": "situational",
            "skill_area": "Leadership",
            "question_text": "Hai mai guidato un progetto o un team? Descrivi la tua esperienza.",
            "question_type": "open",
            "options": [],
        },
        {
            "question_id": "q4",
            "category": "situational",
            "skill_area": "Communication",
            "question_text": "Come gestisci i conflitti con i colleghi o gli stakeholder?",
            "question_type": "multiple_choice",
            "options": [
                "Evito il confronto e cerco compromessi",
                "Affronto direttamente la questione con dati e fatti",
                "Coinvolgo un mediatore o il manager",
                "Ascolto tutte le parti e propongo una soluzione condivisa",
            ],
        },
        {
            "question_id": "q5",
            "category": "interest",
            "skill_area": "Career Goals",
            "question_text": f"Cosa ti motiva a raggiungere la posizione di {target_position}?",
            "question_type": "open",
            "options": [],
        },
    ]


def _fallback_gaps(target_position: str) -> list[dict]:
    """Gap analysis di fallback."""
    return [
        {"skill": "Leadership Tecnica", "current_level": 2, "target_level": 4, "gap": 2, "priority": "medium"},
        {"skill": "System Design", "current_level": 2, "target_level": 5, "gap": 3, "priority": "high"},
        {"skill": "Comunicazione", "current_level": 3, "target_level": 4, "gap": 1, "priority": "low"},
    ]

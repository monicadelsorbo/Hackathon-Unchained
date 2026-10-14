"""
Course Creator Agent — Crea corsi personalizzati per ogni modulo del piano.
Per ogni modulo genera:
- Lezioni con testo formativo
- Video YouTube pertinenti
- Quiz di verifica apprendimento
"""

from __future__ import annotations
import time
from state import UnchainedState
from llm import call_llm_json
from store import update_agent_status


SYSTEM_PROMPT = """Sei un instructional designer esperto. Devi creare un corso personalizzato per un dipendente che sta seguendo un piano di formazione.

Per il modulo fornito, genera un corso con 2-3 lezioni. Ogni lezione deve contenere:

1. **content_markdown**: Un testo formativo in markdown (300-500 parole) che spieghi l'argomento in modo chiaro e pratico, con esempi concreti. Usa heading, bullet list, code block dove appropriato.

2. **youtube_videos**: 2-3 video YouTube reali e pertinenti. Per ogni video fornisci:
   - video_id: l'ID YouTube (es. "dQw4w9WgXcQ")
   - title: titolo descrittivo
   - url: link completo YouTube
   - channel: nome del canale
   - duration_minutes: durata stimata
   - relevance_note: perché questo video è utile per l'apprendimento

3. **quiz**: 2-3 domande a scelta multipla per verificare l'apprendimento. Per ogni domanda:
   - question_text: testo della domanda
   - options: esattamente 4 opzioni
   - correct_answer: indice della risposta corretta (0-3)
   - explanation: spiegazione della risposta corretta

Rispondi con un JSON con questa struttura:
{
    "title": "Titolo del corso personalizzato",
    "description": "Breve descrizione (1-2 frasi)",
    "estimated_hours": 5.0,
    "lessons": [
        {
            "lesson_id": "l1",
            "title": "Titolo lezione",
            "content_markdown": "# Titolo\\n\\nContenuto formativo...",
            "youtube_videos": [...],
            "quiz": [
                {
                    "quiz_id": "q1",
                    "question_text": "Domanda...",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 0,
                    "explanation": "Spiegazione..."
                }
            ]
        }
    ]
}

Importante:
- I video YouTube devono essere REALI e pertinenti (canali noti di formazione tecnica)
- Il testo deve essere personalizzato per il livello attuale del dipendente
- I quiz devono testare la comprensione, non la memoria
- Rispondi SOLO con il JSON"""


def create_course_for_module(
    module: dict,
    employee_name: str = "Dipendente",
    current_role: str = "",
    target_position: str = "",
    skill_gaps: list | None = None,
) -> dict:
    """Genera un corso personalizzato per un singolo modulo. Chiamabile on-demand."""
    gap_map = {g["skill"].lower(): g for g in (skill_gaps or [])}

    module_id = module.get("module_id", "mod-1")
    topics = module.get("topics", [])
    title = module.get("title", "")
    skill_area = module.get("skill_area", "hard")

    current_level = 2
    for topic in topics:
        gap = gap_map.get(topic.lower())
        if gap:
            current_level = gap["current_level"]
            break

    level_desc = {1: "principiante", 2: "base", 3: "intermedio", 4: "avanzato", 5: "esperto"}

    user_prompt = f"""Crea un corso personalizzato per questo modulo:

Modulo: {title}
Argomenti: {', '.join(topics)}
Area: {skill_area}
Descrizione modulo: {module.get('description', '')}

Profilo studente:
- Nome: {employee_name}
- Ruolo attuale: {current_role}
- Posizione target: {target_position}
- Livello attuale negli argomenti: {level_desc.get(current_level, 'intermedio')}

Il corso deve partire dal livello {level_desc.get(current_level, 'intermedio')} e portare verso un livello avanzato.
Scegli video YouTube di canali formativi reali e noti (es. freeCodeCamp, Fireship, Traversy Media, The Coding Train, CS Dojo, Tech With Tim, ArjanCodes, ecc. per tech; The Futur, NNGroup per design; Harvard Business Review per leadership)."""

    try:
        result = call_llm_json(SYSTEM_PROMPT, user_prompt, caller=f"CourseCreator[{module_id}]")
        lessons = result.get("lessons", [])

        for j, lesson in enumerate(lessons):
            lesson["lesson_id"] = f"{module_id}-l{j+1}"
            for k, q in enumerate(lesson.get("quiz", [])):
                q["quiz_id"] = f"{module_id}-l{j+1}-q{k+1}"

        return {
            "custom_course_id": f"cc-{module_id}",
            "module_id": module_id,
            "title": result.get("title", f"Corso: {title}"),
            "skill_area": skill_area,
            "description": result.get("description", ""),
            "lessons": lessons,
            "estimated_hours": result.get("estimated_hours", 5.0),
        }

    except Exception:
        return _fallback_course(module_id, title, skill_area, topics)


def _fallback_course(module_id: str, title: str, skill_area: str, topics: list[str]) -> dict:
    """Corso di fallback se il LLM fallisce."""
    return {
        "custom_course_id": f"cc-{module_id}",
        "module_id": module_id,
        "title": f"Corso Personalizzato: {title}",
        "skill_area": skill_area,
        "description": f"Corso personalizzato su {', '.join(topics[:3])}.",
        "estimated_hours": 4.0,
        "lessons": [
            {
                "lesson_id": f"{module_id}-l1",
                "title": f"Introduzione a {topics[0] if topics else title}",
                "content_markdown": f"# {topics[0] if topics else title}\n\nQuesta lezione copre i fondamenti di {topics[0] if topics else title}.\n\n## Obiettivi\n- Comprendere i concetti base\n- Applicare le conoscenze in scenari pratici\n- Valutare le proprie competenze\n\n## Contenuto\n\nI concetti fondamentali di quest'area includono la comprensione delle best practice, l'applicazione pratica e la capacità di problem solving in contesti reali.\n\n> La formazione continua è la chiave per la crescita professionale.",
                "youtube_videos": [
                    {
                        "video_id": "placeholder",
                        "title": f"Introduzione a {topics[0] if topics else title}",
                        "url": f"https://youtube.com/watch?v=placeholder",
                        "channel": "Formazione Tech",
                        "duration_minutes": 15,
                        "relevance_note": "Video introduttivo sull'argomento.",
                    }
                ],
                "quiz": [
                    {
                        "quiz_id": f"{module_id}-l1-q1",
                        "question_text": f"Quale è l'aspetto più importante di {topics[0] if topics else title}?",
                        "options": [
                            "La teoria senza pratica",
                            "L'applicazione pratica con comprensione dei fondamenti",
                            "La memorizzazione delle regole",
                            "L'imitazione senza comprensione",
                        ],
                        "correct_answer": 1,
                        "explanation": "La combinazione di comprensione teorica e applicazione pratica è fondamentale per un apprendimento efficace.",
                    }
                ],
            }
        ],
    }

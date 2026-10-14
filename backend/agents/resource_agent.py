"""
Resource Agent — Abbina corsi e-learning ai moduli del piano.
No LLM: matching algoritmico puro su tag competenze.
"""

from __future__ import annotations
import time
from state import UnchainedState
from store import update_agent_status
from mock_data import COURSE_CATALOG


def resource_agent(state: UnchainedState) -> dict:
    """Arricchisce ogni modulo del piano con i corsi più rilevanti."""
    request_id = state["request_id"]
    update_agent_status(request_id, "Resource Agent", "running")
    time.sleep(1)

    training_plan = state.get("training_plan", [])
    enriched_plan = []
    used_course_ids: set[str] = set()

    for module in training_plan:
        topics = [t.lower() for t in module.get("topics", [])]
        title_words = module.get("title", "").lower().split()

        # Score ogni corso per rilevanza, escludendo quelli già assegnati
        scored_courses = []
        for course in COURSE_CATALOG:
            if course["course_id"] in used_course_ids:
                continue
            score = _calculate_relevance(course, topics, title_words)
            if score > 0:
                scored_courses.append((score, course))

        # Top 3 corsi per modulo
        scored_courses.sort(key=lambda x: (-x[0], -x[1]["rating"]))
        best_courses = [c for _, c in scored_courses[:3]]

        # Segna come usati
        for c in best_courses:
            used_course_ids.add(c["course_id"])

        enriched_module = {**module, "courses": best_courses}
        enriched_plan.append(enriched_module)

    update_agent_status(request_id, "Resource Agent", "completed")
    return {
        "training_plan": enriched_plan,
        "resources_enriched": True,
    }


def _calculate_relevance(course: dict, topics: list[str], title_words: list[str]) -> float:
    """Calcola score di rilevanza tra un corso e un modulo."""
    score = 0.0
    course_tags = [t.lower() for t in course.get("skill_tags", [])]
    course_title = course.get("title", "").lower()

    # Match diretto sui tag
    for topic in topics:
        for tag in course_tags:
            if topic in tag or tag in topic:
                score += 3.0

    # Match parziale sul titolo del corso
    for word in title_words:
        if len(word) > 3 and word in course_title:
            score += 1.0

    # Bonus per rating alto
    rating = course.get("rating", 0)
    if rating >= 4.5:
        score += 0.5

    return score

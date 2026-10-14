"""
UNCHAINED - SQLite-backed state store.
Stessa interfaccia del vecchio in-memory store, ma persiste su SQLite.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from db import get_connection

logger = logging.getLogger("unchained.store")


# ── Save State ─────────────────────────────────────────────────────────────


def save_state(request_id: str, state: dict) -> None:
    """Salva o aggiorna lo stato completo di una richiesta nel DB."""
    conn = get_connection()
    try:
        _save_request(conn, request_id, state)
        _save_profile(conn, request_id, state)
        _save_agent_statuses(conn, request_id, state.get("agent_statuses", []))
        _save_assessment_questions(conn, request_id, state.get("assessment_questions"))
        _save_assessment_answers(conn, request_id, state.get("assessment_answers"))
        _save_skill_gaps(conn, request_id, state.get("skill_gaps"))
        _save_training_modules(conn, request_id, state.get("training_plan"))
        _save_custom_courses(conn, request_id, state.get("custom_courses"))
        _save_cost_breakdown(conn, request_id, state.get("cost_breakdown"))
        _save_mentor(conn, request_id, state.get("assigned_mentor"))
        _save_review(conn, request_id, state)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Get State ──────────────────────────────────────────────────────────────


def get_state(request_id: str) -> dict | None:
    """Ricostruisce lo stato completo da SQLite."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM requests WHERE request_id = ?", (request_id,)).fetchone()
        if row is None:
            return None

        state: dict = {
            "request_id": row["request_id"],
            "requester_type": row["requester_type"],
            "requester_id": row["requester_id"],
            "employee_id": row["employee_id"],
            "target_position": row["target_position"],
            "request_reason": row["request_reason"],
            "current_phase": row["current_phase"],
        }
        if row["error"]:
            state["error"] = row["error"]

        # Profile
        profile = conn.execute("SELECT * FROM profiles WHERE request_id = ?", (request_id,)).fetchone()
        if profile:
            state["employee_name"] = profile["employee_name"]
            state["current_role"] = profile["current_role"]
            state["cv_text"] = profile["cv_text"]
            state["experience_summary"] = profile["experience_summary"]
            state["hard_skills"] = json.loads(profile["hard_skills_json"])
            state["soft_skills"] = json.loads(profile["soft_skills_json"])

        # Agent statuses
        rows = conn.execute(
            "SELECT agent_name, status, started_at, completed_at FROM agent_statuses WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        state["agent_statuses"] = [dict(r) for r in rows]

        # Assessment questions
        q_rows = conn.execute(
            "SELECT question_id, category, skill_area, question_text, question_type, options_json "
            "FROM assessment_questions WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        if q_rows:
            state["assessment_questions"] = [
                {
                    "question_id": r["question_id"],
                    "category": r["category"],
                    "skill_area": r["skill_area"],
                    "question_text": r["question_text"],
                    "question_type": r["question_type"],
                    "options": json.loads(r["options_json"]),
                }
                for r in q_rows
            ]

        # Assessment answers
        a_rows = conn.execute(
            "SELECT question_id, answer FROM assessment_answers WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        if a_rows:
            state["assessment_answers"] = [
                {"question_id": r["question_id"], "answer": r["answer"]}
                for r in a_rows
            ]
            state["assessment_completed"] = True

        # Skill gaps
        g_rows = conn.execute(
            "SELECT skill, current_level, target_level, gap, priority "
            "FROM skill_gaps WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        if g_rows:
            state["skill_gaps"] = [dict(r) for r in g_rows]

        # Training modules
        m_rows = conn.execute(
            "SELECT module_id, title, description, skill_area, topics_json, courses_json, "
            "duration_weeks, milestone FROM training_modules "
            "WHERE request_id = ? ORDER BY sort_order",
            (request_id,),
        ).fetchall()
        if m_rows:
            state["training_plan"] = [
                {
                    "module_id": r["module_id"],
                    "title": r["title"],
                    "description": r["description"],
                    "skill_area": r["skill_area"],
                    "topics": json.loads(r["topics_json"]),
                    "courses": json.loads(r["courses_json"]),
                    "duration_weeks": r["duration_weeks"],
                    "milestone": r["milestone"],
                }
                for r in m_rows
            ]

        # Custom courses
        cc_rows = conn.execute(
            "SELECT custom_course_id, module_id, title, skill_area, description, "
            "estimated_hours, lessons_json FROM custom_courses WHERE request_id = ? ORDER BY id",
            (request_id,),
        ).fetchall()
        if cc_rows:
            state["custom_courses"] = [
                {
                    "custom_course_id": r["custom_course_id"],
                    "module_id": r["module_id"],
                    "title": r["title"],
                    "skill_area": r["skill_area"],
                    "description": r["description"],
                    "estimated_hours": r["estimated_hours"],
                    "lessons": json.loads(r["lessons_json"]),
                }
                for r in cc_rows
            ]

        # Cost breakdown
        cost = conn.execute("SELECT * FROM cost_breakdowns WHERE request_id = ?", (request_id,)).fetchone()
        if cost:
            state["cost_breakdown"] = {
                "total_course_cost_eur": cost["total_course_cost_eur"],
                "total_hours": cost["total_hours"],
                "estimated_duration_weeks": cost["estimated_duration_weeks"],
                "roi_estimate": cost["roi_estimate"],
                "cost_per_module": json.loads(cost["cost_per_module_json"]),
            }

        # Mentor
        mentor = conn.execute("SELECT * FROM mentor_assignments WHERE request_id = ?", (request_id,)).fetchone()
        if mentor:
            state["assigned_mentor"] = {
                "mentor_id": mentor["mentor_id"],
                "name": mentor["name"],
                "role": mentor["role"],
                "expertise": json.loads(mentor["expertise_json"]),
                "match_score": mentor["match_score"],
                "rationale": mentor["rationale"],
                "availability": mentor["availability"],
            }

        # Review (latest)
        review = conn.execute(
            "SELECT * FROM reviews WHERE request_id = ? ORDER BY id DESC LIMIT 1",
            (request_id,),
        ).fetchone()
        if review:
            state["review_status"] = review["review_status"]
            state["review_iteration"] = review["review_iteration"]
            if review["review_status"] != "pending_review":
                state["review_feedback"] = {
                    "status": review["review_status"],
                    "comments": review["comments"],
                    "requested_changes": json.loads(review["requested_changes_json"]),
                }

        return state
    finally:
        conn.close()


# ── Other queries ──────────────────────────────────────────────────────────


def get_all_requests() -> list[dict]:
    """Restituisce un sommario di tutte le richieste."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT r.request_id, r.employee_id, r.target_position, r.current_phase, "
            "r.requester_type, p.employee_name, "
            "(SELECT rv.review_status FROM reviews rv WHERE rv.request_id = r.request_id ORDER BY rv.id DESC LIMIT 1) as review_status "
            "FROM requests r LEFT JOIN profiles p ON r.request_id = p.request_id "
            "ORDER BY r.created_at DESC"
        ).fetchall()
        return [
            {
                "request_id": r["request_id"],
                "employee_id": r["employee_id"],
                "employee_name": r["employee_name"] or "",
                "target_position": r["target_position"],
                "current_phase": r["current_phase"],
                "requester_type": r["requester_type"],
                "review_status": r["review_status"] or "",
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_plans_for_employee(employee_id: str) -> list[dict]:
    """Restituisce tutti i piani per un dipendente."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT request_id FROM requests WHERE employee_id = ? ORDER BY created_at DESC",
            (employee_id,),
        ).fetchall()
        plans = []
        for r in rows:
            state = get_state(r["request_id"])
            if state:
                plans.append(state)
        return plans
    finally:
        conn.close()


def update_agent_status(request_id: str, agent_name: str, status: str) -> None:
    """Aggiorna lo status di un agente (per polling real-time)."""
    conn = get_connection()
    now = datetime.now(timezone.utc).isoformat()
    try:
        existing = conn.execute(
            "SELECT id, started_at FROM agent_statuses WHERE request_id = ? AND agent_name = ?",
            (request_id, agent_name),
        ).fetchone()

        if existing:
            updates = {"status": status}
            if status == "running" and not existing["started_at"]:
                updates["started_at"] = now
            if status in ("completed", "error"):
                updates["completed_at"] = now

            set_clause = ", ".join(f"{k} = ?" for k in updates)
            conn.execute(
                f"UPDATE agent_statuses SET {set_clause} WHERE id = ?",
                (*updates.values(), existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO agent_statuses (request_id, agent_name, status, started_at, completed_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    request_id,
                    agent_name,
                    status,
                    now if status == "running" else "",
                    now if status in ("completed", "error") else "",
                ),
            )
        conn.commit()
    finally:
        conn.close()


# ── Private save helpers ───────────────────────────────────────────────────


def _save_request(conn, request_id: str, state: dict) -> None:
    conn.execute(
        "INSERT INTO requests (request_id, requester_type, requester_id, employee_id, "
        "target_position, request_reason, current_phase, error, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now')) "
        "ON CONFLICT(request_id) DO UPDATE SET "
        "current_phase=excluded.current_phase, error=excluded.error, updated_at=datetime('now')",
        (
            request_id,
            state.get("requester_type", ""),
            state.get("requester_id", ""),
            state.get("employee_id", ""),
            state.get("target_position", ""),
            state.get("request_reason", ""),
            state.get("current_phase", "initializing"),
            state.get("error"),
        ),
    )


def _save_profile(conn, request_id: str, state: dict) -> None:
    if not state.get("employee_name"):
        return
    conn.execute(
        "INSERT INTO profiles (request_id, employee_name, current_role, cv_text, "
        "experience_summary, hard_skills_json, soft_skills_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(request_id) DO UPDATE SET "
        "employee_name=excluded.employee_name, current_role=excluded.current_role, "
        "cv_text=excluded.cv_text, experience_summary=excluded.experience_summary, "
        "hard_skills_json=excluded.hard_skills_json, soft_skills_json=excluded.soft_skills_json",
        (
            request_id,
            state.get("employee_name", ""),
            state.get("current_role", ""),
            state.get("cv_text", ""),
            state.get("experience_summary", ""),
            json.dumps(state.get("hard_skills", []), ensure_ascii=False),
            json.dumps(state.get("soft_skills", []), ensure_ascii=False),
        ),
    )


def _save_agent_statuses(conn, request_id: str, statuses: list[dict]) -> None:
    for s in statuses:
        conn.execute(
            "INSERT INTO agent_statuses (request_id, agent_name, status, started_at, completed_at) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(request_id, agent_name) DO UPDATE SET "
            "status=excluded.status, started_at=excluded.started_at, completed_at=excluded.completed_at",
            (
                request_id,
                s.get("agent_name", ""),
                s.get("status", "pending"),
                s.get("started_at", ""),
                s.get("completed_at", ""),
            ),
        )


def _save_assessment_questions(conn, request_id: str, questions: list[dict] | None) -> None:
    if not questions:
        return
    for q in questions:
        conn.execute(
            "INSERT INTO assessment_questions (request_id, question_id, category, skill_area, "
            "question_text, question_type, options_json) VALUES (?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(request_id, question_id) DO UPDATE SET "
            "category=excluded.category, skill_area=excluded.skill_area, "
            "question_text=excluded.question_text, question_type=excluded.question_type, "
            "options_json=excluded.options_json",
            (
                request_id,
                q.get("question_id", ""),
                q.get("category", ""),
                q.get("skill_area", ""),
                q.get("question_text", ""),
                q.get("question_type", ""),
                json.dumps(q.get("options", []), ensure_ascii=False),
            ),
        )


def _save_assessment_answers(conn, request_id: str, answers: list[dict] | None) -> None:
    if not answers:
        return
    for a in answers:
        conn.execute(
            "INSERT INTO assessment_answers (request_id, question_id, answer) VALUES (?, ?, ?) "
            "ON CONFLICT(request_id, question_id) DO UPDATE SET answer=excluded.answer",
            (request_id, a.get("question_id", ""), str(a.get("answer", ""))),
        )


def _save_skill_gaps(conn, request_id: str, gaps: list[dict] | None) -> None:
    if not gaps:
        return
    # Cancella e reinserisci (piu' semplice per update)
    conn.execute("DELETE FROM skill_gaps WHERE request_id = ?", (request_id,))
    for g in gaps:
        conn.execute(
            "INSERT INTO skill_gaps (request_id, skill, current_level, target_level, gap, priority) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (request_id, g["skill"], g["current_level"], g["target_level"], g["gap"], g["priority"]),
        )


def _save_training_modules(conn, request_id: str, modules: list[dict] | None) -> None:
    if not modules:
        return
    conn.execute("DELETE FROM training_modules WHERE request_id = ?", (request_id,))
    for i, m in enumerate(modules):
        conn.execute(
            "INSERT INTO training_modules (request_id, module_id, title, description, skill_area, "
            "topics_json, courses_json, duration_weeks, milestone, sort_order) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                request_id,
                m.get("module_id", f"mod-{i+1}"),
                m.get("title", ""),
                m.get("description", ""),
                m.get("skill_area", "hard"),
                json.dumps(m.get("topics", []), ensure_ascii=False),
                json.dumps(m.get("courses", []), ensure_ascii=False),
                m.get("duration_weeks", 2),
                m.get("milestone", ""),
                i,
            ),
        )


def _save_custom_courses(conn, request_id: str, courses: list[dict] | None) -> None:
    if not courses:
        return
    conn.execute("DELETE FROM custom_courses WHERE request_id = ?", (request_id,))
    for c in courses:
        conn.execute(
            "INSERT INTO custom_courses (request_id, custom_course_id, module_id, title, "
            "skill_area, description, estimated_hours, lessons_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                request_id,
                c.get("custom_course_id", ""),
                c.get("module_id", ""),
                c.get("title", ""),
                c.get("skill_area", "hard"),
                c.get("description", ""),
                c.get("estimated_hours", 0),
                json.dumps(c.get("lessons", []), ensure_ascii=False),
            ),
        )


def _save_cost_breakdown(conn, request_id: str, cost: dict | None) -> None:
    if not cost:
        return
    conn.execute(
        "INSERT INTO cost_breakdowns (request_id, total_course_cost_eur, total_hours, "
        "estimated_duration_weeks, roi_estimate, cost_per_module_json) "
        "VALUES (?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(request_id) DO UPDATE SET "
        "total_course_cost_eur=excluded.total_course_cost_eur, total_hours=excluded.total_hours, "
        "estimated_duration_weeks=excluded.estimated_duration_weeks, roi_estimate=excluded.roi_estimate, "
        "cost_per_module_json=excluded.cost_per_module_json",
        (
            request_id,
            cost.get("total_course_cost_eur", 0),
            cost.get("total_hours", 0),
            cost.get("estimated_duration_weeks", 0),
            cost.get("roi_estimate", ""),
            json.dumps(cost.get("cost_per_module", []), ensure_ascii=False),
        ),
    )


def _save_mentor(conn, request_id: str, mentor: dict | None) -> None:
    if not mentor:
        return
    conn.execute(
        "INSERT INTO mentor_assignments (request_id, mentor_id, name, role, expertise_json, "
        "match_score, rationale, availability) VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(request_id) DO UPDATE SET "
        "mentor_id=excluded.mentor_id, name=excluded.name, role=excluded.role, "
        "expertise_json=excluded.expertise_json, match_score=excluded.match_score, "
        "rationale=excluded.rationale, availability=excluded.availability",
        (
            request_id,
            mentor.get("mentor_id", ""),
            mentor.get("name", ""),
            mentor.get("role", ""),
            json.dumps(mentor.get("expertise", []), ensure_ascii=False),
            mentor.get("match_score", 0),
            mentor.get("rationale", ""),
            mentor.get("availability", ""),
        ),
    )


def _save_review(conn, request_id: str, state: dict) -> None:
    review_feedback = state.get("review_feedback")
    review_status = state.get("review_status")
    # Deriva review_status da review_feedback se non esplicito
    if not review_status and review_feedback:
        review_status = review_feedback.get("status")
    if not review_status:
        return
    review_iteration = state.get("review_iteration", 0)

    # Inserisci solo se non esiste gia' questa iterazione
    existing = conn.execute(
        "SELECT id FROM reviews WHERE request_id = ? AND review_iteration = ?",
        (request_id, review_iteration),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE reviews SET review_status = ?, comments = ?, requested_changes_json = ? WHERE id = ?",
            (
                review_status,
                review_feedback.get("comments", "") if review_feedback else "",
                json.dumps(review_feedback.get("requested_changes", []), ensure_ascii=False) if review_feedback else "[]",
                existing["id"],
            ),
        )
    else:
        conn.execute(
            "INSERT INTO reviews (request_id, review_status, comments, requested_changes_json, review_iteration) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                request_id,
                review_status,
                review_feedback.get("comments", "") if review_feedback else "",
                json.dumps(review_feedback.get("requested_changes", []), ensure_ascii=False) if review_feedback else "[]",
                review_iteration,
            ),
        )


# ── Seed helpers ───────────────────────────────────────────────────────────


def seed_mock_data() -> None:
    """Popola il DB con i dati mock (dipendenti, mentori, corsi)."""
    from mock_data import EMPLOYEES, MANAGERS, MENTORS, COURSE_CATALOG

    conn = get_connection()
    try:
        # Employees
        for emp in EMPLOYEES.values():
            conn.execute(
                "INSERT OR IGNORE INTO employees (employee_id, name, current_role, department, cv_text, hr_notes) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (emp["id"], emp["name"], emp["current_role"], emp.get("department", ""),
                 emp.get("cv_text", ""), emp.get("hr_notes", "")),
            )

        # Managers
        for mgr in MANAGERS.values():
            conn.execute(
                "INSERT OR IGNORE INTO managers (manager_id, name, role, department, email) "
                "VALUES (?, ?, ?, ?, ?)",
                (mgr["id"], mgr["name"], mgr["role"], mgr.get("department", ""), mgr.get("email", "")),
            )

        # Mentors
        for m in MENTORS:
            conn.execute(
                "INSERT OR IGNORE INTO mentors (mentor_id, name, role, expertise_json, "
                "completed_mentorships, availability, bio) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (m["mentor_id"], m["name"], m["role"],
                 json.dumps(m["expertise"], ensure_ascii=False),
                 m.get("completed_mentorships", 0), m.get("availability", ""), m.get("bio", "")),
            )

        # Course catalog
        for c in COURSE_CATALOG:
            conn.execute(
                "INSERT OR IGNORE INTO course_catalog (course_id, title, platform, url, "
                "duration_hours, cost_eur, rating, skill_tags_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (c["course_id"], c["title"], c["platform"], c["url"],
                 c["duration_hours"], c["cost_eur"], c["rating"],
                 json.dumps(c["skill_tags"], ensure_ascii=False)),
            )

        conn.commit()
        logger.info(
            "Mock data seeded: %d employees, %d managers, %d mentors, %d courses",
            len(EMPLOYEES), len(MANAGERS), len(MENTORS), len(COURSE_CATALOG),
        )
    finally:
        conn.close()

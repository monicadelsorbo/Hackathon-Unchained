"""
UNCHAINED - SQLite database schema and connection.
"""

import sqlite3
import os
import logging

logger = logging.getLogger("unchained.db")

DB_PATH = os.getenv("UNCHAINED_DB_PATH", os.path.join(os.path.dirname(__file__), "unchained.db"))


def get_connection() -> sqlite3.Connection:
    """Crea una connessione SQLite con row_factory."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Crea tutte le tabelle se non esistono."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
        logger.info("Database inizializzato: %s", DB_PATH)
    finally:
        conn.close()


SCHEMA = """
-- ── Richieste di piano ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS requests (
    request_id      TEXT PRIMARY KEY,
    requester_type  TEXT NOT NULL,           -- 'manager' | 'employee'
    requester_id    TEXT NOT NULL,
    employee_id     TEXT NOT NULL,
    target_position TEXT NOT NULL,
    request_reason  TEXT NOT NULL DEFAULT '',
    current_phase   TEXT NOT NULL DEFAULT 'initializing',
    error           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Profilo estratto dal CV ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS profiles (
    request_id          TEXT PRIMARY KEY REFERENCES requests(request_id),
    employee_name       TEXT,
    current_role        TEXT,
    cv_text             TEXT,
    experience_summary  TEXT,
    hard_skills_json    TEXT DEFAULT '[]',   -- JSON array di {skill, level}
    soft_skills_json    TEXT DEFAULT '[]'
);

-- ── Status degli agenti (per polling real-time) ─────────────────────────

CREATE TABLE IF NOT EXISTS agent_statuses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id      TEXT NOT NULL REFERENCES requests(request_id),
    agent_name      TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',  -- pending|running|completed|error
    started_at      TEXT DEFAULT '',
    completed_at    TEXT DEFAULT '',
    UNIQUE(request_id, agent_name)
);

-- ── Assessment: domande e risposte ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS assessment_questions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id      TEXT NOT NULL REFERENCES requests(request_id),
    question_id     TEXT NOT NULL,
    category        TEXT NOT NULL,           -- technical|situational|interest
    skill_area      TEXT NOT NULL,
    question_text   TEXT NOT NULL,
    question_type   TEXT NOT NULL,           -- multiple_choice|scale|open
    options_json    TEXT DEFAULT '[]',       -- JSON array di stringhe
    UNIQUE(request_id, question_id)
);

CREATE TABLE IF NOT EXISTS assessment_answers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id      TEXT NOT NULL REFERENCES requests(request_id),
    question_id     TEXT NOT NULL,
    answer          TEXT NOT NULL,           -- stringa o numero come testo
    UNIQUE(request_id, question_id)
);

-- ── Skill Gaps ──────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS skill_gaps (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id      TEXT NOT NULL REFERENCES requests(request_id),
    skill           TEXT NOT NULL,
    current_level   INTEGER NOT NULL,
    target_level    INTEGER NOT NULL,
    gap             INTEGER NOT NULL,
    priority        TEXT NOT NULL            -- high|medium|low
);

-- ── Piano di formazione: moduli ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS training_modules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id      TEXT NOT NULL REFERENCES requests(request_id),
    module_id       TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT DEFAULT '',
    skill_area      TEXT NOT NULL,           -- hard|soft
    topics_json     TEXT DEFAULT '[]',       -- JSON array
    courses_json    TEXT DEFAULT '[]',       -- JSON array di CourseResource
    duration_weeks  INTEGER DEFAULT 2,
    milestone       TEXT DEFAULT '',
    sort_order      INTEGER DEFAULT 0,
    UNIQUE(request_id, module_id)
);

-- ── Corsi personalizzati (Course Creator Agent) ─────────────────────────

CREATE TABLE IF NOT EXISTS custom_courses (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id          TEXT NOT NULL REFERENCES requests(request_id),
    custom_course_id    TEXT NOT NULL,
    module_id           TEXT NOT NULL,
    title               TEXT NOT NULL,
    skill_area          TEXT NOT NULL,
    description         TEXT DEFAULT '',
    estimated_hours     REAL DEFAULT 0,
    lessons_json        TEXT DEFAULT '[]',   -- JSON array di LessonContent
    UNIQUE(request_id, custom_course_id)
);

-- ── Cost Breakdown ──────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS cost_breakdowns (
    request_id              TEXT PRIMARY KEY REFERENCES requests(request_id),
    total_course_cost_eur   REAL DEFAULT 0,
    total_hours             REAL DEFAULT 0,
    estimated_duration_weeks INTEGER DEFAULT 0,
    roi_estimate            TEXT DEFAULT '',
    cost_per_module_json    TEXT DEFAULT '[]'    -- JSON array
);

-- ── Mentor Assignment ───────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS mentor_assignments (
    request_id      TEXT PRIMARY KEY REFERENCES requests(request_id),
    mentor_id       TEXT NOT NULL,
    name            TEXT NOT NULL,
    role            TEXT NOT NULL,
    expertise_json  TEXT DEFAULT '[]',
    match_score     REAL DEFAULT 0,
    rationale       TEXT DEFAULT '',
    availability    TEXT DEFAULT ''
);

-- ── Reviews ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS reviews (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id              TEXT NOT NULL REFERENCES requests(request_id),
    review_status           TEXT NOT NULL,           -- approved|changes_requested|pending_review
    comments                TEXT DEFAULT '',
    requested_changes_json  TEXT DEFAULT '[]',
    review_iteration        INTEGER DEFAULT 0,
    created_at              TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Catalogo corsi e-learning ───────────────────────────────────────────

CREATE TABLE IF NOT EXISTS course_catalog (
    course_id       TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    platform        TEXT NOT NULL,
    url             TEXT NOT NULL,
    duration_hours  REAL DEFAULT 0,
    cost_eur        REAL DEFAULT 0,
    rating          REAL DEFAULT 0,
    skill_tags_json TEXT DEFAULT '[]'
);

-- ── Dipendenti ──────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS employees (
    employee_id     TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    current_role    TEXT NOT NULL,
    department      TEXT DEFAULT '',
    cv_text         TEXT DEFAULT '',
    hr_notes        TEXT DEFAULT ''
);

-- ── Manager ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS managers (
    manager_id      TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    role            TEXT NOT NULL,
    department      TEXT DEFAULT '',
    email           TEXT DEFAULT ''
);

-- ── Mentori ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS mentors (
    mentor_id               TEXT PRIMARY KEY,
    name                    TEXT NOT NULL,
    role                    TEXT NOT NULL,
    expertise_json          TEXT DEFAULT '[]',
    completed_mentorships   INTEGER DEFAULT 0,
    availability            TEXT DEFAULT '',
    bio                     TEXT DEFAULT ''
);
"""

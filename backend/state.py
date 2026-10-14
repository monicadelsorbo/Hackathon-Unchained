"""
UNCHAINED - LangGraph State Definition
Stato globale condiviso tra tutti gli agenti del sistema multi-agente.
"""

from __future__ import annotations

from typing import TypedDict
from typing_extensions import NotRequired


# ── Sub-types ──────────────────────────────────────────────────────────────


class SkillLevel(TypedDict):
    skill: str
    level: int  # 1-5


class CourseResource(TypedDict):
    course_id: str
    title: str
    platform: str  # "Coursera" | "Udemy" | "LinkedIn Learning"
    url: str
    duration_hours: float
    cost_eur: float
    rating: float
    skill_tags: list[str]


class TrainingModule(TypedDict):
    module_id: str
    title: str
    description: str
    skill_area: str  # "hard" | "soft"
    topics: list[str]
    courses: list[CourseResource]
    duration_weeks: int
    milestone: str


class MentorMatch(TypedDict):
    mentor_id: str
    name: str
    role: str
    expertise: list[str]
    match_score: float
    rationale: str
    availability: str


class AssessmentQuestion(TypedDict):
    question_id: str
    category: str  # "technical" | "situational" | "interest"
    skill_area: str
    question_text: str
    question_type: str  # "multiple_choice" | "scale" | "open"
    options: list[str]  # vuoto per open/scale


class AssessmentAnswer(TypedDict):
    question_id: str
    answer: str | int


class SkillGap(TypedDict):
    skill: str
    current_level: int  # 1-5
    target_level: int  # 1-5
    gap: int
    priority: str  # "high" | "medium" | "low"


class CostBreakdown(TypedDict):
    total_course_cost_eur: float
    total_hours: float
    estimated_duration_weeks: int
    roi_estimate: str
    cost_per_module: list[dict]


class ReviewFeedback(TypedDict):
    status: str  # "approved" | "changes_requested"
    comments: str
    requested_changes: list[str]


class YouTubeVideo(TypedDict):
    video_id: str
    title: str
    url: str
    channel: str
    duration_minutes: int
    relevance_note: str  # perché questo video è utile


class QuizQuestion(TypedDict):
    quiz_id: str
    question_text: str
    options: list[str]  # 4 opzioni
    correct_answer: int  # indice 0-3
    explanation: str  # spiegazione della risposta corretta


class LessonContent(TypedDict):
    lesson_id: str
    title: str
    content_markdown: str  # testo formativo in markdown
    youtube_videos: list[YouTubeVideo]
    quiz: list[QuizQuestion]


class CustomCourse(TypedDict):
    custom_course_id: str
    module_id: str  # a quale modulo del piano è collegato
    title: str
    skill_area: str
    description: str
    lessons: list[LessonContent]
    estimated_hours: float


class AgentStatus(TypedDict):
    agent_name: str
    status: str  # "pending" | "running" | "completed" | "error"
    started_at: str  # ISO timestamp o stringa vuota
    completed_at: str


# ── Main State ─────────────────────────────────────────────────────────────


class UnchainedState(TypedDict):
    # --- Request metadata ---
    request_id: str
    requester_type: str  # "manager" | "employee"
    requester_id: str
    employee_id: str
    target_position: str
    request_reason: str

    # --- Profile Agent outputs ---
    employee_name: NotRequired[str]
    cv_text: NotRequired[str]
    hard_skills: NotRequired[list[SkillLevel]]
    soft_skills: NotRequired[list[SkillLevel]]
    experience_summary: NotRequired[str]
    current_role: NotRequired[str]

    # --- Assessment Agent outputs ---
    assessment_questions: NotRequired[list[AssessmentQuestion]]
    assessment_answers: NotRequired[list[AssessmentAnswer]]
    assessment_completed: NotRequired[bool]
    skill_gaps: NotRequired[list[SkillGap]]

    # --- Plan Agent outputs ---
    training_plan: NotRequired[list[TrainingModule]]
    plan_summary: NotRequired[str]

    # --- Resource Agent outputs ---
    resources_enriched: NotRequired[bool]

    # --- Course Creator Agent outputs ---
    custom_courses: NotRequired[list[CustomCourse]]

    # --- Cost Agent outputs ---
    cost_breakdown: NotRequired[CostBreakdown]

    # --- Mentor Agent outputs ---
    assigned_mentor: NotRequired[MentorMatch]

    # --- Review Agent outputs ---
    review_status: NotRequired[str]  # "pending_review"|"approved"|"changes_requested"
    review_feedback: NotRequired[ReviewFeedback]
    review_iteration: NotRequired[int]

    # --- Notify Agent outputs ---
    dashboard_updated: NotRequired[bool]

    # --- Orchestration metadata ---
    agent_statuses: NotRequired[list[AgentStatus]]
    current_phase: NotRequired[str]  # "profiling"|"assessment"|"planning"|"review"|"complete"
    error: NotRequired[str]

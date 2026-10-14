"""
UNCHAINED - Pydantic request/response models per FastAPI.
"""

from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


# ── Request Models ─────────────────────────────────────────────────────────


class PlanRequest(BaseModel):
    requester_type: Literal["manager", "employee"]
    requester_id: str
    employee_id: str
    target_position: str
    request_reason: str


class AssessmentAnswerRequest(BaseModel):
    request_id: str
    answers: list[dict]  # [{"question_id": str, "answer": str | int}]


class ReviewDecisionRequest(BaseModel):
    status: Literal["approved", "changes_requested"]
    comments: str = ""
    requested_changes: list[str] = []


# ── Response Models ────────────────────────────────────────────────────────


class PlanRequestResponse(BaseModel):
    request_id: str
    status: str


class PlanStatusResponse(BaseModel):
    request_id: str
    employee_id: str
    employee_name: str | None = None
    target_position: str
    current_phase: str
    agent_statuses: list[dict] = []
    # Dati opzionali disponibili a seconda della fase
    hard_skills: list[dict] | None = None
    soft_skills: list[dict] | None = None
    experience_summary: str | None = None
    current_role: str | None = None
    assessment_questions: list[dict] | None = None
    assessment_completed: bool | None = None
    skill_gaps: list[dict] | None = None
    training_plan: list[dict] | None = None
    plan_summary: str | None = None
    cost_breakdown: dict | None = None
    assigned_mentor: dict | None = None
    custom_courses: list[dict] | None = None
    review_status: str | None = None
    review_feedback: dict | None = None


class DashboardResponse(BaseModel):
    employee_id: str
    employee_name: str
    plans: list[dict]

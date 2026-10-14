"""
UNCHAINED - FastAPI endpoints.
"""

from __future__ import annotations

import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from models import (
    PlanRequest,
    PlanRequestResponse,
    AssessmentAnswerRequest,
    ReviewDecisionRequest,
    PlanStatusResponse,
    DashboardResponse,
)
from mock_data import EMPLOYEES
from graph import phase1_graph, phase2_graph, phase3_graph
from agents.course_creator_agent import create_course_for_module
import store


app = FastAPI(title="UNCHAINED", version="1.0.0", description="Multi-agent training plan generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ────────────────────────────────────────────────────────────────


def _init_agent_statuses(phase: str) -> list[dict]:
    """Inizializza gli status degli agenti per una fase."""
    phase_agents = {
        "phase1": ["Profile Agent", "Assessment Agent"],
        "phase2": [
            "Assessment Agent (Analysis)",
            "Plan Agent",
            "Resource Agent",
            "Cost Agent",
            "Mentor Agent",
        ],
        "phase3": ["Review Agent", "Notify Agent"],
        "phase3_revise": ["Review Agent", "Plan Agent", "Resource Agent", "Cost Agent"],
    }
    return [
        {"agent_name": name, "status": "pending", "started_at": "", "completed_at": ""}
        for name in phase_agents.get(phase, [])
    ]


def _run_phase1(request_id: str) -> None:
    """Esegue Fase 1 in background."""
    state = store.get_state(request_id)
    if state is None:
        return

    state["agent_statuses"] = _init_agent_statuses("phase1")
    state["current_phase"] = "profiling"
    store.save_state(request_id, state)

    try:
        result = phase1_graph.invoke(state)
        # Merge result into state
        state.update(result)
        state["current_phase"] = "awaiting_assessment"
        store.save_state(request_id, state)
    except Exception as e:
        state["error"] = str(e)
        state["current_phase"] = "error"
        store.save_state(request_id, state)


def _run_phase2(request_id: str) -> None:
    """Esegue Fase 2 in background."""
    state = store.get_state(request_id)
    if state is None:
        return

    state["agent_statuses"] = _init_agent_statuses("phase2")
    state["current_phase"] = "planning"
    store.save_state(request_id, state)

    try:
        result = phase2_graph.invoke(state)
        state.update(result)
        state["current_phase"] = "pending_review"
        store.save_state(request_id, state)
    except Exception as e:
        state["error"] = str(e)
        state["current_phase"] = "error"
        store.save_state(request_id, state)


def _run_phase3(request_id: str) -> None:
    """Esegue Fase 3 in background."""
    state = store.get_state(request_id)
    if state is None:
        return

    review_feedback = state.get("review_feedback", {})
    if review_feedback.get("status") == "approved":
        state["agent_statuses"] = _init_agent_statuses("phase3")
    else:
        state["agent_statuses"] = _init_agent_statuses("phase3_revise")

    state["current_phase"] = "reviewing"
    store.save_state(request_id, state)

    try:
        result = phase3_graph.invoke(state)
        state.update(result)
        # Se changes_requested, il piano è stato rivisto, torna a pending_review
        if state.get("review_status") != "approved":
            state["current_phase"] = "pending_review"
        store.save_state(request_id, state)
    except Exception as e:
        state["error"] = str(e)
        state["current_phase"] = "error"
        store.save_state(request_id, state)


# ── Endpoints ──────────────────────────────────────────────────────────────


@app.post("/request-plan", response_model=PlanRequestResponse)
async def request_plan(req: PlanRequest, background_tasks: BackgroundTasks):
    """Avvia il flusso di generazione piano."""
    # Verifica che il dipendente esista nei mock
    if req.employee_id not in EMPLOYEES:
        raise HTTPException(status_code=404, detail=f"Employee {req.employee_id} not found")

    request_id = str(uuid.uuid4())
    employee = EMPLOYEES[req.employee_id]

    # Stato iniziale
    initial_state = {
        "request_id": request_id,
        "requester_type": req.requester_type,
        "requester_id": req.requester_id,
        "employee_id": req.employee_id,
        "target_position": req.target_position,
        "request_reason": req.request_reason,
        "cv_text": employee.get("cv_text", ""),
        "current_phase": "initializing",
        "agent_statuses": [],
    }

    store.save_state(request_id, initial_state)

    if req.requester_type == "manager":
        # Il manager avvia direttamente il flusso
        background_tasks.add_task(_run_phase1, request_id)
        return PlanRequestResponse(request_id=request_id, status="processing")
    else:
        # Il dipendente deve attendere approvazione del manager
        initial_state["current_phase"] = "pending_approval"
        store.save_state(request_id, initial_state)
        return PlanRequestResponse(request_id=request_id, status="pending_approval")


@app.get("/plan/{request_id}", response_model=PlanStatusResponse)
async def get_plan(request_id: str):
    """Recupera lo stato completo di una richiesta."""
    state = store.get_state(request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return PlanStatusResponse(
        request_id=state.get("request_id", request_id),
        employee_id=state.get("employee_id", ""),
        employee_name=state.get("employee_name"),
        target_position=state.get("target_position", ""),
        current_phase=state.get("current_phase", "unknown"),
        agent_statuses=state.get("agent_statuses", []),
        hard_skills=state.get("hard_skills"),
        soft_skills=state.get("soft_skills"),
        experience_summary=state.get("experience_summary"),
        current_role=state.get("current_role"),
        assessment_questions=state.get("assessment_questions"),
        assessment_completed=state.get("assessment_completed"),
        skill_gaps=state.get("skill_gaps"),
        training_plan=state.get("training_plan"),
        plan_summary=state.get("plan_summary"),
        cost_breakdown=state.get("cost_breakdown"),
        assigned_mentor=state.get("assigned_mentor"),
        custom_courses=state.get("custom_courses"),
        review_status=state.get("review_status"),
        review_feedback=state.get("review_feedback"),
    )


@app.post("/plan/{request_id}/approve-request", response_model=PlanRequestResponse)
async def approve_request(request_id: str, background_tasks: BackgroundTasks):
    """Manager approva la richiesta di roadmap di un dipendente, avviando Phase 1."""
    state = store.get_state(request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if state.get("current_phase") != "pending_approval":
        raise HTTPException(status_code=400, detail="Request is not pending approval")

    background_tasks.add_task(_run_phase1, request_id)
    return PlanRequestResponse(request_id=request_id, status="processing")


@app.post("/plan/{request_id}/reject-request", response_model=PlanRequestResponse)
async def reject_request(request_id: str):
    """Manager rifiuta la richiesta di roadmap di un dipendente."""
    state = store.get_state(request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if state.get("current_phase") != "pending_approval":
        raise HTTPException(status_code=400, detail="Request is not pending approval")

    state["current_phase"] = "rejected"
    store.save_state(request_id, state)
    return PlanRequestResponse(request_id=request_id, status="rejected")


@app.post("/assessment/answer", response_model=PlanRequestResponse)
async def submit_assessment(req: AssessmentAnswerRequest, background_tasks: BackgroundTasks):
    """Invia risposte assessment, avvia Fase 2."""
    state = store.get_state(req.request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if state.get("current_phase") != "awaiting_assessment":
        raise HTTPException(status_code=400, detail="Assessment not expected at this phase")

    state["assessment_answers"] = req.answers
    store.save_state(req.request_id, state)

    background_tasks.add_task(_run_phase2, req.request_id)
    return PlanRequestResponse(request_id=req.request_id, status="processing_plan")


@app.post("/plan/{request_id}/review", response_model=PlanRequestResponse)
async def review_plan(request_id: str, req: ReviewDecisionRequest, background_tasks: BackgroundTasks):
    """Manager approva o richiede modifiche."""
    state = store.get_state(request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if state.get("current_phase") != "pending_review":
        raise HTTPException(status_code=400, detail="Plan is not pending review")

    state["review_feedback"] = {
        "status": req.status,
        "comments": req.comments,
        "requested_changes": req.requested_changes,
    }
    state["review_status"] = req.status
    store.save_state(request_id, state)

    background_tasks.add_task(_run_phase3, request_id)
    return PlanRequestResponse(request_id=request_id, status="reviewing")


def _run_course_creator(request_id: str, module_id: str) -> None:
    """Genera un corso AI per un singolo modulo, in background."""
    state = store.get_state(request_id)
    if state is None:
        return

    training_plan = state.get("training_plan", [])
    module = next((m for m in training_plan if m.get("module_id") == module_id), None)
    if module is None:
        return

    course = create_course_for_module(
        module=module,
        employee_name=state.get("employee_name", "Dipendente"),
        current_role=state.get("current_role", ""),
        target_position=state.get("target_position", ""),
        skill_gaps=state.get("skill_gaps", []),
    )

    # Aggiungi il corso alla lista esistente
    existing = state.get("custom_courses", [])
    # Rimuovi eventuale corso precedente per lo stesso modulo
    existing = [c for c in existing if c.get("module_id") != module_id]
    existing.append(course)
    state["custom_courses"] = existing
    store.save_state(request_id, state)


@app.post("/plan/{request_id}/generate-course/{module_id}")
async def generate_course(request_id: str, module_id: str, background_tasks: BackgroundTasks):
    """Genera on-demand un corso AI personalizzato per un modulo specifico."""
    state = store.get_state(request_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Request not found")

    training_plan = state.get("training_plan", [])
    module = next((m for m in training_plan if m.get("module_id") == module_id), None)
    if module is None:
        raise HTTPException(status_code=404, detail=f"Module {module_id} not found")

    background_tasks.add_task(_run_course_creator, request_id, module_id)
    return {"status": "generating", "module_id": module_id}


@app.get("/dashboard/{employee_id}", response_model=DashboardResponse)
async def get_dashboard(employee_id: str):
    """Dashboard dipendente con tutti i piani."""
    employee = EMPLOYEES.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    plans = store.get_plans_for_employee(employee_id)

    # Formatta i piani per la dashboard
    formatted_plans = []
    for p in plans:
        formatted_plans.append(
            {
                "request_id": p.get("request_id", ""),
                "target_position": p.get("target_position", ""),
                "current_phase": p.get("current_phase", ""),
                "plan_summary": p.get("plan_summary", ""),
                "review_status": p.get("review_status", ""),
                "training_plan": p.get("training_plan"),
                "cost_breakdown": p.get("cost_breakdown"),
                "assigned_mentor": p.get("assigned_mentor"),
                "custom_courses": p.get("custom_courses"),
                "skill_gaps": p.get("skill_gaps"),
            }
        )

    return DashboardResponse(
        employee_id=employee_id,
        employee_name=employee.get("name", ""),
        plans=formatted_plans,
    )


@app.get("/requests")
async def list_requests():
    """Lista tutte le richieste."""
    return store.get_all_requests()


@app.get("/employees")
async def list_employees():
    """Lista tutti i dipendenti con dati anagrafici e numero di piani."""
    result = []
    for emp in EMPLOYEES.values():
        plans = store.get_plans_for_employee(emp["id"])
        result.append({
            "employee_id": emp["id"],
            "name": emp["name"],
            "current_role": emp["current_role"],
            "department": emp.get("department", ""),
            "plans_count": len(plans),
            "active_plan_phase": plans[0].get("current_phase", "") if plans else None,
        })
    return result


@app.get("/employee/{employee_id}")
async def get_employee(employee_id: str):
    """Profilo completo di un dipendente con tutti i suoi piani."""
    employee = EMPLOYEES.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    plans = store.get_plans_for_employee(employee_id)
    formatted_plans = []
    for p in plans:
        formatted_plans.append({
            "request_id": p.get("request_id", ""),
            "target_position": p.get("target_position", ""),
            "current_phase": p.get("current_phase", ""),
            "plan_summary": p.get("plan_summary", ""),
            "review_status": p.get("review_status", ""),
            "training_plan": p.get("training_plan"),
            "cost_breakdown": p.get("cost_breakdown"),
            "assigned_mentor": p.get("assigned_mentor"),
            "custom_courses": p.get("custom_courses"),
            "skill_gaps": p.get("skill_gaps"),
            "hard_skills": p.get("hard_skills"),
            "soft_skills": p.get("soft_skills"),
            "experience_summary": p.get("experience_summary"),
        })

    return {
        "employee_id": employee["id"],
        "name": employee["name"],
        "current_role": employee["current_role"],
        "department": employee.get("department", ""),
        "hr_notes": employee.get("hr_notes", ""),
        "plans": formatted_plans,
    }

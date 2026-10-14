const API_BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export const api = {
  requestPlan: (data: {
    requester_type: 'manager' | 'employee'
    requester_id: string
    employee_id: string
    target_position: string
    request_reason: string
  }) => request<{ request_id: string; status: string }>('/request-plan', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  getPlan: (requestId: string) =>
    request<import('../types').PlanStatus>(`/plan/${requestId}`),

  submitAssessment: (data: {
    request_id: string
    answers: { question_id: string; answer: string | number }[]
  }) => request<{ request_id: string; status: string }>('/assessment/answer', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  reviewPlan: (requestId: string, data: {
    status: 'approved' | 'changes_requested'
    comments: string
    requested_changes: string[]
  }) => request<{ request_id: string; status: string }>(`/plan/${requestId}/review`, {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  getDashboard: (employeeId: string) =>
    request<{ employee_id: string; employee_name: string; plans: any[] }>(
      `/dashboard/${employeeId}`
    ),

  getRequests: () =>
    request<import('../types').RequestSummary[]>('/requests'),

  generateCourse: (requestId: string, moduleId: string) =>
    request<{ status: string; module_id: string }>(`/plan/${requestId}/generate-course/${moduleId}`, {
      method: 'POST',
    }),

  approveRequest: (requestId: string) =>
    request<{ request_id: string; status: string }>(`/plan/${requestId}/approve-request`, {
      method: 'POST',
    }),

  rejectRequest: (requestId: string) =>
    request<{ request_id: string; status: string }>(`/plan/${requestId}/reject-request`, {
      method: 'POST',
    }),

  getEmployees: () =>
    request<{
      employee_id: string
      name: string
      current_role: string
      department: string
      plans_count: number
      active_plan_phase: string | null
    }[]>('/employees'),

  getEmployee: (employeeId: string) =>
    request<{
      employee_id: string
      name: string
      current_role: string
      department: string
      hr_notes: string
      plans: any[]
    }>(`/employee/${employeeId}`),
}

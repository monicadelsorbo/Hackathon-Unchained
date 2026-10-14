import { useState, useCallback } from 'react'
import { useParams, useNavigate, Navigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import { useRole } from '../hooks/useRole'
import RoadmapTimeline from '../components/RoadmapTimeline'
import CostBreakdown from '../components/CostBreakdown'
import MentorProfile from '../components/MentorProfile'
import SkillRadar from '../components/SkillRadar'

export default function ReviewPage() {
  const { user } = useRole()

  // Solo i manager possono accedere alla review
  if (user.role !== 'manager') {
    return <Navigate to="/dashboard" replace />
  }
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const [showChangesForm, setShowChangesForm] = useState(false)
  const [comments, setComments] = useState('')
  const [changes, setChanges] = useState('')

  const fetchPlan = useCallback(() => api.getPlan(id!), [id])
  const { data: plan, loading } = usePolling(fetchPlan, 5000, !!id)

  async function handleApprove() {
    setSubmitting(true)
    try {
      await api.reviewPlan(id!, {
        status: 'approved',
        comments: 'Piano approvato.',
        requested_changes: [],
      })
      navigate(`/request/${id}`)
    } catch (err: any) {
      alert(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleRequestChanges() {
    if (!comments.trim()) return
    setSubmitting(true)
    try {
      await api.reviewPlan(id!, {
        status: 'changes_requested',
        comments,
        requested_changes: changes
          .split('\n')
          .map((l) => l.trim())
          .filter(Boolean),
      })
      navigate(`/request/${id}`)
    } catch (err: any) {
      alert(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading && !plan) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
      </div>
    )
  }

  if (!plan) return null

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        Revisione Piano: {plan.employee_name}
      </h1>
      <p className="text-gray-500 mb-8">
        {plan.current_role} &rarr; {plan.target_position}
      </p>

      {/* Plan summary */}
      {plan.plan_summary && (
        <div className="card mb-6">
          <p className="text-gray-700">{plan.plan_summary}</p>
        </div>
      )}

      {/* Plan content */}
      <div className="grid lg:grid-cols-3 gap-8 mb-8">
        <div className="lg:col-span-2">
          {plan.training_plan && (
            <RoadmapTimeline
              modules={plan.training_plan}
              requestId={plan.request_id}
              customCourses={plan.custom_courses}
            />
          )}
        </div>
        <div className="space-y-6">
          {plan.skill_gaps && <SkillRadar gaps={plan.skill_gaps} />}
          {plan.cost_breakdown && <CostBreakdown cost={plan.cost_breakdown} />}
          {plan.assigned_mentor && <MentorProfile mentor={plan.assigned_mentor} />}
        </div>
      </div>

      {/* Review actions */}
      {plan.current_phase === 'pending_review' && (
        <div className="card border-2 border-purple-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Decisione</h3>

          {!showChangesForm ? (
            <div className="flex gap-4">
              <button
                onClick={handleApprove}
                disabled={submitting}
                className="btn-primary flex-1"
              >
                {submitting ? 'Invio...' : 'Approva Piano'}
              </button>
              <button
                onClick={() => setShowChangesForm(true)}
                className="btn-danger flex-1"
              >
                Richiedi Modifiche
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Commenti
                </label>
                <textarea
                  value={comments}
                  onChange={(e) => setComments(e.target.value)}
                  placeholder="Spiega cosa deve essere modificato..."
                  className="input-field h-24 resize-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Modifiche richieste (una per riga)
                </label>
                <textarea
                  value={changes}
                  onChange={(e) => setChanges(e.target.value)}
                  placeholder={"Aggiungere un modulo su leadership\nRidurre la durata totale a 12 settimane"}
                  className="input-field h-24 resize-none"
                />
              </div>
              <div className="flex gap-3">
                <button
                  onClick={handleRequestChanges}
                  disabled={submitting || !comments.trim()}
                  className="btn-danger flex-1"
                >
                  {submitting ? 'Invio...' : 'Invia Modifiche'}
                </button>
                <button
                  onClick={() => setShowChangesForm(false)}
                  className="btn-secondary"
                >
                  Annulla
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

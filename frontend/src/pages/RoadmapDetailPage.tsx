import { useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import RoadmapTimeline from '../components/RoadmapTimeline'
import CostBreakdown from '../components/CostBreakdown'
import MentorProfile from '../components/MentorProfile'
import SkillRadar from '../components/SkillRadar'

export default function RoadmapDetailPage() {
  const { id } = useParams<{ id: string }>()
  const fetchPlan = useCallback(() => api.getPlan(id!), [id])
  const { data: plan, loading } = usePolling(fetchPlan, 5000, !!id)

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
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <Link to={`/request/${id}`} className="text-sm text-brand-600 hover:underline mb-2 inline-block">
            &larr; Torna alla richiesta
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">
            Roadmap: {plan.employee_name}
          </h1>
          <p className="text-gray-500 mt-1">
            {plan.current_role} &rarr; {plan.target_position}
          </p>
        </div>
        {plan.review_status === 'approved' && (
          <span className="badge bg-green-100 text-green-700 text-sm px-3 py-1">
            Approvato
          </span>
        )}
      </div>

      {/* Plan summary */}
      {plan.plan_summary && (
        <div className="card mb-8">
          <p className="text-gray-700">{plan.plan_summary}</p>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Main: Timeline with inline course generation */}
        <div className="lg:col-span-2 space-y-10">
          {plan.training_plan && plan.training_plan.length > 0 ? (
            <RoadmapTimeline
              modules={plan.training_plan}
              requestId={plan.request_id}
              customCourses={plan.custom_courses}
            />
          ) : (
            <div className="card text-center py-8 text-gray-500">
              Piano non ancora generato.
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {plan.skill_gaps && plan.skill_gaps.length > 0 && (
            <SkillRadar gaps={plan.skill_gaps} />
          )}

          {plan.cost_breakdown && (
            <CostBreakdown cost={plan.cost_breakdown} />
          )}

          {plan.assigned_mentor && (
            <MentorProfile mentor={plan.assigned_mentor} />
          )}
        </div>
      </div>
    </div>
  )
}

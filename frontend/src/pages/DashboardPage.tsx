import { useCallback } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import { useRole } from '../hooks/useRole'

export default function DashboardPage() {
  const { user } = useRole()

  // Solo i dipendenti vedono la propria dashboard
  if (user.role === 'manager') {
    return <Navigate to="/requests" replace />
  }

  const fetchDashboard = useCallback(
    () => api.getDashboard(user.id),
    [user.id]
  )
  const { data: dashboard, loading } = usePolling(fetchDashboard, 5000)

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Le mie Roadmap</h1>
      <p className="text-gray-500 mb-8">I tuoi piani di formazione personalizzati, {user.name}.</p>

      {loading && !dashboard && (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
        </div>
      )}

      {dashboard && (
        <div>
          {dashboard.plans.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-gray-500 mb-4">Non hai ancora piani formativi.</p>
              <Link to="/request" className="btn-primary">
                Richiedi un Piano
              </Link>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2">
              {dashboard.plans.map((plan: any) => (
                <div key={plan.request_id} className="card hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-semibold text-gray-900">{plan.target_position}</h3>
                    <span
                      className={`badge ${
                        plan.current_phase === 'complete'
                          ? 'bg-green-100 text-green-700'
                          : plan.current_phase === 'pending_review'
                          ? 'bg-purple-100 text-purple-700'
                          : 'bg-yellow-100 text-yellow-700'
                      }`}
                    >
                      {plan.current_phase === 'complete'
                        ? 'Approvato'
                        : plan.current_phase === 'pending_review'
                        ? 'In revisione'
                        : plan.current_phase}
                    </span>
                  </div>
                  {plan.plan_summary && (
                    <p className="text-sm text-gray-600 mb-3">{plan.plan_summary}</p>
                  )}
                  {plan.cost_breakdown && (
                    <div className="flex gap-4 text-xs text-gray-500 mb-4">
                      <span>&euro;{plan.cost_breakdown.total_course_cost_eur?.toFixed(0)}</span>
                      <span>{plan.cost_breakdown.total_hours?.toFixed(0)}h</span>
                      <span>{plan.cost_breakdown.estimated_duration_weeks} sett.</span>
                    </div>
                  )}
                  {plan.current_phase === 'complete' ? (
                    <Link
                      to={`/roadmap/${plan.request_id}`}
                      className="text-sm text-brand-600 hover:text-brand-700 font-medium"
                    >
                      Vedi Roadmap &rarr;
                    </Link>
                  ) : (
                    <Link
                      to={`/request/${plan.request_id}`}
                      className="text-sm text-gray-500 hover:text-gray-700 font-medium"
                    >
                      Segui stato &rarr;
                    </Link>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

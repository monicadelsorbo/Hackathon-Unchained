import { useCallback } from 'react'
import { useParams, Link, Navigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import { useRole } from '../hooks/useRole'

const phaseLabels: Record<string, string> = {
  pending_approval: 'Da Approvare',
  rejected: 'Rifiutata',
  initializing: 'Inizializzazione',
  profiling: 'Profiling',
  awaiting_assessment: 'Assessment',
  planning: 'Pianificazione',
  pending_review: 'In Revisione',
  reviewing: 'Revisione',
  complete: 'Completato',
  error: 'Errore',
}

const phaseColors: Record<string, string> = {
  pending_approval: 'bg-amber-100 text-amber-700',
  rejected: 'bg-red-100 text-red-700',
  initializing: 'bg-gray-100 text-gray-700',
  profiling: 'bg-blue-100 text-blue-700',
  awaiting_assessment: 'bg-yellow-100 text-yellow-700',
  planning: 'bg-blue-100 text-blue-700',
  pending_review: 'bg-purple-100 text-purple-700',
  reviewing: 'bg-purple-100 text-purple-700',
  complete: 'bg-green-100 text-green-700',
  error: 'bg-red-100 text-red-700',
}

export default function EmployeeProfilePage() {
  const { employeeId } = useParams<{ employeeId: string }>()
  const { user } = useRole()
  const isManager = user.role === 'manager'

  // Il dipendente puo' vedere solo il proprio profilo
  if (!isManager && user.id !== employeeId) {
    return <Navigate to="/dashboard" replace />
  }

  const fetchEmployee = useCallback(() => api.getEmployee(employeeId!), [employeeId])
  const { data: profile, loading } = usePolling(fetchEmployee, 10000, !!employeeId)

  if (loading && !profile) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
      </div>
    )
  }

  if (!profile) return null

  // Prendi skills dal piano piu' recente che le ha
  const latestWithSkills = profile.plans.find((p: any) => p.hard_skills || p.soft_skills)

  return (
    <div className="max-w-4xl mx-auto">
      {/* Back link */}
      {isManager && (
        <Link to="/employees" className="text-sm text-brand-600 hover:underline mb-4 inline-block">
          &larr; Tutti i dipendenti
        </Link>
      )}

      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 bg-brand-100 rounded-full flex items-center justify-center text-brand-700 font-bold text-lg">
            {profile.name.split(' ').map((n: string) => n[0]).join('')}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{profile.name}</h1>
            <p className="text-gray-500">{profile.current_role}</p>
            {profile.department && (
              <span className="badge bg-gray-100 text-gray-600 mt-1">{profile.department}</span>
            )}
          </div>
        </div>

        {/* HR Notes - solo per manager */}
        {isManager && profile.hr_notes && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
            <h3 className="text-sm font-semibold text-blue-800 mb-1">Note HR</h3>
            <p className="text-sm text-blue-700">{profile.hr_notes}</p>
          </div>
        )}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Colonna principale: Piani */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-lg font-semibold text-gray-900">
            Piani Formativi ({profile.plans.length})
          </h2>

          {profile.plans.length === 0 ? (
            <div className="card text-center py-8 text-gray-500">
              <p className="mb-3">Nessun piano formativo attivo.</p>
              {isManager && (
                <Link to="/request" className="btn-primary text-sm">
                  Crea Piano
                </Link>
              )}
            </div>
          ) : (
            profile.plans.map((plan: any) => (
              <div key={plan.request_id} className="card">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-gray-900">{plan.target_position}</h3>
                    {plan.plan_summary && (
                      <p className="text-sm text-gray-500 mt-1 line-clamp-2">{plan.plan_summary}</p>
                    )}
                  </div>
                  <span className={`badge ${phaseColors[plan.current_phase] || 'bg-gray-100 text-gray-700'}`}>
                    {phaseLabels[plan.current_phase] || plan.current_phase}
                  </span>
                </div>

                {/* Stats */}
                {plan.cost_breakdown && (
                  <div className="flex gap-4 text-xs text-gray-500 mb-3 border-t border-gray-100 pt-3">
                    <span>Costo: &euro;{plan.cost_breakdown.total_course_cost_eur?.toFixed(0)}</span>
                    <span>Ore: {plan.cost_breakdown.total_hours?.toFixed(0)}h</span>
                    <span>Durata: {plan.cost_breakdown.estimated_duration_weeks} settimane</span>
                  </div>
                )}

                {/* Skill gaps */}
                {plan.skill_gaps && plan.skill_gaps.length > 0 && (
                  <div className="mb-3">
                    <p className="text-xs font-medium text-gray-500 mb-1.5">Gap Competenze</p>
                    <div className="flex flex-wrap gap-1">
                      {plan.skill_gaps.map((g: any) => (
                        <span
                          key={g.skill}
                          className={`badge text-xs ${
                            g.priority === 'high'
                              ? 'bg-red-100 text-red-700'
                              : g.priority === 'medium'
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-green-100 text-green-700'
                          }`}
                        >
                          {g.skill} ({g.current_level}&rarr;{g.target_level})
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Mentor */}
                {plan.assigned_mentor && (
                  <div className="text-xs text-gray-500 mb-3">
                    Mentor: <span className="font-medium text-gray-700">{plan.assigned_mentor.name}</span>
                    {' '}&mdash; {plan.assigned_mentor.role}
                  </div>
                )}

                {/* Training modules count */}
                {plan.training_plan && (
                  <div className="text-xs text-gray-500 mb-3">
                    {plan.training_plan.length} moduli formativi
                    {plan.custom_courses && plan.custom_courses.length > 0 && (
                      <> &middot; {plan.custom_courses.length} corsi AI generati</>
                    )}
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-3 border-t border-gray-100 pt-3">
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
                  {isManager && plan.current_phase === 'pending_review' && (
                    <Link
                      to={`/review/${plan.request_id}`}
                      className="text-sm text-purple-600 hover:text-purple-700 font-medium"
                    >
                      Revisiona &rarr;
                    </Link>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Sidebar: Competenze */}
        <div className="space-y-6">
          {latestWithSkills?.hard_skills && latestWithSkills.hard_skills.length > 0 && (
            <div className="card">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Hard Skills</h3>
              <div className="space-y-2">
                {latestWithSkills.hard_skills.map((s: any) => (
                  <div key={s.skill}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-700">{s.skill}</span>
                      <span className="text-gray-500">{s.level}/5</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5">
                      <div
                        className="bg-blue-500 h-1.5 rounded-full"
                        style={{ width: `${(s.level / 5) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {latestWithSkills?.soft_skills && latestWithSkills.soft_skills.length > 0 && (
            <div className="card">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Soft Skills</h3>
              <div className="space-y-2">
                {latestWithSkills.soft_skills.map((s: any) => (
                  <div key={s.skill}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-700">{s.skill}</span>
                      <span className="text-gray-500">{s.level}/5</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5">
                      <div
                        className="bg-orange-400 h-1.5 rounded-full"
                        style={{ width: `${(s.level / 5) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {latestWithSkills?.experience_summary && (
            <div className="card">
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Esperienza</h3>
              <p className="text-sm text-gray-600">{latestWithSkills.experience_summary}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

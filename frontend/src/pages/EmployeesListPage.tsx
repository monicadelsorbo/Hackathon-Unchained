import { useCallback } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import { useRole } from '../hooks/useRole'

const phaseLabels: Record<string, string> = {
  pending_approval: 'Da Approvare',
  initializing: 'Inizializzazione',
  profiling: 'Profiling',
  awaiting_assessment: 'Assessment',
  planning: 'Pianificazione',
  pending_review: 'In Revisione',
  complete: 'Completato',
}

const phaseColors: Record<string, string> = {
  pending_approval: 'bg-amber-100 text-amber-700',
  initializing: 'bg-gray-100 text-gray-700',
  profiling: 'bg-blue-100 text-blue-700',
  awaiting_assessment: 'bg-yellow-100 text-yellow-700',
  planning: 'bg-blue-100 text-blue-700',
  pending_review: 'bg-purple-100 text-purple-700',
  complete: 'bg-green-100 text-green-700',
}

export default function EmployeesListPage() {
  const { user } = useRole()

  if (user.role !== 'manager') {
    return <Navigate to="/dashboard" replace />
  }

  const fetchEmployees = useCallback(() => api.getEmployees(), [])
  const { data: employees, loading } = usePolling(fetchEmployees, 10000)

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Dipendenti</h1>
      <p className="text-gray-500 mb-8">Panoramica di tutti i dipendenti e i loro piani formativi.</p>

      {loading && !employees && (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
        </div>
      )}

      {employees && employees.length > 0 && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {employees.map((emp) => (
            <Link
              key={emp.employee_id}
              to={`/employee/${emp.employee_id}`}
              className="card hover:shadow-md transition-shadow group"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-brand-100 rounded-full flex items-center justify-center text-brand-700 font-semibold text-sm">
                  {emp.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 group-hover:text-brand-600 transition-colors">
                    {emp.name}
                  </h3>
                  <p className="text-xs text-gray-500">{emp.current_role}</p>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">
                  {emp.department}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-gray-400 text-xs">
                    {emp.plans_count} {emp.plans_count === 1 ? 'piano' : 'piani'}
                  </span>
                  {emp.active_plan_phase && (
                    <span className={`badge text-xs ${phaseColors[emp.active_plan_phase] || 'bg-gray-100 text-gray-700'}`}>
                      {phaseLabels[emp.active_plan_phase] || emp.active_plan_phase}
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {employees && employees.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-500">Nessun dipendente trovato.</p>
        </div>
      )}
    </div>
  )
}

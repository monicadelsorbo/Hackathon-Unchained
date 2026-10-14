import { useCallback } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'

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

export default function RequestsListPage() {
  const fetchRequests = useCallback(() => api.getRequests(), [])
  const { data: requests, loading } = usePolling(fetchRequests, 5000)

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Richieste</h1>
        <Link to="/request" className="btn-primary">
          Nuova Richiesta
        </Link>
      </div>

      {loading && !requests && (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
        </div>
      )}

      {requests && requests.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-500 mb-4">Nessuna richiesta trovata.</p>
          <Link to="/request" className="btn-primary">
            Crea la prima richiesta
          </Link>
        </div>
      )}

      {requests && requests.length > 0 && (
        <div className="card overflow-hidden p-0">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Dipendente
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Posizione Target
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Tipo
                </th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase">
                  Stato
                </th>
                <th className="px-6 py-3" />
              </tr>
            </thead>
            <tbody>
              {requests.map((req) => (
                <tr key={req.request_id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <p className="text-sm font-medium text-gray-900">
                      {req.employee_name || req.employee_id}
                    </p>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {req.target_position}
                  </td>
                  <td className="px-6 py-4">
                    <span className="badge bg-gray-100 text-gray-600">
                      {req.requester_type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`badge ${phaseColors[req.current_phase] || 'bg-gray-100 text-gray-700'}`}>
                      {phaseLabels[req.current_phase] || req.current_phase}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      to={`/request/${req.request_id}`}
                      className="text-sm text-brand-600 hover:text-brand-700 font-medium"
                    >
                      Dettagli
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

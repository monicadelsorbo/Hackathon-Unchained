import { useCallback, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import { useRole } from '../hooks/useRole'
import AgentStatusTracker from '../components/AgentStatusTracker'

const phaseLabels: Record<string, string> = {
  pending_approval: 'In attesa di Approvazione',
  rejected: 'Rifiutata',
  initializing: 'Inizializzazione...',
  profiling: 'Analisi Profilo',
  awaiting_assessment: 'In attesa dell\'Assessment',
  planning: 'Generazione Piano',
  pending_review: 'In attesa di Revisione',
  reviewing: 'Revisione in corso',
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

export default function RequestStatusPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useRole()
  const isManager = user.role === 'manager'
  const [approving, setApproving] = useState(false)

  const fetchPlan = useCallback(() => api.getPlan(id!), [id])
  const { data: plan, loading, error } = usePolling(fetchPlan, 2000, !!id)

  if (loading && !plan) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
      </div>
    )
  }

  if (error) {
    return <div className="text-red-600">Errore: {error}</div>
  }

  if (!plan) return null

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {plan.employee_name || 'Dipendente'}
          </h1>
          <p className="text-gray-500 mt-1">
            Target: <span className="font-medium text-gray-700">{plan.target_position}</span>
          </p>
        </div>
        <span className={`badge text-sm px-3 py-1 ${phaseColors[plan.current_phase] || 'bg-gray-100 text-gray-700'}`}>
          {phaseLabels[plan.current_phase] || plan.current_phase}
        </span>
      </div>

      {/* Agent Status */}
      <AgentStatusTracker statuses={plan.agent_statuses} />

      {/* Actions based on phase AND role */}
      <div className="mt-6 space-y-4">
        {plan.current_phase === 'pending_approval' && (
          <div className="card bg-amber-50 border-amber-200">
            <h3 className="font-semibold text-amber-800 mb-2">
              {isManager ? 'Richiesta da Approvare' : 'In attesa di approvazione'}
            </h3>
            {isManager ? (
              <>
                <p className="text-sm text-amber-700 mb-4">
                  Il dipendente ha richiesto la generazione di un piano formativo
                  per la posizione di <span className="font-semibold">{plan.target_position}</span>.
                  Approva per avviare l'analisi del profilo e la generazione del piano.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={async () => {
                      setApproving(true)
                      try {
                        await api.approveRequest(id!)
                      } catch (err: any) {
                        alert(err.message)
                      } finally {
                        setApproving(false)
                      }
                    }}
                    disabled={approving}
                    className="btn-primary flex-1"
                  >
                    {approving ? 'Approvazione...' : 'Approva Richiesta'}
                  </button>
                  <button
                    onClick={async () => {
                      setApproving(true)
                      try {
                        await api.rejectRequest(id!)
                      } catch (err: any) {
                        alert(err.message)
                      } finally {
                        setApproving(false)
                      }
                    }}
                    disabled={approving}
                    className="btn-danger flex-1"
                  >
                    Rifiuta
                  </button>
                </div>
              </>
            ) : (
              <p className="text-sm text-amber-700">
                La tua richiesta e' stata inviata al manager. Riceverai una notifica quando sara' approvata.
              </p>
            )}
          </div>
        )}

        {plan.current_phase === 'rejected' && (
          <div className="card bg-red-50 border-red-200">
            <h3 className="font-semibold text-red-800 mb-2">Richiesta Rifiutata</h3>
            <p className="text-sm text-red-700">
              {isManager
                ? 'Hai rifiutato questa richiesta di piano formativo.'
                : 'La tua richiesta di piano formativo e\' stata rifiutata dal manager.'}
            </p>
          </div>
        )}

        {plan.current_phase === 'awaiting_assessment' && (
          <div className="card bg-yellow-50 border-yellow-200">
            <h3 className="font-semibold text-yellow-800 mb-2">Assessment Pronto</h3>
            {!isManager ? (
              <>
                <p className="text-sm text-yellow-700 mb-4">
                  L'assessment personalizzato con {plan.assessment_questions?.length || 0} domande
                  &egrave; pronto. Completa l'assessment per procedere.
                </p>
                <button
                  onClick={() => navigate(`/assessment/${id}`)}
                  className="btn-primary"
                >
                  Inizia Assessment
                </button>
              </>
            ) : (
              <p className="text-sm text-yellow-700">
                In attesa che il dipendente completi l'assessment
                ({plan.assessment_questions?.length || 0} domande).
              </p>
            )}
          </div>
        )}

        {plan.current_phase === 'pending_review' && (
          <div className="card bg-purple-50 border-purple-200">
            <h3 className="font-semibold text-purple-800 mb-2">
              {isManager ? 'Piano Pronto per la Revisione' : 'In attesa di approvazione'}
            </h3>
            {isManager ? (
              <>
                <p className="text-sm text-purple-700 mb-4">
                  Il piano formativo &egrave; stato generato. Revisiona e approva il piano.
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => navigate(`/roadmap/${id}`)}
                    className="btn-secondary"
                  >
                    Vedi Roadmap
                  </button>
                  <button
                    onClick={() => navigate(`/review/${id}`)}
                    className="btn-primary"
                  >
                    Revisiona Piano
                  </button>
                </div>
              </>
            ) : (
              <>
                <p className="text-sm text-purple-700 mb-4">
                  Il piano &egrave; stato generato ed &egrave; in attesa di approvazione da parte del manager.
                  Puoi visualizzare l'anteprima della roadmap.
                </p>
                <button
                  onClick={() => navigate(`/roadmap/${id}`)}
                  className="btn-secondary"
                >
                  Vedi Anteprima Roadmap
                </button>
              </>
            )}
          </div>
        )}

        {plan.current_phase === 'complete' && (
          <div className="card bg-green-50 border-green-200">
            <h3 className="font-semibold text-green-800 mb-2">Piano Approvato!</h3>
            <p className="text-sm text-green-700 mb-4">
              {isManager
                ? 'Il piano formativo &egrave; stato approvato ed inviato al dipendente.'
                : 'Il tuo piano formativo &egrave; stato approvato! Puoi iniziare il percorso.'}
            </p>
            <button
              onClick={() => navigate(`/roadmap/${id}`)}
              className="btn-primary"
            >
              Vedi Roadmap Completa
            </button>
          </div>
        )}

        {plan.current_phase === 'error' && (
          <div className="card bg-red-50 border-red-200">
            <h3 className="font-semibold text-red-800">Errore</h3>
            <p className="text-sm text-red-700">
              Si &egrave; verificato un errore durante l'elaborazione.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

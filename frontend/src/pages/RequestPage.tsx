import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useRole } from '../hooks/useRole'

const employees = [
  { id: 'emp-001', name: 'Marco Bianchi', role: 'Junior Software Developer' },
  { id: 'emp-002', name: 'Giulia Rossi', role: 'Mid-Level UX Designer' },
  { id: 'emp-003', name: 'Alessandro Ferretti', role: 'Senior Backend Developer' },
]

const targetPositions = ['Senior Software Developer', 'UX Lead', 'Solutions Architect']

export default function RequestPage() {
  const navigate = useNavigate()
  const { user } = useRole()
  const isManager = user.role === 'manager'
  const [loading, setLoading] = useState(false)

  const [form, setForm] = useState({
    employee_id: isManager ? '' : user.id,
    target_position: '',
    request_reason: '',
  })

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await api.requestPlan({
        requester_type: user.role,
        requester_id: user.id,
        employee_id: form.employee_id,
        target_position: form.target_position,
        request_reason: form.request_reason,
      })
      navigate(`/request/${res.request_id}`)
    } catch (err: any) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        {isManager ? 'Richiedi Piano per un Dipendente' : 'Richiedi il tuo Piano Formativo'}
      </h1>
      <p className="text-gray-500 mb-8">
        {isManager
          ? 'Seleziona un dipendente e la posizione target per generare un piano personalizzato.'
          : 'Scegli la posizione target per generare il tuo percorso di crescita.'}
      </p>

      <form onSubmit={handleSubmit} className="card space-y-6">
        {/* Employee select - solo per manager */}
        {isManager ? (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dipendente
            </label>
            <select
              value={form.employee_id}
              onChange={(e) => setForm((f) => ({ ...f, employee_id: e.target.value }))}
              className="input-field"
              required
            >
              <option value="">Seleziona dipendente...</option>
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.name} — {emp.role}
                </option>
              ))}
            </select>
          </div>
        ) : (
          <div className="bg-brand-50 border border-brand-200 rounded-lg p-4">
            <p className="text-sm text-brand-700">
              Richiesta per: <span className="font-semibold">{user.name}</span>
            </p>
          </div>
        )}

        {/* Target position */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Posizione Target
          </label>
          <select
            value={form.target_position}
            onChange={(e) => setForm((f) => ({ ...f, target_position: e.target.value }))}
            className="input-field"
            required
          >
            <option value="">Seleziona posizione...</option>
            {targetPositions.map((pos) => (
              <option key={pos} value={pos}>
                {pos}
              </option>
            ))}
          </select>
        </div>

        {/* Reason */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Motivazione
          </label>
          <textarea
            value={form.request_reason}
            onChange={(e) => setForm((f) => ({ ...f, request_reason: e.target.value }))}
            placeholder={isManager
              ? 'Descrivi il motivo della richiesta per questo dipendente...'
              : 'Descrivi le tue motivazioni e obiettivi di crescita...'}
            className="input-field h-24 resize-none"
            required
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? 'Avvio in corso...' : 'Avvia Generazione Piano'}
        </button>
      </form>
    </div>
  )
}

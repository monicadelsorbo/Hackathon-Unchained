import { useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { usePolling } from '../hooks/usePolling'
import AssessmentWizard from '../components/AssessmentWizard'

export default function AssessmentPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)

  const fetchPlan = useCallback(() => api.getPlan(id!), [id])
  const { data: plan, loading } = usePolling(fetchPlan, 5000, !!id)

  if (loading && !plan) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600" />
      </div>
    )
  }

  if (!plan?.assessment_questions || plan.assessment_questions.length === 0) {
    return (
      <div className="max-w-2xl mx-auto card text-center py-12">
        <p className="text-gray-500">Assessment non ancora disponibile.</p>
      </div>
    )
  }

  async function handleSubmit(answers: { question_id: string; answer: string | number }[]) {
    setSubmitting(true)
    try {
      await api.submitAssessment({ request_id: id!, answers })
      navigate(`/request/${id}`)
    } catch (err: any) {
      alert(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Assessment Personalizzato</h1>
        <p className="text-gray-500 mt-1">
          {plan.employee_name} &mdash; Target: {plan.target_position}
        </p>
      </div>

      <AssessmentWizard
        questions={plan.assessment_questions}
        onSubmit={handleSubmit}
        submitting={submitting}
      />
    </div>
  )
}

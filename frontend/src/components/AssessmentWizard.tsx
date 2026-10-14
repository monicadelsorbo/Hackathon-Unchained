import { useState } from 'react'
import type { AssessmentQuestion } from '../types'

interface Props {
  questions: AssessmentQuestion[]
  onSubmit: (answers: { question_id: string; answer: string | number }[]) => void
  submitting?: boolean
}

export default function AssessmentWizard({ questions, onSubmit, submitting }: Props) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string | number>>({})

  const question = questions[currentIndex]
  const progress = ((currentIndex + 1) / questions.length) * 100
  const isLast = currentIndex === questions.length - 1
  const hasAnswer = answers[question?.question_id] !== undefined && answers[question?.question_id] !== ''

  function setAnswer(value: string | number) {
    setAnswers((prev) => ({ ...prev, [question.question_id]: value }))
  }

  function handleNext() {
    if (isLast) {
      const formatted = Object.entries(answers).map(([question_id, answer]) => ({
        question_id,
        answer,
      }))
      onSubmit(formatted)
    } else {
      setCurrentIndex((i) => i + 1)
    }
  }

  if (!question) return null

  const categoryColors: Record<string, string> = {
    technical: 'bg-blue-100 text-blue-700',
    situational: 'bg-orange-100 text-orange-700',
    interest: 'bg-green-100 text-green-700',
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-500 mb-2">
          <span>Domanda {currentIndex + 1} di {questions.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-brand-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question card */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <span className={`badge ${categoryColors[question.category] || 'bg-gray-100 text-gray-600'}`}>
            {question.category}
          </span>
          <span className="badge bg-gray-100 text-gray-600">{question.skill_area}</span>
        </div>

        <h3 className="text-lg font-semibold text-gray-900 mb-6">
          {question.question_text}
        </h3>

        {/* Answer input based on question type */}
        {question.question_type === 'multiple_choice' && (
          <div className="space-y-3">
            {question.options.map((option, i) => (
              <button
                key={i}
                onClick={() => setAnswer(option)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                  answers[question.question_id] === option
                    ? 'border-brand-500 bg-brand-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <span className="text-sm">{option}</span>
              </button>
            ))}
          </div>
        )}

        {question.question_type === 'scale' && (
          <div className="flex gap-3 justify-center">
            {[1, 2, 3, 4, 5].map((val) => (
              <button
                key={val}
                onClick={() => setAnswer(val)}
                className={`w-14 h-14 rounded-full text-lg font-semibold transition-all ${
                  answers[question.question_id] === val
                    ? 'bg-brand-500 text-white shadow-lg scale-110'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {val}
              </button>
            ))}
          </div>
        )}

        {question.question_type === 'open' && (
          <textarea
            value={(answers[question.question_id] as string) || ''}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Scrivi la tua risposta..."
            className="input-field h-32 resize-none"
          />
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
          disabled={currentIndex === 0}
          className="btn-secondary disabled:opacity-30"
        >
          Indietro
        </button>
        <button
          onClick={handleNext}
          disabled={!hasAnswer || submitting}
          className="btn-primary"
        >
          {submitting ? 'Invio in corso...' : isLast ? 'Completa Assessment' : 'Avanti'}
        </button>
      </div>
    </div>
  )
}

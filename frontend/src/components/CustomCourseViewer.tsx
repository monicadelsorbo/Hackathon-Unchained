import { useState } from 'react'
import type { CustomCourse, LessonContent, QuizQuestion } from '../types'

// ── Quiz Component ────────────────────────────────────────────────────────

function QuizCard({ question, onAnswer }: { question: QuizQuestion; onAnswer: (correct: boolean) => void }) {
  const [selected, setSelected] = useState<number | null>(null)
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit() {
    if (selected === null) return
    setSubmitted(true)
    onAnswer(selected === question.correct_answer)
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <p className="text-sm font-medium text-gray-800 mb-3">{question.question_text}</p>
      <div className="space-y-2 mb-3">
        {question.options.map((opt, i) => {
          let classes = 'w-full text-left p-3 rounded-lg border text-sm transition-all '
          if (!submitted) {
            classes += selected === i
              ? 'border-brand-500 bg-brand-50'
              : 'border-gray-200 hover:border-gray-300'
          } else if (i === question.correct_answer) {
            classes += 'border-green-500 bg-green-50 text-green-800'
          } else if (i === selected) {
            classes += 'border-red-500 bg-red-50 text-red-800'
          } else {
            classes += 'border-gray-200 opacity-50'
          }

          return (
            <button
              key={i}
              onClick={() => !submitted && setSelected(i)}
              disabled={submitted}
              className={classes}
            >
              {opt}
            </button>
          )
        })}
      </div>
      {!submitted ? (
        <button
          onClick={handleSubmit}
          disabled={selected === null}
          className="btn-primary text-sm py-2"
        >
          Verifica
        </button>
      ) : (
        <div className={`p-3 rounded-lg text-sm ${
          selected === question.correct_answer
            ? 'bg-green-50 border border-green-200 text-green-800'
            : 'bg-red-50 border border-red-200 text-red-800'
        }`}>
          <p className="font-medium mb-1">
            {selected === question.correct_answer ? 'Corretto!' : 'Sbagliato'}
          </p>
          <p>{question.explanation}</p>
        </div>
      )}
    </div>
  )
}

// ── Lesson Component ──────────────────────────────────────────────────────

function LessonViewer({ lesson, index }: { lesson: LessonContent; index: number }) {
  const [expanded, setExpanded] = useState(index === 0)
  const [quizResults, setQuizResults] = useState<boolean[]>([])

  function handleQuizAnswer(correct: boolean) {
    setQuizResults((prev) => [...prev, correct])
  }

  const quizComplete = quizResults.length === lesson.quiz.length
  const quizScore = quizResults.filter(Boolean).length

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden">
      {/* Lesson header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <span className="w-8 h-8 bg-brand-500 text-white rounded-full flex items-center justify-center text-sm font-semibold">
            {index + 1}
          </span>
          <h4 className="font-medium text-gray-900">{lesson.title}</h4>
        </div>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${expanded ? 'rotate-180' : ''}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {expanded && (
        <div className="p-4 space-y-6">
          {/* Content */}
          <div className="prose prose-sm max-w-none">
            <div
              className="text-gray-700 leading-relaxed whitespace-pre-line"
              dangerouslySetInnerHTML={{ __html: renderMarkdown(lesson.content_markdown) }}
            />
          </div>

          {/* YouTube Videos */}
          {lesson.youtube_videos && lesson.youtube_videos.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-red-500">&#9654;</span> Video Consigliati
              </h5>
              <div className="grid gap-4 sm:grid-cols-2">
                {lesson.youtube_videos.map((video) => (
                  <div key={video.video_id} className="border border-gray-200 rounded-lg overflow-hidden">
                    {video.video_id !== 'placeholder' ? (
                      <div className="aspect-video">
                        <iframe
                          className="w-full h-full"
                          src={`https://www.youtube.com/embed/${video.video_id}`}
                          title={video.title}
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                        />
                      </div>
                    ) : (
                      <div className="aspect-video bg-gray-100 flex items-center justify-center text-gray-400">
                        Video non disponibile
                      </div>
                    )}
                    <div className="p-3">
                      <p className="text-sm font-medium text-gray-800">{video.title}</p>
                      <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                        <span>{video.channel}</span>
                        <span>{video.duration_minutes} min</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1 italic">{video.relevance_note}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quiz */}
          {lesson.quiz && lesson.quiz.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span>&#9997;&#65039;</span> Quiz di Verifica
              </h5>
              {quizComplete && (
                <div className={`mb-4 p-3 rounded-lg text-sm font-medium ${
                  quizScore === lesson.quiz.length
                    ? 'bg-green-50 border border-green-200 text-green-800'
                    : quizScore >= lesson.quiz.length / 2
                    ? 'bg-yellow-50 border border-yellow-200 text-yellow-800'
                    : 'bg-red-50 border border-red-200 text-red-800'
                }`}>
                  Risultato: {quizScore}/{lesson.quiz.length} risposte corrette
                  {quizScore === lesson.quiz.length && ' — Eccellente!'}
                </div>
              )}
              <div className="space-y-4">
                {lesson.quiz.map((q) => (
                  <QuizCard key={q.quiz_id} question={q} onAnswer={handleQuizAnswer} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Main Component ────────────────────────────────────────────────────────

interface Props {
  courses: CustomCourse[]
}

export default function CustomCourseViewer({ courses }: Props) {
  if (!courses || courses.length === 0) return null

  return (
    <div className="space-y-8">
      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
        <span>&#127891;</span> Corsi Personalizzati
      </h3>
      {courses.map((course) => (
        <div key={course.custom_course_id} className="card">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h4 className="font-semibold text-gray-900">{course.title}</h4>
              <p className="text-sm text-gray-500 mt-1">{course.description}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`badge ${
                course.skill_area === 'hard' ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'
              }`}>
                {course.skill_area === 'hard' ? 'Hard Skill' : 'Soft Skill'}
              </span>
              <span className="badge bg-gray-100 text-gray-600">
                ~{course.estimated_hours}h
              </span>
            </div>
          </div>

          <div className="space-y-4">
            {course.lessons.map((lesson, i) => (
              <LessonViewer key={lesson.lesson_id} lesson={lesson} index={i} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

// ── Simple markdown renderer ──────────────────────────────────────────────

function renderMarkdown(md: string): string {
  return md
    .replace(/^### (.+)$/gm, '<h4 class="text-base font-semibold text-gray-800 mt-4 mb-2">$1</h4>')
    .replace(/^## (.+)$/gm, '<h3 class="text-lg font-semibold text-gray-800 mt-4 mb-2">$1</h3>')
    .replace(/^# (.+)$/gm, '<h2 class="text-xl font-bold text-gray-900 mt-4 mb-2">$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code class="bg-gray-100 px-1.5 py-0.5 rounded text-sm text-brand-700">$1</code>')
    .replace(/^- (.+)$/gm, '<li class="ml-4 list-disc text-gray-700">$1</li>')
    .replace(/^> (.+)$/gm, '<blockquote class="border-l-4 border-brand-300 pl-4 italic text-gray-600 my-2">$1</blockquote>')
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="bg-gray-900 text-green-300 rounded-lg p-4 text-sm overflow-x-auto my-3"><code>$2</code></pre>')
    .replace(/\n\n/g, '<br/><br/>')
}

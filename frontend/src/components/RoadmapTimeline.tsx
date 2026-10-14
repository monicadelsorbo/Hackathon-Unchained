import { useState } from 'react'
import type { TrainingModule, CustomCourse } from '../types'
import CourseCard from './CourseCard'
import CustomCourseViewer from './CustomCourseViewer'
import { api } from '../api/client'

interface Props {
  modules: TrainingModule[]
  requestId: string
  customCourses?: CustomCourse[] | null
}

export default function RoadmapTimeline({ modules, requestId, customCourses }: Props) {
  const [generating, setGenerating] = useState<Record<string, boolean>>({})

  // Map custom courses by module_id for quick lookup
  const courseByModule: Record<string, CustomCourse> = {}
  if (customCourses) {
    for (const c of customCourses) {
      courseByModule[c.module_id] = c
    }
  }

  async function handleGenerateCourse(moduleId: string) {
    setGenerating((prev) => ({ ...prev, [moduleId]: true }))
    try {
      await api.generateCourse(requestId, moduleId)
      // The polling on RoadmapDetailPage will pick up the new course
    } catch (err) {
      console.error('Failed to generate course:', err)
    } finally {
      // Keep the loading state for a bit — polling will update the data
      setTimeout(() => {
        setGenerating((prev) => ({ ...prev, [moduleId]: false }))
      }, 3000)
    }
  }

  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-brand-200" />

      <div className="space-y-8">
        {modules.map((mod, i) => {
          const hasCourse = !!courseByModule[mod.module_id]
          const isGenerating = generating[mod.module_id]

          return (
            <div key={mod.module_id} className="relative pl-16">
              {/* Circle on timeline */}
              <div className="absolute left-4 w-5 h-5 bg-brand-500 rounded-full border-4 border-white shadow" />

              <div className="card">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="badge bg-brand-100 text-brand-700 mb-2">
                      Modulo {i + 1} &middot; {mod.duration_weeks} settimane
                    </span>
                    <h4 className="text-lg font-semibold text-gray-900 mt-1">
                      {mod.title}
                    </h4>
                  </div>
                  <span className={`badge ${
                    mod.skill_area === 'hard' ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'
                  }`}>
                    {mod.skill_area === 'hard' ? 'Hard Skill' : 'Soft Skill'}
                  </span>
                </div>

                <p className="text-sm text-gray-600 mb-3">{mod.description}</p>

                {/* Topics */}
                <div className="flex flex-wrap gap-1 mb-4">
                  {mod.topics.map((topic) => (
                    <span key={topic} className="badge bg-gray-100 text-gray-600">
                      {topic}
                    </span>
                  ))}
                </div>

                {/* Milestone */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                  <p className="text-sm text-green-800">
                    <span className="font-medium">Milestone:</span> {mod.milestone}
                  </p>
                </div>

                {/* Learning options */}
                <div className="border-t border-gray-100 pt-4">
                  <h5 className="text-sm font-medium text-gray-700 mb-3">Modalita di apprendimento</h5>

                  <div className="grid gap-3 sm:grid-cols-2 mb-4">
                    {/* E-learning option */}
                    <div className="border border-gray-200 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 bg-blue-100 rounded flex items-center justify-center text-blue-600 text-xs font-bold">E</span>
                        <span className="text-sm font-medium text-gray-800">Corsi E-Learning</span>
                      </div>
                      <p className="text-xs text-gray-500">
                        {mod.courses && mod.courses.length > 0
                          ? `${mod.courses.length} corsi dal catalogo disponibili`
                          : 'Nessun corso nel catalogo'}
                      </p>
                    </div>

                    {/* AI-generated option */}
                    <div className={`border rounded-lg p-3 ${hasCourse ? 'border-brand-300 bg-brand-50' : 'border-gray-200'}`}>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 bg-brand-100 rounded flex items-center justify-center text-brand-600 text-xs font-bold">AI</span>
                        <span className="text-sm font-medium text-gray-800">Corso Generato AI</span>
                      </div>
                      {hasCourse ? (
                        <p className="text-xs text-brand-600 font-medium">Corso generato disponibile</p>
                      ) : (
                        <button
                          onClick={() => handleGenerateCourse(mod.module_id)}
                          disabled={isGenerating}
                          className="text-xs text-brand-600 hover:text-brand-700 font-medium disabled:opacity-50"
                        >
                          {isGenerating ? (
                            <span className="flex items-center gap-1">
                              <span className="animate-spin inline-block w-3 h-3 border-2 border-brand-500 border-t-transparent rounded-full" />
                              Generazione in corso...
                            </span>
                          ) : (
                            'Genera corso personalizzato'
                          )}
                        </button>
                      )}
                    </div>
                  </div>

                  {/* E-learning courses list */}
                  {mod.courses && mod.courses.length > 0 && (
                    <div className="mb-4">
                      <h5 className="text-sm font-medium text-gray-700 mb-2">
                        Corsi consigliati dal catalogo
                      </h5>
                      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                        {mod.courses.map((course) => (
                          <CourseCard key={course.course_id} course={course} />
                        ))}
                      </div>
                    </div>
                  )}

                  {/* AI-generated course inline */}
                  {hasCourse && (
                    <CustomCourseViewer courses={[courseByModule[mod.module_id]]} />
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

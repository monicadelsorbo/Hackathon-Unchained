import type { CourseResource } from '../types'

const platformColors: Record<string, string> = {
  Coursera: 'bg-blue-100 text-blue-800',
  Udemy: 'bg-purple-100 text-purple-800',
  'LinkedIn Learning': 'bg-cyan-100 text-cyan-800',
}

interface Props {
  course: CourseResource
}

export default function CourseCard({ course }: Props) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h4 className="text-sm font-semibold text-gray-800 leading-tight flex-1">
          {course.title}
        </h4>
        <span className={`badge ml-2 ${platformColors[course.platform] || 'bg-gray-100 text-gray-800'}`}>
          {course.platform}
        </span>
      </div>
      <div className="flex items-center gap-4 text-xs text-gray-500 mt-3">
        <span>{course.duration_hours}h</span>
        <span>&euro;{course.cost_eur.toFixed(2)}</span>
        <span className="text-yellow-600">{'★'.repeat(Math.round(course.rating))} {course.rating}</span>
      </div>
      <div className="flex flex-wrap gap-1 mt-2">
        {course.skill_tags.slice(0, 3).map((tag) => (
          <span key={tag} className="badge bg-gray-100 text-gray-600">
            {tag}
          </span>
        ))}
      </div>
    </div>
  )
}

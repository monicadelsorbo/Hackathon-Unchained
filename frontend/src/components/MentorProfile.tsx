import type { MentorMatch } from '../types'

interface Props {
  mentor: MentorMatch
}

export default function MentorProfile({ mentor }: Props) {
  return (
    <div className="card">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
        Mentore Assegnato
      </h3>
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 bg-brand-100 rounded-full flex items-center justify-center text-2xl shrink-0">
          {mentor.name.charAt(0)}
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900">{mentor.name}</h4>
          <p className="text-sm text-gray-500">{mentor.role}</p>
          <p className="text-sm text-gray-600 mt-2">{mentor.rationale}</p>
          <div className="flex flex-wrap gap-1 mt-3">
            {mentor.expertise.map((exp) => (
              <span key={exp} className="badge bg-brand-100 text-brand-700">
                {exp}
              </span>
            ))}
          </div>
          <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
            <span>Disponibilit&agrave;: {mentor.availability}</span>
            <span>Match: {Math.round(mentor.match_score)}%</span>
          </div>
        </div>
      </div>
    </div>
  )
}

import type { SkillGap } from '../types'

interface Props {
  gaps: SkillGap[]
}

export default function SkillRadar({ gaps }: Props) {
  const priorityColors: Record<string, string> = {
    high: 'bg-red-100 text-red-700 border-red-200',
    medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    low: 'bg-green-100 text-green-700 border-green-200',
  }

  return (
    <div className="card">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
        Gap Analysis
      </h3>
      <div className="space-y-3">
        {gaps.map((gap) => (
          <div key={gap.skill} className="flex items-center gap-3">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">{gap.skill}</span>
                <span className={`badge ${priorityColors[gap.priority]}`}>
                  {gap.priority}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-gray-200 rounded-full h-2 relative">
                  {/* Current level */}
                  <div
                    className="bg-blue-400 h-2 rounded-full absolute"
                    style={{ width: `${(gap.current_level / 5) * 100}%` }}
                  />
                  {/* Target level marker */}
                  <div
                    className="absolute top-1/2 -translate-y-1/2 w-0.5 h-4 bg-red-500"
                    style={{ left: `${(gap.target_level / 5) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 w-16 text-right">
                  {gap.current_level} → {gap.target_level}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-4 mt-4 text-xs text-gray-400">
        <span className="flex items-center gap-1">
          <span className="w-3 h-2 bg-blue-400 rounded" /> Attuale
        </span>
        <span className="flex items-center gap-1">
          <span className="w-0.5 h-3 bg-red-500" /> Target
        </span>
      </div>
    </div>
  )
}

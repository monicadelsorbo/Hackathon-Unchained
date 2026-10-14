import type { AgentStatus } from '../types'

const agentIcons: Record<string, string> = {
  'Profile Agent': '\u{1F9E0}',
  'Assessment Agent': '\u{1F4CB}',
  'Assessment Agent (Analysis)': '\u{1F50D}',
  'Plan Agent': '\u{1F4DA}',
  'Resource Agent': '\u{1F393}',
  'Cost Agent': '\u{1F4B0}',
  'Mentor Agent': '\u{1F91D}',
  'Review Agent': '\u{2705}',
  'Notify Agent': '\u{1F514}',
}

function StatusDot({ status }: { status: string }) {
  if (status === 'running') {
    return (
      <span className="relative flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500" />
      </span>
    )
  }
  if (status === 'completed') {
    return <span className="inline-flex rounded-full h-3 w-3 bg-green-500" />
  }
  if (status === 'error') {
    return <span className="inline-flex rounded-full h-3 w-3 bg-red-500" />
  }
  return <span className="inline-flex rounded-full h-3 w-3 bg-gray-300" />
}

function getElapsedTime(started: string, completed: string): string {
  if (!started) return ''
  const start = new Date(started).getTime()
  const end = completed ? new Date(completed).getTime() : Date.now()
  const seconds = Math.round((end - start) / 1000)
  return `${seconds}s`
}

interface Props {
  statuses: AgentStatus[]
}

export default function AgentStatusTracker({ statuses }: Props) {
  if (!statuses || statuses.length === 0) return null

  return (
    <div className="card">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
        Agenti AI al lavoro
      </h3>
      <div className="space-y-3">
        {statuses.map((agent) => (
          <div
            key={agent.agent_name}
            className={`flex items-center gap-3 p-3 rounded-lg border transition-all duration-300 ${
              agent.status === 'running'
                ? 'border-blue-200 bg-blue-50'
                : agent.status === 'completed'
                ? 'border-green-200 bg-green-50'
                : 'border-gray-100 bg-gray-50'
            }`}
          >
            <span className="text-xl w-8 text-center">
              {agentIcons[agent.agent_name] || '\u{1F916}'}
            </span>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-800">{agent.agent_name}</p>
              <p className="text-xs text-gray-500 capitalize">{agent.status}</p>
            </div>
            <div className="flex items-center gap-2">
              {agent.started_at && (
                <span className="text-xs text-gray-400">
                  {getElapsedTime(agent.started_at, agent.completed_at)}
                </span>
              )}
              <StatusDot status={agent.status} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

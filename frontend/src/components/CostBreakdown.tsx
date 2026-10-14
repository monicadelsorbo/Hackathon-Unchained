import type { CostBreakdown as CostBreakdownType } from '../types'

interface Props {
  cost: CostBreakdownType
}

export default function CostBreakdown({ cost }: Props) {
  return (
    <div className="card">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
        Analisi Costi e ROI
      </h3>

      {/* Summary cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-blue-700">
            &euro;{cost.total_course_cost_eur.toFixed(0)}
          </p>
          <p className="text-xs text-blue-600 mt-1">Costo Totale</p>
        </div>
        <div className="bg-purple-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-purple-700">
            {cost.total_hours.toFixed(0)}h
          </p>
          <p className="text-xs text-purple-600 mt-1">Ore Totali</p>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-green-700">
            {cost.estimated_duration_weeks}
          </p>
          <p className="text-xs text-green-600 mt-1">Settimane</p>
        </div>
      </div>

      {/* ROI */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
        <p className="text-sm text-amber-800">{cost.roi_estimate}</p>
      </div>

      {/* Per-module breakdown */}
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="text-left py-2 text-gray-500 font-medium">Modulo</th>
            <th className="text-right py-2 text-gray-500 font-medium">Corsi</th>
            <th className="text-right py-2 text-gray-500 font-medium">Ore</th>
            <th className="text-right py-2 text-gray-500 font-medium">Costo</th>
          </tr>
        </thead>
        <tbody>
          {cost.cost_per_module.map((m) => (
            <tr key={m.module_id} className="border-b border-gray-100">
              <td className="py-2 text-gray-700">{m.module_title}</td>
              <td className="py-2 text-right text-gray-600">{m.num_courses}</td>
              <td className="py-2 text-right text-gray-600">{m.hours}h</td>
              <td className="py-2 text-right text-gray-600">&euro;{m.cost_eur.toFixed(0)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

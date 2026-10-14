import { NavLink, Outlet } from 'react-router-dom'
import { useMemo } from 'react'
import { useRole } from '../hooks/useRole'

const managerNav = [
  { to: '/requests', label: 'Richieste' },
  { to: '/employees', label: 'Dipendenti' },
  { to: '/request', label: 'Nuovo Piano' },
]

const employeeNav = [
  { to: '/dashboard', label: 'Le mie Roadmap' },
  { to: '/request', label: 'Richiedi Piano' },
]

export default function Layout() {
  const { user, setUserId, allUsers } = useRole()
  const navItems = useMemo(() => {
    if (user.role === 'manager') return managerNav
    return [
      ...employeeNav,
      { to: `/employee/${user.id}`, label: 'Il mio Profilo' },
    ]
  }, [user.role, user.id])

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-brand-900 text-white flex flex-col">
        <div className="p-6 border-b border-white/10">
          <h1 className="text-xl font-bold tracking-tight">UNCHAINED</h1>
          <p className="text-xs text-brand-200 mt-1">AI Training Planner</p>
        </div>

        {/* User Switcher */}
        <div className="p-4 border-b border-white/10">
          <label className="block text-xs text-brand-200 mb-1.5 uppercase tracking-wider">
            Accesso come
          </label>
          <select
            value={user.id}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full bg-white/10 text-white text-sm rounded-lg px-3 py-2 border border-white/20 focus:outline-none focus:ring-1 focus:ring-brand-200"
          >
            {Object.values(allUsers).map((u) => (
              <option key={u.id} value={u.id} className="text-gray-900">
                {u.name} ({u.role === 'manager' ? 'Manager' : 'Dipendente'})
              </option>
            ))}
          </select>
          <span className={`inline-block mt-2 text-xs px-2 py-0.5 rounded-full ${
            user.role === 'manager'
              ? 'bg-purple-500/30 text-purple-200'
              : 'bg-green-500/30 text-green-200'
          }`}>
            {user.role === 'manager' ? 'Manager' : 'Dipendente'}
          </span>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-white/15 text-white'
                    : 'text-brand-200 hover:bg-white/10 hover:text-white'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-white/10 text-xs text-brand-200">
          Hackathon MVP v1.0
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}

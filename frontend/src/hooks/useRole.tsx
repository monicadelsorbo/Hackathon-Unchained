import { createContext, useContext, useState, type ReactNode } from 'react'

export type UserRole = 'manager' | 'employee'

export interface UserInfo {
  role: UserRole
  id: string
  name: string
  employeeId?: string // solo per dipendente
}

const USERS: Record<string, UserInfo> = {
  'mgr-001': { role: 'manager', id: 'mgr-001', name: 'Laura Conti' },
  'emp-001': { role: 'employee', id: 'emp-001', name: 'Marco Bianchi', employeeId: 'emp-001' },
  'emp-002': { role: 'employee', id: 'emp-002', name: 'Giulia Rossi', employeeId: 'emp-002' },
  'emp-003': { role: 'employee', id: 'emp-003', name: 'Alessandro Ferretti', employeeId: 'emp-003' },
}

interface RoleContextType {
  user: UserInfo
  setUserId: (id: string) => void
  allUsers: typeof USERS
}

const RoleContext = createContext<RoleContextType | null>(null)

export function RoleProvider({ children }: { children: ReactNode }) {
  const [userId, setUserId] = useState('mgr-001')
  const user = USERS[userId] || USERS['mgr-001']

  return (
    <RoleContext.Provider value={{ user, setUserId, allUsers: USERS }}>
      {children}
    </RoleContext.Provider>
  )
}

export function useRole() {
  const ctx = useContext(RoleContext)
  if (!ctx) throw new Error('useRole must be used within RoleProvider')
  return ctx
}

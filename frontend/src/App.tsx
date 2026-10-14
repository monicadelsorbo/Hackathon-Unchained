import { Routes, Route, Navigate } from 'react-router-dom'
import { useRole } from './hooks/useRole'
import Layout from './components/Layout'
import RequestPage from './pages/RequestPage'
import RequestStatusPage from './pages/RequestStatusPage'
import RequestsListPage from './pages/RequestsListPage'
import AssessmentPage from './pages/AssessmentPage'
import DashboardPage from './pages/DashboardPage'
import RoadmapDetailPage from './pages/RoadmapDetailPage'
import ReviewPage from './pages/ReviewPage'
import EmployeesListPage from './pages/EmployeesListPage'
import EmployeeProfilePage from './pages/EmployeeProfilePage'

function HomeRedirect() {
  const { user } = useRole()
  return <Navigate to={user.role === 'manager' ? '/requests' : '/dashboard'} replace />
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomeRedirect />} />
        <Route path="/request" element={<RequestPage />} />
        <Route path="/request/:id" element={<RequestStatusPage />} />
        <Route path="/requests" element={<RequestsListPage />} />
        <Route path="/assessment/:id" element={<AssessmentPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/roadmap/:id" element={<RoadmapDetailPage />} />
        <Route path="/review/:id" element={<ReviewPage />} />
        <Route path="/employees" element={<EmployeesListPage />} />
        <Route path="/employee/:employeeId" element={<EmployeeProfilePage />} />
      </Route>
    </Routes>
  )
}

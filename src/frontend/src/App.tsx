import { Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import Landing from './components/Landing'
import Login from './components/Login'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import Products from './components/Products'
import Orders from './components/Orders'
import Categories from './components/Categories'
import Variants from './components/Variants'
import Options from './components/Options'
import TimeSlots from './components/TimeSlots'
import DeliveryZones from './components/DeliveryZones'
import Conversations from './components/Conversations'
import Users from './components/Users'
import Customers from './components/Customers'
import Notifications from './components/Notifications'
import Settings from './components/Settings'
import Ratings from './components/Ratings'
import Permissions from './components/Permissions'
import Statistics from './components/Statistics'
import AuditLogs from './components/AuditLogs'
import InstallPage from './components/InstallPage'

function App() {
  return (
    <AppProvider>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/products" element={<Products />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/variants" element={<Variants />} />
          <Route path="/options" element={<Options />} />
          <Route path="/timeslots" element={<TimeSlots />} />
          <Route path="/delivery" element={<DeliveryZones />} />
          <Route path="/conversations" element={<Conversations />} />
          <Route path="/users" element={<Users />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/ratings" element={<Ratings />} />
          <Route path="/permissions" element={<Permissions />} />
          <Route path="/statistics" element={<Statistics />} />
          <Route path="/audit" element={<AuditLogs />} />
          <Route path="/install" element={<InstallPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AppProvider>
  )
}

export default App
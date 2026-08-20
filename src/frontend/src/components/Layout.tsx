import { useEffect, useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { logout, api } from '../api'
import NotificationCenter from './NotificationCenter'
import InstallPWA from './InstallPWA'
import { useAppContext } from '../context/AppContext'

function Layout() {
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { appName, setAppName, soundEnabled, setSoundEnabled } = useAppContext()

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await api.get('/settings')
        if (response.data.app_name) setAppName(response.data.app_name)
        if (response.data.sound_enabled !== undefined) setSoundEnabled(response.data.sound_enabled)
      } catch (err) {
        console.error(err)
      }
    }
    fetchSettings()
  }, [setAppName, setSoundEnabled])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const closeSidebar = () => setSidebarOpen(false)

  return (
    <div className="layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>{appName}</h2>
        </div>
        <nav className="sidebar-nav" onClick={closeSidebar}>
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>📊</span> Tableau de bord
          </NavLink>
          <NavLink to="/statistics" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>📈</span> Statistiques
          </NavLink>
          <NavLink to="/products" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>📦</span> Produits
          </NavLink>
          <NavLink to="/categories" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🗂️</span> Catégories
          </NavLink>
          <NavLink to="/variants" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🔀</span> Variantes
          </NavLink>
          <NavLink to="/options" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>⚙️</span> Options
          </NavLink>
          <NavLink to="/timeslots" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🕒</span> Créneaux
          </NavLink>
          <NavLink to="/delivery" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🚚</span> Livraison
          </NavLink>
          <NavLink to="/orders" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🧾</span> Commandes
          </NavLink>
          <NavLink to="/conversations" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>💬</span> Conversations
          </NavLink>
          <NavLink to="/customers" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>👥</span> Clients
          </NavLink>
          <NavLink to="/users" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🛡️</span> Utilisateurs
          </NavLink>
          <NavLink to="/notifications" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🔔</span> Notifications
          </NavLink>
          <NavLink to="/ratings" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>⭐</span> Évaluations
          </NavLink>
          <NavLink to="/permissions" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🔐</span> Permissions
          </NavLink>
          <NavLink to="/audit" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>📋</span> Audit
          </NavLink>
          <NavLink to="/settings" className={({ isActive }) => (isActive ? 'active' : '')}>
            <span>🔧</span> Paramètres
          </NavLink>
        </nav>
        <div className="sidebar-footer">
          <button className="btn btn-danger" onClick={handleLogout}>Déconnexion</button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button className="hamburger" onClick={() => setSidebarOpen(!sidebarOpen)}>
            ☰
          </button>
          <h1>{appName}</h1>
          <InstallPWA />
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </main>

      <NotificationCenter />
    </div>
  )
}

export default Layout
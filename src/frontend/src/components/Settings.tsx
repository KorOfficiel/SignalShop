import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAppContext } from '../context/AppContext'

function Settings() {
  const { appName, setAppName, soundEnabled, setSoundEnabled } = useAppContext()
  const [activeTab, setActiveTab] = useState('general')
  const [name, setName] = useState(appName)
  const [sound, setSound] = useState(soundEnabled)
  const [welcomeMessage, setWelcomeMessage] = useState('Bonjour ! Bienvenue chez SignalShop. Comment puis-je vous aider ?')
  const [tone, setTone] = useState('vous')
  const [signalPhone, setSignalPhone] = useState('')
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')
  const [permissions, setPermissions] = useState<any>({})

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const [settingsRes, permissionsRes] = await Promise.all([
          api.get('/settings'),
          api.get('/permissions'),
        ])
        const data = settingsRes.data
        if (data.app_name) setName(data.app_name)
        if (data.sound_enabled !== undefined) setSound(data.sound_enabled)
        if (data.welcome_message) setWelcomeMessage(data.welcome_message)
        if (data.tone) setTone(data.tone)
        if (data.signal_service_phone) setSignalPhone(data.signal_service_phone)
        setPermissions(permissionsRes.data)
      } catch (err) {
        console.error(err)
      }
    }
    fetchSettings()
  }, [])

  const handleSaveGeneral = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaved(false)
    setError('')
    try {
      await api.put('/settings', {
        app_name: name,
        sound_enabled: sound,
        welcome_message: welcomeMessage,
        tone: tone,
        signal_service_phone: signalPhone,
      })
      setAppName(name)
      setSoundEnabled(sound)
      setSaved(true)
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde')
    }
  }

  const handleSavePermissions = async () => {
    setSaved(false)
    setError('')
    try {
      await api.put('/permissions', permissions)
      setSaved(true)
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde des permissions')
    }
  }

  const handlePermissionChange = (role: string, permission: string) => {
    setPermissions((prev: any) => ({
      ...prev,
      [role]: {
        ...prev[role],
        [permission]: !prev[role]?.[permission],
      },
    }))
  }

  return (
    <div>
      <h1>Paramètres</h1>
      <div className="tabs">
        <button className={activeTab === 'general' ? 'tab active' : 'tab'} onClick={() => setActiveTab('general')}>Général</button>
        <button className={activeTab === 'signal' ? 'tab active' : 'tab'} onClick={() => setActiveTab('signal')}>Signal</button>
        <button className={activeTab === 'notifications' ? 'tab active' : 'tab'} onClick={() => setActiveTab('notifications')}>Notifications</button>
        <button className={activeTab === 'permissions' ? 'tab active' : 'tab'} onClick={() => setActiveTab('permissions')}>Permissions</button>
      </div>

      {activeTab === 'general' && (
        <form onSubmit={handleSaveGeneral} className="card" style={{ maxWidth: 600 }}>
          <label>Nom de l'application</label>
          <input value={name} onChange={(e) => setName(e.target.value)} />

          <label>Message d'accueil</label>
          <textarea value={welcomeMessage} onChange={(e) => setWelcomeMessage(e.target.value)} rows={3} />

          <label>Ton</label>
          <select value={tone} onChange={(e) => setTone(e.target.value)}>
            <option value="vous">Vouvoiement</option>
            <option value="tu">Tutoiement</option>
          </select>

          <label>Numéro de service Signal</label>
          <input value={signalPhone} onChange={(e) => setSignalPhone(e.target.value)} placeholder="+33612345678" />

          <button type="submit" className="btn">Enregistrer</button>
          {saved && <p className="alert-success">Paramètres enregistrés.</p>}
          {error && <p className="alert-error">{error}</p>}
        </form>
      )}

      {activeTab === 'signal' && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h2>Configuration Signal</h2>
          <p>Le numéro de service est utilisé pour envoyer les messages via Signal.</p>
          <label>Numéro de service</label>
          <input value={signalPhone} onChange={(e) => setSignalPhone(e.target.value)} placeholder="+33612345678" />
          <button className="btn" onClick={handleSaveGeneral}>Enregistrer</button>
        </div>
      )}

      {activeTab === 'notifications' && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h2>Notifications</h2>
          <label>
            <input
              type="checkbox"
              checked={sound}
              onChange={(e) => {
                setSound(e.target.checked)
                api.put('/settings', { sound_enabled: e.target.checked })
              }}
            />{' '}
            Activer les notifications sonores
          </label>
        </div>
      )}

      {activeTab === 'permissions' && (
        <div className="card" style={{ maxWidth: 900 }}>
          <h2>Permissions par rôle</h2>
          <table>
            <thead>
              <tr>
                <th>Permission</th>
                <th>OWNER</th>
                <th>ADMIN</th>
                <th>MANAGER</th>
                <th>STAFF</th>
              </tr>
            </thead>
            <tbody>
              {[
                'manage_products',
                'manage_categories',
                'manage_orders',
                'manage_users',
                'manage_settings',
                'view_conversations',
                'take_handoff',
                'manage_customers',
                'manage_scheduling',
                'manage_delivery',
                'manage_ratings',
                'manage_notifications',
                'export_orders',
                'view_statistics',
                'view_audit',
              ].map((perm) => (
                <tr key={perm}>
                  <td>{perm}</td>
                  {['OWNER', 'ADMIN', 'MANAGER', 'STAFF'].map((role) => (
                    <td key={role}>
                      <input
                        type="checkbox"
                        disabled={role === 'OWNER'}
                        checked={permissions[role]?.[perm] ?? false}
                        onChange={() => handlePermissionChange(role, perm)}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button className="btn" onClick={handleSavePermissions}>Enregistrer les permissions</button>
          {saved && <p className="alert-success">Permissions enregistrées.</p>}
          {error && <p className="alert-error">{error}</p>}
        </div>
      )}
    </div>
  )
}

export default Settings
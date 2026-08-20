import { useEffect, useState } from 'react'
import { api } from '../api'

function Permissions() {
  const [permissions, setPermissions] = useState<any>({})
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchPermissions = async () => {
      try {
        const response = await api.get('/permissions')
        setPermissions(response.data)
      } catch (err) {
        console.error(err)
      }
    }
    fetchPermissions()
  }, [])

  const handleChange = (role: string, permission: string) => {
    setPermissions((prev: any) => ({
      ...prev,
      [role]: {
        ...prev[role],
        [permission]: !prev[role][permission],
      },
    }))
  }

  const handleSave = async () => {
    setSaved(false)
    setError('')
    try {
      await api.put('/permissions', permissions)
      setSaved(true)
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || 'Erreur lors de la sauvegarde')
    }
  }

  return (
    <div>
      <h1>Permissions</h1>
      <p>Définissez ce que chaque rôle peut faire.</p>
      {saved && <p className="alert-success">Permissions enregistrées.</p>}
      {error && <p className="alert-error">{error}</p>}

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
          ].map((perm) => (
            <tr key={perm}>
              <td>{perm}</td>
              {['OWNER', 'ADMIN', 'MANAGER', 'STAFF'].map((role) => (
                <td key={role}>
                  <input
                    type="checkbox"
                    disabled={role === 'OWNER'}
                    checked={permissions[role]?.[perm] ?? false}
                    onChange={() => handleChange(role, perm)}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <button className="btn" onClick={handleSave}>Enregistrer</button>
    </div>
  )
}

export default Permissions
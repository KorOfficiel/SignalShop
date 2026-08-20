import { useEffect, useState } from 'react'
import { api } from '../api'

interface AuditEvent {
  id: string
  action: string
  entity_type?: string
  entity_id?: string
  details?: any
  created_at: string
  user_id?: string | null
}

function AuditLogs() {
  const [events, setEvents] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchEvents = async () => {
    setLoading(true)
    try {
      const response = await api.get('/audit')
      setEvents(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEvents()
  }, [])

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Journal d'audit</h1>
      {error && <p className="alert-error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Action</th>
            <th>Entité</th>
            <th>Détails</th>
            <th>Utilisateur</th>
          </tr>
        </thead>
        <tbody>
          {events.length === 0 ? (
            <tr><td colSpan={5}>Aucun événement.</td></tr>
          ) : (
            events.map((event) => (
              <tr key={event.id}>
                <td>{new Date(event.created_at).toLocaleString('fr-FR')}</td>
                <td>{event.action}</td>
                <td>{event.entity_type || '-'}</td>
                <td>{event.details ? JSON.stringify(event.details) : '-'}</td>
                <td>{event.user_id ? event.user_id.slice(0, 8) + '...' : '-'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

export default AuditLogs
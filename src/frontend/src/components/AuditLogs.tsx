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
  const [message, setMessage] = useState('')

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

  const handleDelete = async (id: string) => {
    if (!confirm('Supprimer cet événement ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/audit/${id}`)
      setMessage('Événement supprimé.')
      fetchEvents()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleClearAll = async () => {
    if (!confirm('Voulez-vous vraiment supprimer tous les journaux d\'audit ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete('/audit')
      setMessage('Tous les journaux ont été supprimés.')
      fetchEvents()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => alert('ID copié !'))
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Journal d'audit</h1>
      <button className="btn btn-danger" onClick={handleClearAll} style={{ marginBottom: 10 }}>
        Tout effacer
      </button>
      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Action</th>
            <th>Entité</th>
            <th>Détails</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {events.length === 0 ? (
            <tr><td colSpan={6}>Aucun événement.</td></tr>
          ) : (
            events.map((event) => (
              <tr key={event.id}>
                <td>
                  <span style={{ fontSize: 12 }}>{event.id.slice(0, 8)}...</span>{' '}
                  <button className="btn btn-primary btn-sm" onClick={() => copyToClipboard(event.id)}>Copier</button>
                </td>
                <td>{new Date(event.created_at).toLocaleString('fr-FR')}</td>
                <td>{event.action}</td>
                <td>{event.entity_type || '-'}</td>
                <td>{event.details ? JSON.stringify(event.details) : '-'}</td>
                <td>
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(event.id)}>Supprimer</button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

export default AuditLogs
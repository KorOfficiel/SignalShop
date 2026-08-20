import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Notification {
  id: string
  type: string
  message: string
  read: boolean
  created_at: string
}

function Notifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const fetchNotifications = async () => {
    setLoading(true)
    try {
      const response = await api.get('/notifications')
      setNotifications(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNotifications()
  }, [])

  const markAsRead = async (id: string) => {
    setError('')
    setMessage('')
    try {
      await api.patch(`/notifications/${id}/read`)
      fetchNotifications()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  const markAllAsRead = async () => {
    setError('')
    setMessage('')
    try {
      await api.patch('/notifications/read-all')
      setMessage('Toutes les notifications sont lues.')
      fetchNotifications()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  const deleteNotification = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cette notification ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/notifications/${id}`)
      setMessage('Notification supprimée.')
      fetchNotifications()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  const deleteAllNotifications = async () => {
    if (!confirm('Voulez-vous vraiment supprimer toutes les notifications ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete('/notifications')
      setMessage('Toutes les notifications sont supprimées.')
      fetchNotifications()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Notifications</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={markAllAsRead} style={{ marginLeft: 10 }}>
          Tout marquer comme lu
        </button>
        <button className="btn btn-danger" onClick={deleteAllNotifications} style={{ marginLeft: 10 }}>
          Tout supprimer
        </button>
      </nav>
      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}

      {notifications.length === 0 ? (
        <p>Aucune notification.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Message</th>
              <th>Date</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {notifications.map((notif) => (
              <tr key={notif.id} style={{ background: notif.read ? 'transparent' : '#f9f9f9' }}>
                <td>{notif.type}</td>
                <td>{notif.message}</td>
                <td>{new Date(notif.created_at).toLocaleString('fr-FR')}</td>
                <td>{notif.read ? 'Lu' : 'Non lu'}</td>
                <td>
                  {!notif.read && (
                    <button className="btn btn-primary" onClick={() => markAsRead(notif.id)}>
                      Marquer lu
                    </button>
                  )}
                  <button className="btn btn-danger" onClick={() => deleteNotification(notif.id)} style={{ marginLeft: 5 }}>
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Notifications
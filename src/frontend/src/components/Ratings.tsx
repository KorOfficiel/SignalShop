import { useEffect, useState } from 'react'
import { api } from '../api'

interface Rating {
  id: string
  customer_id: string
  rating: number
  comment?: string | null
  created_at: string
}

function Ratings() {
  const [ratings, setRatings] = useState<Rating[]>([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const fetchRatings = async () => {
    setLoading(true)
    try {
      const response = await api.get('/ratings')
      setRatings(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRatings()
  }, [])

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous supprimer cette évaluation ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/ratings/${id}`)
      setMessage('Évaluation supprimée.')
      fetchRatings()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur : ${err.response?.data?.detail || err.message}`)
    }
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Évaluations</h1>
      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}
      {ratings.length === 0 ? (
        <p>Aucune évaluation.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Client</th>
              <th>Note</th>
              <th>Commentaire</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {ratings.map((rating) => (
              <tr key={rating.id}>
                <td>{rating.customer_id}</td>
                <td>{'⭐'.repeat(rating.rating)} ({rating.rating}/5)</td>
                <td>{rating.comment || '-'}</td>
                <td>{new Date(rating.created_at).toLocaleString('fr-FR')}</td>
                <td>
                  <button className="btn btn-danger" onClick={() => handleDelete(rating.id)}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Ratings
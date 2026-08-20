import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface TimeSlot {
  id: string
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  active: boolean
}

function TimeSlots() {
  const [slots, setSlots] = useState<TimeSlot[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    start_time: '',
    end_time: '',
    capacity: 1,
    active: true,
  })

  const fetchSlots = async () => {
    setLoading(true)
    try {
      const response = await api.get('/scheduling/slots')
      setSlots(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des créneaux')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSlots()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target
    const val = type === 'number' ? Number(value) : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload = {
      ...formData,
      start_time: new Date(formData.start_time).toISOString(),
      end_time: new Date(formData.end_time).toISOString(),
    }
    try {
      if (editingId) {
        await api.patch(`/scheduling/slots/${editingId}`, payload)
      } else {
        await api.post('/scheduling/slots', payload)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ start_time: '', end_time: '', capacity: 1, active: true })
      fetchSlots()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement du créneau")
    }
  }

  const handleEdit = (slot: TimeSlot) => {
    setEditingId(slot.id)
    const startLocal = new Date(slot.start_time).toISOString().slice(0, 16)
    const endLocal = new Date(slot.end_time).toISOString().slice(0, 16)
    setFormData({
      start_time: startLocal,
      end_time: endLocal,
      capacity: slot.capacity,
      active: slot.active,
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer ce créneau ?')) return
    try {
      await api.delete(`/scheduling/slots/${id}`)
      fetchSlots()
    } catch (err) {
      console.error(err)
      alert('Erreur lors de la suppression')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => alert('ID copié !'))
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="container">
      <h1>Créneaux</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter un créneau'}
        </button>
      </nav>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Début</label>
          <input type="datetime-local" name="start_time" value={formData.start_time} onChange={handleChange} required />
          <label>Fin</label>
          <input type="datetime-local" name="end_time" value={formData.end_time} onChange={handleChange} required />
          <label>Capacité</label>
          <input type="number" name="capacity" value={formData.capacity} onChange={handleChange} min={1} required />
          <label>Actif</label>
          <input type="checkbox" name="active" checked={formData.active} onChange={(e) => setFormData({ ...formData, active: e.target.checked })} />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Début</th>
            <th>Fin</th>
            <th>Capacité</th>
            <th>Réservé</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {slots.map((slot) => (
            <tr key={slot.id}>
              <td>
                <span style={{ fontSize: 12 }}>{slot.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(slot.id)}>Copier</button>
              </td>
              <td>{new Date(slot.start_time).toLocaleString('fr-FR')}</td>
              <td>{new Date(slot.end_time).toLocaleString('fr-FR')}</td>
              <td>{slot.capacity}</td>
              <td>{slot.booked_count}</td>
              <td>{slot.active ? 'Actif' : 'Inactif'}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(slot)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(slot.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default TimeSlots
import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface DeliveryZone {
  id: string
  name: string
  fee: number
  min_order: number
  active: boolean
}

function DeliveryZones() {
  const [zones, setZones] = useState<DeliveryZone[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    fee: 0,
    min_order: 0,
    active: true,
  })

  const fetchZones = async () => {
    setLoading(true)
    try {
      const response = await api.get('/delivery/zones')
      setZones(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des zones')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchZones()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target
    const val = type === 'number' ? Number(value) : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingId) {
        await api.patch(`/delivery/zones/${editingId}`, formData)
      } else {
        await api.post('/delivery/zones', formData)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ name: '', fee: 0, min_order: 0, active: true })
      fetchZones()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement de la zone")
    }
  }

  const handleEdit = (zone: DeliveryZone) => {
    setEditingId(zone.id)
    setFormData({
      name: zone.name,
      fee: zone.fee,
      min_order: zone.min_order,
      active: zone.active,
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cette zone ?')) return
    try {
      await api.delete(`/delivery/zones/${id}`)
      fetchZones()
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
      <h1>Zones de livraison</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter une zone'}
        </button>
      </nav>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Nom</label>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <label>Frais (en centimes, ex: 500 = 5€)</label>
          <input type="number" name="fee" value={formData.fee} onChange={handleChange} required />
          <label>Montant minimum (en centimes)</label>
          <input type="number" name="min_order" value={formData.min_order} onChange={handleChange} />
          <label>Actif</label>
          <input type="checkbox" name="active" checked={formData.active} onChange={(e) => setFormData({ ...formData, active: e.target.checked })} />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Frais</th>
            <th>Commande min</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {zones.map((zone) => (
            <tr key={zone.id}>
              <td>
                <span style={{ fontSize: 12 }}>{zone.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(zone.id)}>Copier</button>
              </td>
              <td>{zone.name}</td>
              <td>{(zone.fee / 100).toFixed(2)} €</td>
              <td>{(zone.min_order / 100).toFixed(2)} €</td>
              <td>{zone.active ? 'Actif' : 'Inactif'}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(zone)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(zone.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DeliveryZones
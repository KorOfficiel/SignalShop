import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Customer {
  id: string
  signal_phone_hash: string
}

function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    signal_phone_hash: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const fetchCustomers = async () => {
    setLoading(true)
    try {
      const response = await api.get('/customers')
      setCustomers(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur chargement : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCustomers()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      if (editingId) {
        await api.patch(`/customers/${editingId}`, formData)
        setMessage('Client modifié.')
      } else {
        await api.post('/customers', formData)
        setMessage('Client créé avec succès.')
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ signal_phone_hash: '' })
      fetchCustomers()
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || err.message || "Erreur lors de l'enregistrement")
    }
  }

  const handleEdit = (customer: Customer) => {
    setEditingId(customer.id)
    setFormData({ signal_phone_hash: customer.signal_phone_hash })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('⚠️ Supprimer définitivement ce client ?\n\nCela supprimera aussi ses paniers, commandes et conversations, et réapprovisionnera le stock.')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/customers/${id}`)
      setMessage('Client et données associées supprimés.')
      fetchCustomers()
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || err.message || 'Erreur lors de la suppression')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => alert('ID copié !'))
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="container">
      <h1>Clients</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); setError(''); setMessage(''); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter un client'}
        </button>
      </nav>

      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Signal Phone Hash</label>
          <input name="signal_phone_hash" value={formData.signal_phone_hash} onChange={handleChange} required />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Signal Phone Hash</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.id}>
              <td>
                <span style={{ fontSize: 12 }}>{customer.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(customer.id)}>Copier</button>
              </td>
              <td>{customer.signal_phone_hash}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(customer)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(customer.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Customers
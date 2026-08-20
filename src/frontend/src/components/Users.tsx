import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface User {
  id: string
  email: string
  full_name?: string | null
  role: string
}

function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    role: 'STAFF',
    password: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const response = await api.get('/users')
      setUsers(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur chargement : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setMessage('')
    try {
      if (editingId) {
        await api.patch(`/users/${editingId}`, formData)
        setMessage('Utilisateur modifié.')
      } else {
        await api.post('/users', formData)
        setMessage('Utilisateur créé avec succès.')
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ email: '', full_name: '', role: 'STAFF', password: '' })
      fetchUsers()
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || err.message || "Erreur lors de l'enregistrement")
    }
  }

  const handleEdit = (user: User) => {
    setEditingId(user.id)
    setFormData({
      email: user.email,
      full_name: user.full_name || '',
      role: user.role,
      password: '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cet utilisateur ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/users/${id}`)
      setMessage('Utilisateur supprimé.')
      fetchUsers()
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || err.message || 'Erreur lors de la suppression')
    }
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="container">
      <h1>Utilisateurs</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); setError(''); setMessage(''); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter un utilisateur'}
        </button>
      </nav>

      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Email</label>
          <input name="email" type="email" value={formData.email} onChange={handleChange} required />
          <label>Nom complet</label>
          <input name="full_name" value={formData.full_name} onChange={handleChange} />
          <label>Rôle</label>
          <select name="role" value={formData.role} onChange={handleChange}>
            <option value="OWNER">OWNER</option>
            <option value="ADMIN">ADMIN</option>
            <option value="MANAGER">MANAGER</option>
            <option value="STAFF">STAFF</option>
          </select>
          {!editingId && (
            <>
              <label>Mot de passe</label>
              <input name="password" type="password" value={formData.password} onChange={handleChange} required />
            </>
          )}
          {editingId && (
            <>
              <label>Nouveau mot de passe (optionnel)</label>
              <input name="password" type="password" value={formData.password} onChange={handleChange} placeholder="Laisser vide pour ne pas changer" />
            </>
          )}
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Nom complet</th>
            <th>Rôle</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.email}</td>
              <td>{user.full_name || '-'}</td>
              <td>{user.role}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(user)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(user.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Users
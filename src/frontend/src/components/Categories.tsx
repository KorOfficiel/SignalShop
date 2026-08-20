import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Category {
  id: string
  name: string
  description?: string | null
  position: number
  active: boolean
}

function Categories() {
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    position: 0,
    active: true,
  })

  const fetchCategories = async () => {
    setLoading(true)
    try {
      const response = await api.get('/catalog/categories')
      setCategories(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des catégories')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCategories()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    const val = type === 'number' ? Number(value) : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingId) {
        await api.patch(`/catalog/categories/${editingId}`, formData)
      } else {
        await api.post('/catalog/categories', formData)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ name: '', description: '', position: 0, active: true })
      fetchCategories()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement de la catégorie")
    }
  }

  const handleEdit = (category: Category) => {
    setEditingId(category.id)
    setFormData({
      name: category.name,
      description: category.description || '',
      position: category.position,
      active: category.active,
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cette catégorie ?')) return
    try {
      await api.delete(`/catalog/categories/${id}`)
      fetchCategories()
    } catch (err) {
      console.error(err)
      alert('Erreur lors de la suppression (peut-être liée à des produits)')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => alert('ID copié !'))
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="container">
      <h1>Catégories</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter une catégorie'}
        </button>
      </nav>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Nom</label>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <label>Description</label>
          <textarea name="description" value={formData.description} onChange={handleChange} />
          <label>Position</label>
          <input type="number" name="position" value={formData.position} onChange={handleChange} />
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
            <th>Description</th>
            <th>Position</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((category) => (
            <tr key={category.id}>
              <td>
                <span style={{ fontSize: 12 }}>{category.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(category.id)}>Copier</button>
              </td>
              <td>{category.name}</td>
              <td>{category.description || '-'}</td>
              <td>{category.position}</td>
              <td>{category.active ? 'Actif' : 'Inactif'}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(category)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(category.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Categories
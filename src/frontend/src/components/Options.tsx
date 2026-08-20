import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Product {
  id: string
  name: string
}

interface OptionDefinition {
  id: string
  product_id: string
  name: string
  type: string
  required: boolean
  choices?: string[] | null
}

function Options() {
  const [options, setOptions] = useState<OptionDefinition[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    product_id: '',
    name: '',
    type: 'single_choice',
    required: false,
    choices: '',
  })

  const fetchOptions = async () => {
    setLoading(true)
    try {
      const response = await api.get('/catalog/options')
      setOptions(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des options')
    } finally {
      setLoading(false)
    }
  }

  const fetchProducts = async () => {
    try {
      const response = await api.get('/catalog/products')
      setProducts(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchOptions()
    fetchProducts()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.product_id) {
      alert('Veuillez sélectionner un produit')
      return
    }
    try {
      const payload = {
        ...formData,
        choices: formData.choices ? formData.choices.split(',').map((s) => s.trim()) : null,
      }
      if (editingId) {
        await api.patch(`/catalog/options/${editingId}`, payload)
      } else {
        await api.post('/catalog/options', payload)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ product_id: '', name: '', type: 'single_choice', required: false, choices: '' })
      fetchOptions()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement de l'option")
    }
  }

  const handleEdit = (option: OptionDefinition) => {
    setEditingId(option.id)
    setFormData({
      product_id: option.product_id,
      name: option.name,
      type: option.type,
      required: option.required,
      choices: option.choices ? option.choices.join(', ') : '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cette option ?')) return
    try {
      await api.delete(`/catalog/options/${id}`)
      fetchOptions()
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
      <h1>Options</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter une option'}
        </button>
      </nav>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Produit</label>
          <select name="product_id" value={formData.product_id} onChange={handleChange} required>
            <option value="">Sélectionner un produit</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>{product.name}</option>
            ))}
          </select>
          <label>Nom de l'option</label>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <label>Type</label>
          <select name="type" value={formData.type} onChange={handleChange}>
            <option value="single_choice">Choix unique</option>
            <option value="multiple_choice">Choix multiple</option>
            <option value="text">Texte</option>
            <option value="number">Nombre</option>
            <option value="boolean">Oui/Non</option>
          </select>
          {['single_choice', 'multiple_choice'].includes(formData.type) && (
            <>
              <label>Choix (séparés par des virgules)</label>
              <input name="choices" value={formData.choices} onChange={handleChange} placeholder="Noir, Lait, Blanc" />
            </>
          )}
          <label>Requis</label>
          <input type="checkbox" name="required" checked={formData.required} onChange={handleChange} />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Produit</th>
            <th>Nom</th>
            <th>Type</th>
            <th>Requis</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {options.map((option) => {
            const product = products.find((p) => p.id === option.product_id)
            return (
              <tr key={option.id}>
                <td>
                  <span style={{ fontSize: 12 }}>{option.id.slice(0, 8)}...</span>{' '}
                  <button className="btn btn-primary" onClick={() => copyToClipboard(option.id)}>Copier</button>
                </td>
                <td>{product ? product.name : option.product_id}</td>
                <td>{option.name}</td>
                <td>{option.type}</td>
                <td>{option.required ? 'Oui' : 'Non'}</td>
                <td>
                  <button className="btn btn-primary" onClick={() => handleEdit(option)}>Modifier</button>
                  <button className="btn btn-danger" onClick={() => handleDelete(option.id)}>Supprimer</button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default Options
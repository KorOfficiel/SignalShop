import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Product {
  id: string
  name: string
}

interface Variant {
  id: string
  product_id: string
  name: string
  description?: string | null
  price_modifier: number
  price_override?: number | null
  stock_quantity?: number | null
  reference?: string | null
  image_url?: string | null
  active: boolean
}

function Variants() {
  const [variants, setVariants] = useState<Variant[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    product_id: '',
    name: '',
    description: '',
    price_modifier: 0,
    price_override: null as number | null,
    stock_quantity: null as number | null,
    reference: '',
    image_url: '',
    active: true,
  })

  const fetchVariants = async () => {
    setLoading(true)
    try {
      const response = await api.get('/catalog/variants')
      setVariants(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des variantes')
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
    fetchVariants()
    fetchProducts()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    const val = type === 'number' ? Number(value) : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.product_id) {
      alert('Veuillez sélectionner un produit')
      return
    }
    try {
      if (editingId) {
        await api.patch(`/catalog/variants/${editingId}`, formData)
      } else {
        await api.post('/catalog/variants', formData)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({ product_id: '', name: '', description: '', price_modifier: 0, price_override: null, stock_quantity: null, reference: '', image_url: '', active: true })
      fetchVariants()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement de la variante")
    }
  }

  const handleEdit = (variant: Variant) => {
    setEditingId(variant.id)
    setFormData({
      product_id: variant.product_id,
      name: variant.name,
      description: variant.description || '',
      price_modifier: variant.price_modifier,
      price_override: variant.price_override ?? null,
      stock_quantity: variant.stock_quantity ?? null,
      reference: variant.reference || '',
      image_url: variant.image_url || '',
      active: variant.active,
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer cette variante ?')) return
    try {
      await api.delete(`/catalog/variants/${id}`)
      fetchVariants()
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
      <h1>Variantes</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter une variante'}
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
          <label>Nom</label>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <label>Description</label>
          <textarea name="description" value={formData.description} onChange={handleChange} />
          <label>Supplément (en centimes)</label>
          <input type="number" name="price_modifier" value={formData.price_modifier} onChange={handleChange} />
          <label>Prix fixe alternatif (en centimes, laisser vide si aucun)</label>
          <input type="number" name="price_override" value={formData.price_override ?? ''} onChange={(e) => setFormData({ ...formData, price_override: e.target.value === '' ? null : Number(e.target.value) })} />
          <label>Stock (laisser vide si illimité)</label>
          <input type="number" name="stock_quantity" value={formData.stock_quantity ?? ''} onChange={(e) => setFormData({ ...formData, stock_quantity: e.target.value === '' ? null : Number(e.target.value) })} />
          <label>Référence</label>
          <input name="reference" value={formData.reference} onChange={handleChange} />
          <label>URL Image</label>
          <input name="image_url" value={formData.image_url} onChange={handleChange} />
          <label>Actif</label>
          <input type="checkbox" name="active" checked={formData.active} onChange={(e) => setFormData({ ...formData, active: e.target.checked })} />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Produit</th>
            <th>Nom</th>
            <th>Supplément</th>
            <th>Stock</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {variants.map((variant) => {
            const product = products.find((p) => p.id === variant.product_id)
            return (
              <tr key={variant.id}>
                <td>
                  <span style={{ fontSize: 12 }}>{variant.id.slice(0, 8)}...</span>{' '}
                  <button className="btn btn-primary" onClick={() => copyToClipboard(variant.id)}>Copier</button>
                </td>
                <td>{product ? product.name : variant.product_id}</td>
                <td>{variant.name}</td>
                <td>{(variant.price_modifier / 100).toFixed(2)} €</td>
                <td>{variant.stock_quantity ?? 'Illimité'}</td>
                <td>{variant.active ? 'Actif' : 'Inactif'}</td>
                <td>
                  <button className="btn btn-primary" onClick={() => handleEdit(variant)}>Modifier</button>
                  <button className="btn btn-danger" onClick={() => handleDelete(variant.id)}>Supprimer</button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default Variants
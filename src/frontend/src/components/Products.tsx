import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Product {
  id: string
  name: string
  description?: string | null
  base_price: number
  stock_quantity?: number | null
  stock_mode: string
  active: boolean
  category_id?: string | null
}

function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    base_price: 0,
    unit: 'unité',
    stock_mode: 'illimited',
    stock_quantity: 0,
    active: true,
    category_id: '',
  })

  const fetchProducts = async () => {
    setLoading(true)
    try {
      const response = await api.get('/catalog/products')
      setProducts(response.data)
    } catch (err) {
      console.error(err)
      alert('Erreur lors du chargement des produits')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    const val = type === 'number' ? Number(value) : value
    setFormData({ ...formData, [name]: val })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        ...formData,
        category_id: formData.category_id ? formData.category_id : null,
      }
      if (editingId) {
        await api.patch(`/catalog/products/${editingId}`, payload)
      } else {
        await api.post('/catalog/products', payload)
      }
      setShowForm(false)
      setEditingId(null)
      setFormData({
        name: '',
        description: '',
        base_price: 0,
        unit: 'unité',
        stock_mode: 'illimited',
        stock_quantity: 0,
        active: true,
        category_id: '',
      })
      fetchProducts()
    } catch (err) {
      console.error(err)
      alert("Erreur lors de l'enregistrement du produit")
    }
  }

  const handleEdit = (product: Product) => {
    setEditingId(product.id)
    setFormData({
      name: product.name,
      description: product.description || '',
      base_price: product.base_price,
      unit: 'unité',
      stock_mode: product.stock_mode,
      stock_quantity: product.stock_quantity ?? 0,
      active: product.active,
      category_id: product.category_id || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Voulez-vous vraiment supprimer ce produit ?')) return
    try {
      await api.delete(`/catalog/products/${id}`)
      fetchProducts()
    } catch (err) {
      console.error(err)
      alert('Erreur lors de la suppression')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('ID copié dans le presse-papier !')
    })
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div className="container">
      <h1>Produits</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => { setShowForm(!showForm); setEditingId(null); }} style={{ marginLeft: 10 }}>
          {showForm ? 'Annuler' : 'Ajouter un produit'}
        </button>
      </nav>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 400 }}>
          <label>Nom</label>
          <input name="name" value={formData.name} onChange={handleChange} required />
          <label>Description</label>
          <textarea name="description" value={formData.description} onChange={handleChange} />
          <label>Prix (en centimes, ex: 1400 pour 14€)</label>
          <input type="number" name="base_price" value={formData.base_price} onChange={handleChange} required />
          <label>Unité</label>
          <input name="unit" value={formData.unit} onChange={handleChange} />
          <label>Mode de stock</label>
          <select name="stock_mode" value={formData.stock_mode} onChange={handleChange}>
            <option value="illimited">Illimité</option>
            <option value="limited">Limité</option>
            <option value="unavailable">Indisponible</option>
          </select>
          {formData.stock_mode === 'limited' && (
            <>
              <label>Quantité en stock</label>
              <input type="number" name="stock_quantity" value={formData.stock_quantity} onChange={handleChange} />
            </>
          )}
          <label>Actif</label>
          <input type="checkbox" name="active" checked={formData.active} onChange={(e) => setFormData({ ...formData, active: e.target.checked })} />
          <label>ID de catégorie (optionnel)</label>
          <input name="category_id" value={formData.category_id} onChange={handleChange} placeholder="UUID" />
          <button className="btn" type="submit">{editingId ? 'Mettre à jour' : 'Enregistrer'}</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Description</th>
            <th>Prix</th>
            <th>Stock</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>
                <span style={{ fontSize: 12 }}>{product.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(product.id)}>Copier</button>
              </td>
              <td>{product.name}</td>
              <td>{product.description || '-'}</td>
              <td>{(product.base_price / 100).toFixed(2)} €</td>
              <td>
                {product.stock_mode === 'illimited'
                  ? 'Illimité'
                  : product.stock_quantity !== null && product.stock_quantity !== undefined
                  ? product.stock_quantity
                  : '-'}
              </td>
              <td>{product.active ? 'Actif' : 'Inactif'}</td>
              <td>
                <button className="btn btn-primary" onClick={() => handleEdit(product)}>Modifier</button>
                <button className="btn btn-danger" onClick={() => handleDelete(product.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Products
import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface OrderItem {
  id: string
  product_id: string
  variant_id?: string | null
  quantity: number
  options?: any
  unit_price: number
  total_price: number
}

interface Order {
  id: string
  customer_id: string
  total_amount: number
  delivery_fee: number
  status: string
  created_at: string
  delivery_address?: any
  scheduled_slot_id?: string | null
  items: OrderItem[]
}

interface Customer {
  id: string
  signal_phone_hash: string
}

interface Product {
  id: string
  name: string
  base_price: number
  stock_mode: string
  stock_quantity?: number | null
}

interface TimeSlot {
  id: string
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  active: boolean
}

interface DeliveryZone {
  id: string
  name: string
  fee: number
  min_order: number
  active: boolean
}

const STATUSES = ['DRAFT','PENDING_CONFIRMATION','CONFIRMED','ACCEPTED','IN_PREPARATION','READY','OUT_FOR_DELIVERY','COMPLETED','CANCELLED','REFUSED','EXPIRED']

function Orders() {
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [customers, setCustomers] = useState<Customer[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [timeSlots, setTimeSlots] = useState<TimeSlot[]>([])
  const [deliveryZones, setDeliveryZones] = useState<DeliveryZone[]>([])
  const [selectedCustomerId, setSelectedCustomerId] = useState('')
  const [selectedSlotId, setSelectedSlotId] = useState('')
  const [selectedZoneId, setSelectedZoneId] = useState('')
  const [items, setItems] = useState([{ product_id: '', quantity: 1 }])

  const fetchOrders = async () => {
    setLoading(true)
    try {
      const response = await api.get('/orders')
      setOrders(response.data)
    } catch (err) {
      console.error(err)
      setError('Erreur lors du chargement des commandes')
    } finally {
      setLoading(false)
    }
  }

  const fetchData = async () => {
    try {
      const [custRes, prodRes, slotsRes, zonesRes] = await Promise.all([
        api.get('/customers'),
        api.get('/catalog/products'),
        api.get('/scheduling/slots'),
        api.get('/delivery/zones'),
      ])
      setCustomers(custRes.data)
      setProducts(prodRes.data)
      setTimeSlots(slotsRes.data.filter((s: TimeSlot) => s.active && s.booked_count < s.capacity))
      setDeliveryZones(zonesRes.data.filter((z: DeliveryZone) => z.active))
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchOrders()
    fetchData()
  }, [])

  const handleAddItem = () => {
    setItems([...items, { product_id: '', quantity: 1 }])
  }

  const handleRemoveItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index))
  }

  const handleItemChange = (index: number, field: 'product_id' | 'quantity', value: string | number) => {
    const newItems = [...items]
    newItems[index] = { ...newItems[index], [field]: value }
    setItems(newItems)
  }

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setMessage('')
    if (!selectedCustomerId) {
      setError('Veuillez sélectionner un client.')
      return
    }
    if (items.length === 0 || items.some((item) => !item.product_id)) {
      setError('Veuillez ajouter au moins un produit.')
      return
    }
    try {
      await api.post('/orders/direct', {
        customer_id: selectedCustomerId,
        items: items.map((item) => ({
          product_id: item.product_id,
          quantity: Number(item.quantity),
        })),
        scheduled_slot_id: selectedSlotId || null,
        delivery_zone_id: selectedZoneId || null,
      })
      setMessage('Commande créée avec succès.')
      setShowCreateForm(false)
      setSelectedCustomerId('')
      setSelectedSlotId('')
      setSelectedZoneId('')
      setItems([{ product_id: '', quantity: 1 }])
      fetchOrders()
      fetchData()
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || "Erreur lors de la création de la commande")
    }
  }

  const handleStatusChange = async (orderId: string, newStatus: string) => {
    setError('')
    setMessage('')
    try {
      await api.patch(`/orders/${orderId}`, { status: newStatus })
      setMessage('Statut mis à jour.')
      fetchOrders()
      if (selectedOrder && selectedOrder.id === orderId) {
        setSelectedOrder({ ...selectedOrder, status: newStatus })
      }
    } catch (err) {
      console.error(err)
      setError("Erreur lors du changement de statut.")
    }
  }

  const handleCancelOrder = async (orderId: string) => {
    if (!confirm('Voulez-vous vraiment annuler cette commande ?')) return
    setError('')
    setMessage('')
    try {
      await api.post(`/orders/${orderId}/cancel`)
      setMessage('Commande annulée.')
      fetchOrders()
      if (selectedOrder && selectedOrder.id === orderId) {
        setSelectedOrder({ ...selectedOrder, status: 'CANCELLED' })
      }
    } catch (err) {
      console.error(err)
      setError("Erreur lors de l'annulation de la commande")
    }
  }

  const handleDeleteOrder = async (orderId: string) => {
    if (!confirm('Voulez-vous supprimer définitivement cette commande ?')) return
    setError('')
    setMessage('')
    try {
      await api.delete(`/orders/${orderId}`)
      setMessage('Commande supprimée.')
      setSelectedOrder(null)
      fetchOrders()
    } catch (err) {
      console.error(err)
      setError('Erreur lors de la suppression de la commande')
    }
  }

  const handleViewDetails = (order: Order) => {
    setSelectedOrder(order)
    setError('')
    setMessage('')
  }

  const handleExportCSV = async () => {
    try {
      const response = await api.get('/export/orders', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'commandes.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error(err)
      setError("Erreur lors de l'export CSV")
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => alert('ID copié !'))
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Commandes</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
        <button className="btn" onClick={() => setShowCreateForm(!showCreateForm)} style={{ marginLeft: 10 }}>
          {showCreateForm ? 'Annuler' : 'Nouvelle commande'}
        </button>
        <button className="btn" onClick={handleExportCSV} style={{ marginLeft: 10 }}>Exporter CSV</button>
      </nav>
      {message && <p className="alert-success">{message}</p>}
      {error && <p className="alert-error">{error}</p>}

      {showCreateForm && (
        <form onSubmit={handleCreateOrder} className="card" style={{ maxWidth: 700 }}>
          <h2>Créer une commande directe</h2>

          <label>Client</label>
          <select value={selectedCustomerId} onChange={(e) => setSelectedCustomerId(e.target.value)} required>
            <option value="">Sélectionner un client</option>
            {customers.map((cust) => (
              <option key={cust.id} value={cust.id}>{cust.signal_phone_hash}</option>
            ))}
          </select>

          <label>Créneau de livraison (optionnel)</label>
          <select value={selectedSlotId} onChange={(e) => setSelectedSlotId(e.target.value)}>
            <option value="">Aucun créneau</option>
            {timeSlots.map((slot) => (
              <option key={slot.id} value={slot.id}>
                {new Date(slot.start_time).toLocaleString('fr-FR')} - {new Date(slot.end_time).toLocaleTimeString('fr-FR')} ({slot.capacity - slot.booked_count} places)
              </option>
            ))}
          </select>

          <label>Zone de livraison (optionnel)</label>
          <select value={selectedZoneId} onChange={(e) => setSelectedZoneId(e.target.value)}>
            <option value="">Aucune zone</option>
            {deliveryZones.map((zone) => (
              <option key={zone.id} value={zone.id}>{zone.name} ({(zone.fee / 100).toFixed(2)} €)</option>
            ))}
          </select>

          <h3>Articles</h3>
          {items.map((item, index) => (
            <div key={index} style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
              <select
                style={{ flex: 2 }}
                value={item.product_id}
                onChange={(e) => handleItemChange(index, 'product_id', e.target.value)}
                required
              >
                <option value="">Produit</option>
                {products.map((prod) => (
                  <option key={prod.id} value={prod.id}>{prod.name} ({(prod.base_price / 100).toFixed(2)} €)</option>
                ))}
              </select>
              <input
                type="number"
                min={1}
                value={item.quantity}
                onChange={(e) => handleItemChange(index, 'quantity', Number(e.target.value))}
                style={{ width: 80 }}
                required
              />
              {items.length > 1 && (
                <button type="button" className="btn btn-danger btn-sm" onClick={() => handleRemoveItem(index)}>✕</button>
              )}
            </div>
          ))}
          <button type="button" className="btn" onClick={handleAddItem}>+ Ajouter un article</button>

          <div style={{ marginTop: 20 }}>
            <button className="btn" type="submit">Créer la commande</button>
          </div>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Total</th>
            <th>Statut</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>
                <span style={{ fontSize: 12 }}>{order.id.slice(0, 8)}...</span>{' '}
                <button className="btn btn-primary" onClick={() => copyToClipboard(order.id)}>Copier</button>
              </td>
              <td>{(order.total_amount / 100).toFixed(2)} €</td>
              <td>{order.status}</td>
              <td>{new Date(order.created_at).toLocaleString('fr-FR')}</td>
              <td>
                <button className="btn" onClick={() => handleViewDetails(order)}>Détails</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedOrder && (
        <div className="card" style={{ marginTop: 30 }}>
          <h2>Détail de la commande</h2>
          <p><strong>ID :</strong> {selectedOrder.id}</p>
          <p><strong>Client :</strong> {selectedOrder.customer_id}</p>
          <p><strong>Total :</strong> {(selectedOrder.total_amount / 100).toFixed(2)} €</p>
          <p><strong>Frais de livraison :</strong> {(selectedOrder.delivery_fee / 100).toFixed(2)} €</p>
          <p><strong>Statut :</strong> {selectedOrder.status}</p>
          <p><strong>Date :</strong> {new Date(selectedOrder.created_at).toLocaleString('fr-FR')}</p>
          {selectedOrder.delivery_address && <p><strong>Adresse :</strong> {JSON.stringify(selectedOrder.delivery_address)}</p>}
          <h3>Articles</h3>
          {selectedOrder.items.length === 0 ? (
            <p>Aucun article enregistré.</p>
          ) : (
            <ul>
              {selectedOrder.items.map((item) => (
                <li key={item.id}>Produit : {item.product_id} - Quantité : {item.quantity} - Total : {(item.total_price / 100).toFixed(2)} €</li>
              ))}
            </ul>
          )}
          <h3>Changer le statut</h3>
          <select value={selectedOrder.status} onChange={(e) => handleStatusChange(selectedOrder.id, e.target.value)}>
            {STATUSES.map((status) => <option key={status} value={status}>{status}</option>)}
          </select>
          <div style={{ marginTop: 20 }}>
            <button className="btn btn-success" onClick={() => handleStatusChange(selectedOrder.id, 'COMPLETED')}>
              Marquer comme livrée
            </button>
            <button className="btn btn-danger" onClick={() => handleCancelOrder(selectedOrder.id)}>Annuler la commande</button>
            <button className="btn btn-danger" onClick={() => handleDeleteOrder(selectedOrder.id)} style={{ marginLeft: 10 }}>Supprimer définitivement</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default Orders
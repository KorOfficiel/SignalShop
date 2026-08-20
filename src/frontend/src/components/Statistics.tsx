import { useEffect, useState } from 'react'
import { api } from '../api'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts'

function Statistics() {
  const [ordersByDay, setOrdersByDay] = useState([])
  const [topProducts, setTopProducts] = useState([])
  const [revenue, setRevenue] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ordersRes, topRes, revRes] = await Promise.all([
          api.get('/statistics/orders-by-day'),
          api.get('/statistics/top-products'),
          api.get('/statistics/revenue'),
        ])
        setOrdersByDay(ordersRes.data)
        setTopProducts(topRes.data)
        setRevenue(revRes.data.total_revenue_cents)
      } catch (err: any) {
        console.error(err)
        setError('Erreur lors du chargement des statistiques')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Statistiques</h1>
      {error && <p className="alert-error">{error}</p>}

      <div className="row">
        <div className="card stat-card">
          <h2>{(revenue / 100).toFixed(2)} €</h2>
          <p>Chiffre d'affaires</p>
        </div>
      </div>

      <div className="card">
        <h2>Commandes (7 derniers jours)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={ordersByDay}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="orders" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>Top produits</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topProducts}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="product" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="quantity" fill="#16a34a" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default Statistics
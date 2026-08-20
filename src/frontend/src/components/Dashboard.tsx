import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

function Dashboard() {
  const [counts, setCounts] = useState({
    products: 0,
    categories: 0,
    orders: 0,
    conversations: 0,
    users: 0,
    customers: 0,
    unreadNotifications: 0,
  })

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const [productsRes, categoriesRes, ordersRes, conversationsRes, usersRes, customersRes, notifRes] = await Promise.all([
          api.get('/catalog/products'),
          api.get('/catalog/categories'),
          api.get('/orders'),
          api.get('/conversations'),
          api.get('/users'),
          api.get('/customers'),
          api.get('/notifications?unread_only=true'),
        ])
        setCounts({
          products: productsRes.data.length,
          categories: categoriesRes.data.length,
          orders: ordersRes.data.length,
          conversations: conversationsRes.data.length,
          users: usersRes.data.length,
          customers: customersRes.data.length,
          unreadNotifications: notifRes.data.length,
        })
      } catch (err) {
        console.error(err)
      }
    }
    fetchCounts()
  }, [])

  return (
    <div>
      <h1>Tableau de bord</h1>
      <p>Bienvenue dans votre espace professionnel.</p>

      <div className="row">
        <Link to="/products" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.products}</h2>
            <p>Produits</p>
          </div>
        </Link>
        <Link to="/categories" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.categories}</h2>
            <p>Catégories</p>
          </div>
        </Link>
        <Link to="/orders" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.orders}</h2>
            <p>Commandes</p>
          </div>
        </Link>
        <Link to="/conversations" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.conversations}</h2>
            <p>Conversations</p>
          </div>
        </Link>
        <Link to="/users" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.users}</h2>
            <p>Utilisateurs</p>
          </div>
        </Link>
        <Link to="/customers" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.customers}</h2>
            <p>Clients</p>
          </div>
        </Link>
        <Link to="/notifications" className="stat-link">
          <div className="card stat-card">
            <h2>{counts.unreadNotifications}</h2>
            <p>Notifications non lues</p>
          </div>
        </Link>
      </div>
    </div>
  )
}

export default Dashboard
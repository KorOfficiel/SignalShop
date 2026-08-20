import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api'

function Login() {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin1234')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err: any) {
      console.error(err)
      if (err.response) {
        setError(`Erreur ${err.response.status}: ${JSON.stringify(err.response.data)}`)
      } else if (err.request) {
        setError('Aucune réponse du serveur. Vérifiez que le backend est démarré.')
      } else {
        setError(`Erreur: ${err.message}`)
      }
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-logo">🛒</div>
        <h1>SignalShop</h1>
        <p className="login-subtitle">Espace professionnel</p>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="alert-error">{error}</p>}
          <button type="submit" className="btn btn-block">Se connecter</button>
        </form>
      </div>
    </div>
  )
}

export default Login
import { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

interface Message {
  id: string
  sender: string
  timestamp: string
  content?: string | null
}

interface Conversation {
  id: string
  customer_id: string
  state: string
  timer_expires_at?: string | null
  created_at: string
  updated_at: string
  closed: boolean
}

function Conversations() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const fetchConversations = async () => {
    setLoading(true)
    try {
      const response = await api.get('/conversations')
      setConversations(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur chargement conversations : ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchConversations()
  }, [])

  const fetchMessages = async (conversationId: string) => {
    try {
      const response = await api.get(`/conversations/${conversationId}/messages`)
      setMessages(response.data)
    } catch (err: any) {
      console.error(err)
      setError(`Erreur chargement messages : ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleSelect = (id: string) => {
    setSelectedId(id)
    setError('')
    setSuccess('')
    fetchMessages(id)
  }

  const handleAction = async (conversationId: string, action: 'handoff' | 'ai-resume' | 'stop-ai' | 'close') => {
    setError('')
    setSuccess('')
    try {
      await api.post(`/conversations/${conversationId}/${action}`)
      setSuccess(`Action "${action}" effectuée.`)
      fetchConversations()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur action : ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleSendMessage = async (conversationId: string) => {
    if (!newMessage.trim()) return
    setError('')
    setSuccess('')
    try {
      await api.post(`/conversations/${conversationId}/message`, { body: newMessage })
      setSuccess('Message envoyé.')
      setNewMessage('')
      fetchMessages(conversationId)
      fetchConversations()
    } catch (err: any) {
      console.error(err)
      setError(`Erreur envoi : ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent, conversationId: string) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage(conversationId)
    }
  }

  if (loading) return <p>Chargement...</p>

  return (
    <div>
      <h1>Conversations</h1>
      <nav>
        <Link to="/dashboard">Retour</Link>
      </nav>
      {error && <p className="alert-error">{error}</p>}
      {success && <p className="alert-success">{success}</p>}

      <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: 250 }}>
          <h3>Liste des conversations</h3>
          <table>
            <thead>
              <tr><th>ID</th><th>État</th><th>Client</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {conversations.map((conv) => (
                <tr key={conv.id}>
                  <td>{conv.id.slice(0, 8)}...</td>
                  <td>{conv.state}</td>
                  <td>{conv.customer_id}</td>
                  <td><button className="btn btn-sm" onClick={() => handleSelect(conv.id)}>Voir</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {selectedId && (
          <div style={{ flex: 2 }}>
            <h3>Conversation {selectedId.slice(0, 8)}</h3>
            <div style={{ border: '1px solid #ccc', borderRadius: 8, padding: 10, minHeight: 300, maxHeight: 400, overflowY: 'auto', background: '#fafafa' }}>
              {messages.length === 0 ? (
                <p>Aucun message.</p>
              ) : (
                messages.map((msg) => (
                  <div key={msg.id} style={{ marginBottom: 10, textAlign: msg.sender === 'professional' ? 'right' : 'left' }}>
                    <div style={{ display: 'inline-block', background: msg.sender === 'professional' ? '#2563eb' : '#e5e7eb', color: msg.sender === 'professional' ? 'white' : 'black', padding: '8px 12px', borderRadius: 12 }}>
                      <strong>{msg.sender}: </strong> {msg.content || '(contenu masqué)'}
                    </div>
                    <div style={{ fontSize: 10, color: '#666' }}>{new Date(msg.timestamp).toLocaleTimeString('fr-FR')}</div>
                  </div>
                ))
              )}
            </div>
            <div style={{ display: 'flex', gap: 10, marginTop: 10 }}>
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={(e) => handleKeyPress(e, selectedId)}
                style={{ flex: 1 }}
                placeholder="Écrivez votre message et appuyez sur Entrée..."
              />
              <button className="btn" onClick={() => handleSendMessage(selectedId)}>Envoyer</button>
            </div>
            <div style={{ marginTop: 10, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <button className="btn" onClick={() => handleAction(selectedId, 'handoff')}>Prendre la main</button>
              <button className="btn" onClick={() => handleAction(selectedId, 'ai-resume')}>Repasser à l'IA</button>
              <button className="btn btn-danger" onClick={() => handleAction(selectedId, 'stop-ai')}>Stop IA</button>
              <button className="btn btn-danger" onClick={() => handleAction(selectedId, 'close')}>Fermer</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Conversations
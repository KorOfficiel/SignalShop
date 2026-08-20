import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

interface Notification {
  id: string
  type: string
  message: string
  read: boolean
  created_at: string
}

function NotificationCenter() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [toasts, setToasts] = useState<Notification[]>([])
  const [soundEnabled, setSoundEnabled] = useState(true)
  const audioContextRef = useRef<AudioContext | null>(null)

  const playBeep = () => {
    if (!audioContextRef.current) {
      audioContextRef.current = new AudioContext()
    }
    const ctx = audioContextRef.current
    const oscillator = ctx.createOscillator()
    const gainNode = ctx.createGain()
    oscillator.connect(gainNode)
    gainNode.connect(ctx.destination)
    oscillator.type = 'sine'
    oscillator.frequency.value = 880
    gainNode.gain.setValueAtTime(0.3, ctx.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5)
    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + 0.5)
  }

  // Récupérer le paramètre sonore
  useEffect(() => {
    const fetchSoundSetting = async () => {
      try {
        const response = await api.get('/settings')
        if (response.data.sound_enabled !== undefined) {
          setSoundEnabled(response.data.sound_enabled)
        }
      } catch (err) {
        console.error(err)
      }
    }
    fetchSoundSetting()
  }, [])

  // Polling des notifications non lues toutes les 30 secondes
  useEffect(() => {
    const pollNotifications = async () => {
      try {
        const response = await api.get('/notifications?unread_only=true')
        const newNotifications: Notification[] = response.data

        setNotifications((prev) => {
          const prevIds = new Set(prev.map((n) => n.id))
          const added = newNotifications.filter((n) => !prevIds.has(n.id))
          if (added.length > 0) {
            setToasts((prevToasts) => [...prevToasts, ...added])
            if (soundEnabled) {
              playBeep()
            }
          }
          return newNotifications
        })
      } catch (err) {
        console.error(err)
      }
    }

    pollNotifications()
    const interval = setInterval(pollNotifications, 30000)
    return () => clearInterval(interval)
  }, [soundEnabled])

  // Supprimer un toast après 5 secondes
  useEffect(() => {
    if (toasts.length === 0) return
    const timer = setTimeout(() => {
      setToasts((prev) => prev.slice(1))
    }, 5000)
    return () => clearTimeout(timer)
  }, [toasts])

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className="toast">
          <strong>{toast.type}</strong>
          <p>{toast.message}</p>
        </div>
      ))}
    </div>
  )
}

export default NotificationCenter
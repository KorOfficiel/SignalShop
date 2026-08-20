import { Link } from 'react-router-dom'
import InstallPWA from './InstallPWA'

const features = [
  { icon: '📦', title: 'Catalogue intelligent', desc: 'Gérez produits, variantes, options et stocks en quelques clics.' },
  { icon: '🧾', title: 'Commandes automatisées', desc: 'Suivez les commandes et changez les statuts facilement.' },
  { icon: '💬', title: 'Conversations Signal', desc: 'Répondez à vos clients directement depuis le dashboard.' },
  { icon: '📊', title: 'Statistiques claires', desc: 'Visualisez votre chiffre d\'affaires et vos meilleures ventes.' },
  { icon: '🔔', title: 'Notifications temps réel', desc: 'Soyez alerté des nouveaux événements instantanément.' },
  { icon: '👥', title: 'Multi-utilisateurs', desc: 'Créez des rôles et gérez les permissions par employé.' },
]

function Landing() {
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a, #1e3a8a, #3b82f6)', fontFamily: 'Inter, Segoe UI, sans-serif', overflow: 'hidden' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto', padding: 20 }}>
        {/* Hero */}
        <header style={{ textAlign: 'center', padding: '60px 0' }}>
          <div style={{ fontSize: 70, animation: 'float 3s ease-in-out infinite' }}>🛒</div>
          <h1 style={{ fontSize: '3rem', margin: '10px 0', color: 'white', fontWeight: 800, letterSpacing: '-1px' }}>
            SignalShop
          </h1>
          <p style={{ fontSize: 1.2rem, color: '#cbd5e1', maxWidth: 600, margin: '0 auto' }}>
            Votre assistant commercial intelligent, directement dans Signal.
          </p>
          <div style={{ marginTop: 30, display: 'flex', gap: 15, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link
              to="/install"
              style={{ background: '#2563eb', color: 'white', padding: '14px 28px', borderRadius: 30, textDecoration: 'none', fontWeight: 600, boxShadow: '0 10px 25px rgba(37,99,235,0.5)' }}
            >
              Télécharger l'application
            </Link>
            <Link
              to="/login"
              style={{ background: '#16a34a', color: 'white', padding: '14px 28px', borderRadius: 30, textDecoration: 'none', fontWeight: 600, boxShadow: '0 10px 25px rgba(22,163,74,0.5)' }}
            >
              Accéder au dashboard
            </Link>
          </div>
          <div style={{ marginTop: 20 }}>
            <InstallPWA />
          </div>
        </header>

        {/* Features */}
        <section style={{ padding: '40px 0' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 20 }}>
            {features.map((feature, idx) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', borderRadius: 20, padding: 30, textAlign: 'center', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ fontSize: 40 }}>{feature.icon}</div>
                <h3 style={{ color: 'white', margin: '10px 0' }}>{feature.title}</h3>
                <p style={{ color: '#cbd5e1' }}>{feature.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* How it works */}
        <section style={{ padding: '40px 0', textAlign: 'center' }}>
          <h2 style={{ color: 'white', fontSize: '2rem' }}>Comment ça marche ?</h2>
          <div style={{ display: 'flex', gap: 20, justifyContent: 'center', flexWrap: 'wrap', marginTop: 30 }}>
            {['1. Installez le dashboard', '2. Configurez vos produits', '3. Recevez les commandes via Signal'].map((step, i) => (
              <div key={i} style={{ background: 'rgba(255,255,255,0.05)', borderRadius: 20, padding: 25, flex: 1, minWidth: 220, border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ fontSize: 24, color: '#fbbf24' }}>Étape {i+1}</div>
                <p style={{ color: '#e2e8f0', marginTop: 10 }}>{step}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Footer */}
        <footer style={{ padding: '30px 0', textAlign: 'center', color: '#94a3b8' }}>
          <p>© 2026 SignalShop — Version MVP open source.</p>
        </footer>
      </div>

      <style>{`
        @keyframes float {
          0%,100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
      `}</style>
    </div>
  )
}

export default Landing
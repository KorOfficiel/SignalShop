import { Link } from 'react-router-dom'

function InstallPage() {
  return (
    <div className="container" style={{ textAlign: 'center', paddingTop: 50 }}>
      <h1>Installer SignalShop</h1>
      <p style={{ fontSize: 18, marginBottom: 30 }}>
        Transformez ce site en application sur votre appareil.
      </p>

      <div style={{ maxWidth: 400, margin: '0 auto', textAlign: 'left' }}>
        <h2>📱 Android (Chrome)</h2>
        <ol>
          <li>Ouvrez le menu ⋮ en haut à droite.</li>
          <li>Choisissez <strong>Installer l'application</strong>.</li>
          <li>Validez.</li>
        </ol>

        <h2>🍎 iPhone / iPad (Safari)</h2>
        <ol>
          <li>Appuyez sur le bouton <strong>Partager</strong>.</li>
          <li>Faites défiler et sélectionnez <strong>Sur l'écran d'accueil</strong>.</li>
          <li>Validez.</li>
        </ol>

        <h2>💻 Ordinateur (Chrome/Edge)</h2>
        <ol>
          <li>Ouvrez le menu ⋮ ou ⋯.</li>
          <li>Choisissez <strong>Installer SignalShop…</strong>.</li>
        </ol>
      </div>

      <Link to="/dashboard" className="btn" style={{ marginTop: 30 }}>
        Retour au tableau de bord
      </Link>
    </div>
  )
}

export default InstallPage
20_MONITORING.md
1. Supervision
Composant
Indicateurs
Serveur
CPU, RAM, disque
Base
Connexions, requêtes lentes, espace
Signal
État du compte service et professionnel, flux d’événements
Backend
Latence, erreurs, santé
Queue
Taille, erreurs, retries
IA
Latence, erreurs fournisseur

2. Health checks
Chaque composant critique expose un état.
États : HEALTHY, DEGRADED, DOWN.
Tableau de bord système affiche ces états.
3. Alertes
Signal down.
Backend down.
Database down.
Disque presque plein.
Mémoire élevée.
Erreurs répétées.
IA indisponible.
Queue bloquée.
4. Logs
Logs techniques structurés.
Pas de données personnelles.
Correlation ID pour relier événements.
Journal d’audit pour actions administratives.
5. Tests
Alertes simulées.
Health checks.
Logs sans données personnelles.
Correlation ID.

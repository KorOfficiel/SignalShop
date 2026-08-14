19_DEPLOYMENT.md
1. Environnement cible
Serveur Linux VPS unique.
Docker Compose pour l’orchestration.
Reverse proxy Nginx ou Caddy.
Services : backend, frontend, PostgreSQL, Redis, Signal Adapter, monitoring.
2. Configuration
Secrets et variables techniques dans .env.
Paramètres métier dans la base, gérés par dashboard.
Jamais de clés dans le code.
3. Environnements
development : local, conteneurisé.
testing : base jetable, données fictives.
production : VPS.
4. Mise à jour
Sauvegarde.
Déploiement de la nouvelle version.
Migrations de base.
Tests santé.
Validation production.
Rollback si problème.
5. Rollback
Version précédente disponible.
Restauration de la sauvegarde si nécessaire.
Health check après rollback.
6. Reprise automatique
Services configurés pour redémarrer automatiquement après crash.
Éviter boucles infinies de redémarrage.
Supervision des états.
7. Tests
Déploiement sur VPS.
Mise à jour.
Rollback.
Restauration de sauvegarde.
Démarrage après redémarrage serveur.

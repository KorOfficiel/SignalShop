24_DEVELOPER_GUIDE.md
1. Objectif
Documentation technique pour installation, développement, tests, déploiement et maintenance.
2. Environnement
Docker Compose.
Services : backend, frontend, base, Redis, signal-adapter.
Variables d’environnement pour secrets.
3. Développement
Branches Git : main, develop, feature.
Chaque modification doit être documentée et testée.
Exécuter tests avant merge.
Ne jamais casser les modules existants.
4. Architecture
Backend FastAPI.
Frontend React.
Signal Adapter isolé.
Tool Gateway pour l’IA.
PostgreSQL source de vérité.
5. Tests
Lancer les tests unitaires, intégration, API.
Tests de concurrence.
Tests sécurité.
Tests suppression.
6. Déploiement
Suivre la procédure : backup → deploy → migration → tests → health check.
Rollback possible.
Vérifier les logs et métriques.
7. Maintenance
Sauvegardes régulières.
Restaurations testées.
Purge automatique.
Mise à jour des dépendances.
8. Troubleshooting
Documenter : IA ne répond plus, Signal ne reçoit plus, dashboard inaccessible, commande bloquée, créneau incorrect, stock incorrect.

22_DISASTER_RECOVERY.md
1. Sauvegardes
PostgreSQL sauvegardé régulièrement.
Sauvegardes chiffrées.
Conservation alignée sur politique de confidentialité.
Restauration testée régulièrement.
2. Restauration
Procédure documentée.
Restauration de la base et des secrets.
Purge post-restauration des données supprimées.
Health check.
3. Pannes
Panne
Comportement
Signal
File d’attente, retries, alerte
IA
Informer client, proposer humain
Base
État sécurisé, pas de confirmation sans persistance
Redis
Pas de perte de données critiques
Serveur
Redémarrage automatique

4. RTO/RPO
Objectif : RPO minimal pour commandes confirmées.
Aucune perte incohérente de commande.
RTO raisonnable pour VPS unique.
5. Tests
Sauvegarde → restauration → validation.
Panne Signal.
Panne IA.
Panne base.
Redémarrage.

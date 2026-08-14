14_SECURITY.md

1. Authentification dashboard
Email + mot de passe.
Mots de passe hachés avec algorithme sûr.
Sessions avec expiration.
Déconnexion.
Protection contre brute-force.
MFA optionnelle.
JWT pour API dashboard.
2. Autorisation
Rôles : OWNER, ADMIN, MANAGER, STAFF.
Chaque route API vérifie le rôle et l’appartenance au tenant.
Toute requête est filtrée par tenant_id et selon le contexte customer_id.


Permission
OWNER
ADMIN
MANAGER
STAFF
Voir commandes
✅
✅
✅
✅
Modifier statut commande
✅
✅
✅
✅
Gérer catalogue
✅
✅
✅
❌
Modifier prix
✅
✅
✅
❌
Supprimer données
✅
✅
❌
❌
Gérer utilisateurs
✅
✅
❌
❌
Paramètres système
✅
✅
❌
❌
Répondre aux clients
✅
✅
✅
✅
Voir conversations
✅
✅
✅
✅
Prendre la main
✅
✅
✅
✅



3. Isolation
Un client ne peut jamais accéder aux données d’un autre client.
Un tenant ne peut jamais voir les données d’un autre tenant.
Les requêtes croisées sont interdites.
L’IA ne peut pas contourner cette isolation.
4. Secrets
Aucun secret dans Git.
Utilisation de variables d’environnement ou coffre.
Clés API IA, signal-cli, base, Redis externalisées.
Rotation possible.
5. Chiffrement
Données sensibles au repos chiffrées : adresses, contenus conversation si conservés.
Les sauvegardes sont chiffrées.
Les clés de chiffrement sont protégées.
6. Logs
Aucune donnée personnelle dans les logs.
Aucune conversation complète, adresse, numéro, token.
Logs techniques : identifiant d’événement, service, horodatage, sévérité.
7. Validation des entrées
Toute entrée est validée.
Ne jamais faire confiance au client, dashboard, IA, Signal ou requête HTTP.
Rejet des formats invalides, longueurs excessives.
8. Prompt injection
L’IA doit refuser les instructions malveillantes.
Les permissions sont contrôlées backend.
Les outils ne permettent que les actions autorisées.
Exemple : un client ne peut pas obtenir la liste des commandes.
9. Actions sensibles
Suppression massive, modification globale, paramètres système demandent validation explicite.
Journal d’audit enregistre qui a fait quoi, sans données personnelles.
10. Tests de sécurité
Authentification, autorisation, injections SQL/API.
Accès croisé tenant/client.
Fuite de données.
Secrets exposés.
Prompt injection simulée.
Brute force.
Session expirée.

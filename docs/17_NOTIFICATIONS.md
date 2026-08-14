17_NOTIFICATIONS.md
1. Événements notifiables
Nouvelle commande.
Commande modifiée.
Commande annulée.
Problème IA.
Client demande un humain.
Stock faible.
Créneau complet.
Erreur système.
Serveur indisponible.
Paiement si ajouté ultérieurement.
2. Canaux
Dashboard.
Signal professionnel.
Email futur possible.
3. Configuration
Instantané, résumé, silencieux.
Choix du canal par type d’événement.
Anti-spam : ne pas notifier des dizaines de fois le même événement.
Règle anti-spam MVP : les notifications instantanées sont envoyées immédiatement, mais si le même type d’événement se produit plusieurs fois en moins de 5 minutes, un seul message récapitulatif est envoyé. 
4. Contenu
Notifications concises et actionnables.
Exemple : « Nouvelle commande #1048 — 42 € — 19h00. »
Aucune donnée personnelle inutile.
Aucun message client complet.
5. Fiabilité
Les notifications échouées sont retentées.
Fallback dashboard si Signal indisponible.
Corrélation par identifiant d’événement.
6. Tests
Nouvelle commande notifiée.
Stock faible.
Demande humaine.
Panne Signal pendant notification.
Configuration anti-spam.

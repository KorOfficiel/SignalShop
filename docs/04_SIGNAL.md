04_SIGNAL.md
1. Rôle de Signal
Signal est le canal client unique. Le système ne doit jamais mélanger Signal avec la logique métier. Toute l’intégration est encapsulée dans un Signal Adapter.
2. Comptes Signal
2.1 Compte service clients
Numéro distinct dédié aux échanges avec les clients.
C’est ce numéro que les clients contactent.
Le système écoute les messages entrants sur ce compte.
2.2 Compte professionnel
Numéro distinct utilisé uniquement pour les notifications professionnelles. Il ne permet pas d’intervenir dans les conversations pour le MVP. Ce numéro est whitelisté dans la configuration. 
2.3 Changement de numéro
Le professionnel peut changer les numéros via une procédure de liaison.
Le système doit permettre de relier un nouveau numéro sans bloquer l’activité.
Une vérification est requise avant activation.
3. Intégration technique
Utilisation de signal-cli comme projet tiers non officiel.
L’adapter consomme les interfaces JSON-RPC, daemon HTTP et flux SSE.
La dépendance est isolée, versionnée, surveillée et testée.
Aucun autre composant ne communique directement avec signal-cli.
4. Liaison du compte
Préparer un compte service ou professionnel.
Lancer la procédure de liaison via l’adapter.
Afficher ou transmettre le QR code nécessaire.
Valider le code de vérification éventuel.
Tester l’envoi et la réception.
Activer le numéro dans la configuration.
5. Réception des messages
Le Signal Adapter détecte un message entrant.
Il génère un événement interne avec identifiant unique du message.
Il publie cet événement sur le Message Bus.
Un worker traite l’événement de manière idempotente.
Le Message Processor identifie la conversation et l’état.
6. Envoi des messages
Toute réponse passe par le Signal Adapter.
L’adapter vérifie l’état du compte signal.
En cas d’échec, le message est conservé dans une file d’erreur.
Les retries sont contrôlés avec délais et limites.
7. Erreurs et pannes
Événement
Comportement
Signal indisponible
Mise en file, retries contrôlés, notification professionnel si seuil dépassé
Message mal formé
L’adapter ignore ou journalise sans contenu personnel
Fichier multimédia non supporté
Message client indiquant que seuls les textes sont acceptés
Doublon
Idempotence par identifiant de message
Changement de numéro
Procédure de liaison, aucune perte de commande

8. Sécurité
Les secrets signal-cli ne sont jamais dans le code.
Les numéros sont traités comme données sensibles.
Les logs ne contiennent pas les messages ni numéros en clair.
L’accès à l’adapter est limité au backend.
9. Tests
Réception et envoi sur numéro service.
Réception sur numéro professionnel.
Liaison d’appareil.
Panne simulée et retry.
Doublons d’événements.
Rate limiting éventuel.
Changement de numéro.

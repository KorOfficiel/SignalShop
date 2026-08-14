15_PRIVACY.md
1. Principes
Minimisation des données.
Ne pas stocker une information simplement parce qu’elle est disponible.
Confidentialité par défaut.
Suppression possible et documentée.
Le professionnel choisit les conservations.
2. Catégories de données
Catégorie
Contenu
Conversationnelle
Messages échangés sur Signal
Comptable
Commandes, totaux, statuts
Adresse
Adresse de livraison
Client
Hash du numéro Signal
Technique
Logs, métriques, audit

3. Par défaut
Conversations : 30 jours.
Commandes : 1 an.
Adresses : supprimées après livraison.
Logs : sans données personnelles.
Les contenus de messages ne sont pas conservés en clair par défaut. Si le professionnel active la conservation des messages, ils sont chiffrés au repos et conservés 30 jours. 
4. Minimisation
L’IA ne reçoit qu’un contexte minimal.
Les logs ne contiennent ni message ni adresse.
Les données de session temporaires sont éphémères.
5. Suppression
Suppression d’un message.
Suppression d’une conversation.
Suppression d’un client.
Suppression d’un historique.
Suppression totale de toutes les données d’un client.
Les commandes comptables peuvent être conservées ou anonymisées selon politique.
6. Chiffrement
Les adresses et contenus conversationnels conservés sont chiffrés au repos.
Les clés sont hors de la base.
7. Cas limites
Suppression totale avec commandes en cours.
Suppression d’une conversation sans supprimer la commande comptable.
Purge post-restauration.
Sauvegardes ne doivent pas prolonger indéfiniment les données supprimées.
8. Tests
Suppression message, conversation, client, historique.
Suppression totale.
Vérification après redémarrage.
Vérification des logs sans données personnelles.

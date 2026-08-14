16_RETENTION.md
1. Politique de conservation
Donnée
Conservation
Métadonnées conversationnelles
30 jours par défaut
Messages bruts
non conservés par défaut ; si activé, conservés 30 jours chiffrés au repos. 
Commandes
1 an
Adresses
supprimées après livraison de toutes les commandes actives ou 30 jours après la dernière commande. 
Logs techniques
Durée courte, sans données personnelles
Sauvegardes
Chiffrées, durée alignée sur la politique

2. Purge automatique
Un service de purge identifie les données éligibles.
Supprime les données et nettoie les relations.
Nettoie les caches associés.
Produit uniquement des logs techniques nécessaires.
Respecte les règles de backup.
3. Suppression sélective
Le professionnel peut supprimer une conversation sans toucher à une commande comptable légitime.
Les références entre catégories de données sont distinguées.
4. Suppression totale
Fonction « Supprimer toutes les données de ce client ».
Identifie toutes les données liées par référence.
Applique les règles de suppression définies.
Les commandes comptables peuvent être anonymisées si conservation légale.
Pour le MVP, la suppression totale est bloquée tant qu’il existe une commande non terminée (statut différent de COMPLETED ou CANCELLED). 
5. Backups
Une sauvegarde ne doit pas conserver éternellement des données supprimées.
Après restauration, le service de purge doit purger les données redevenues éligibles.
Les restaurations sont testées régulièrement.
6. Tests
Purge automatique.
Suppression sélective.
Suppression totale.
Redémarrage après purge.
Restauration de backup contenant des données supprimées.

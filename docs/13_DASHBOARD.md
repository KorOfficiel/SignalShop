13_DASHBOARD.md
1. Objectif
Permettre au professionnel de tout gérer sans compétence technique. Interface web responsive, priorité mobile. Toutes les actions métier sont des formulaires et boutons simples.
2. Modules


Module
Fonctions
Accueil
Commandes du jour, en attente, en préparation, créneaux, stock faible, conversations humaines, alertes
Commandes
Liste, filtres, détail, changement de statut, notes internes
Conversations
Lecture, réponse, prise de main, arrêt/reprise IA, informations de commande. Par défaut, seules les métadonnées (dates, statuts, résumé) sont affichées. Le contenu des messages n’est visible que si la conservation des messages est activée dans les paramètres de confidentialité. 
Catalogue
Ajouter, modifier, désactiver, supprimer, dupliquer, réorganiser. Les images sont stockées localement dans un volume Docker (pas de S3 pour le MVP). 
Prix
Modification immédiate ou programmée
Stock
Consultation, ajustement, alertes
Créneaux
Calendrier, horaires, capacités, exceptions, fermeture/réouverture
Livraison
Zones, tarifs, minimum, activation
Notifications
Canaux, événements, résumés
Confidentialité
Politique de conservation, suppression sélective/totale
Utilisateurs
Rôles et permissions
Système
État des composants, santé, alertes

3. UX
Mobile-first : boutons grands, navigation simple.
PC : sidebar, tableaux.
Accessibilité : contrastes, taille texte, navigation clavier, messages d’erreur clairs.
Tous les textes sont séparés du code pour traduction future.
4. Permissions
Rôle
Peut
OWNER
Tout gérer, y compris utilisateurs et système
ADMIN
Gérer métier, utilisateurs, confidentialité
MANAGER
Gérer commandes, catalogue, conversations
STAFF
Voir commandes, répondre clients, modifier statut

Restrictions :
STAFF ne peut pas modifier paramètres système, API, supprimer toutes les données.
MANAGER ne peut pas changer secrets ou accès technique.
5. Erreurs
Toute erreur est affichée simplement.
Le professionnel ne voit jamais SQL, traceback, JSON.
Les actions sensibles demandent confirmation.
6. Tests
Navigation mobile.
Accès par rôle.
Création de produit, changement de prix, stock.
Prise de main conversation.
Affichage commande.
Notifications.

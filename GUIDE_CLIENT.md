# Guide d'utilisation de SignalShop

Bienvenue ! Ce guide vous explique comment installer, configurer et utiliser SignalShop, votre assistant commercial connecté à Signal.

---

## 1. Installation

### Prérequis
- Un PC Windows 10/11.
- Docker Desktop (téléchargeable gratuitement sur https://www.docker.com/products/docker-desktop).
- Git (https://git-scm.com/downloads).
- Python 3.12+ (https://www.python.org/downloads/).

### Étapes d'installation
1. Double-cliquez sur `install.bat`.
2. Suivez les instructions à l'écran :
   - Email administrateur (ex : `admin@example.com`)
   - Mot de passe administrateur (ex : `admin1234`)
   - Numéro de service Signal (laissez vide si vous n'en avez pas encore)
3. Le script va :
   - Créer le fichier `.env`.
   - Démarrer les services Docker (base de données, backend, frontend).
   - Initialiser la base de données.
   - Créer l'utilisateur administrateur.
4. Une fois terminé, ouvrez votre navigateur sur `http://localhost:3000`.
5. Connectez-vous avec l'email et le mot de passe choisis.

---

## 2. Démarrage et arrêt

### Démarrer
- Double-cliquez sur `start_system.bat`.

### Arrêter
- Double-cliquez sur `stop_system.bat`.

---

## 3. Utilisation du tableau de bord

### 3.1 Tableau de bord
La page d'accueil affiche des indicateurs : produits, commandes, clients, etc. Cliquez sur une carte pour accéder à la section correspondante.

### 3.2 Gérer les produits
- Allez dans **Produits**.
- Cliquez sur **Ajouter un produit**.
- Remplissez les champs : nom, description, prix en centimes, unité, stock, catégorie.
- Cliquez **Enregistrer**.

### 3.3 Gérer les catégories
- Allez dans **Catégories**.
- Ajoutez, modifiez ou supprimez des catégories.

### 3.4 Gérer les variantes et options
- Utilisez les pages **Variantes** et **Options** pour configurer des déclinaisons de produits (ex : tailles, parfums).

### 3.5 Gérer les commandes
- Allez dans **Commandes**.
- Pour créer une commande manuelle : **Nouvelle commande**.
- Sélectionnez le client, le produit, la quantité, le créneau et la zone de livraison.
- Cliquez **Créer la commande**.
- Pour changer le statut : ouvrez le détail de la commande et utilisez le menu déroulant.
- Pour annuler : **Annuler la commande**.
- Pour supprimer : **Supprimer définitivement**.

### 3.6 Gérer les clients
- Allez dans **Clients**.
- Ajoutez un client en renseignant son numéro Signal (ou un hash).
- Modifiez ou supprimez selon besoin.

### 3.7 Conversations
- Allez dans **Conversations**.
- Sélectionnez une conversation pour voir l'historique.
- Écrivez votre message et appuyez sur **Entrée** pour envoyer.
- Utilisez les boutons **Prendre la main**, **Repasser à l'IA**, **Stop IA**, **Fermer** pour gérer l'état.

> **Note** : Tant que vous n'avez pas pris la main, l'IA répond automatiquement aux clients.

### 3.8 Notifications
- Allez dans **Notifications** pour voir les événements (nouvelles commandes, stock faible, etc.).
- Marquez comme lu ou supprimez.

### 3.9 Évaluations
- Consultez et supprimez les évaluations clients (note sur 5 + commentaire).

### 3.10 Statistiques
- Visualisez le chiffre d'affaires, les commandes par jour et les produits les plus vendus.

### 3.11 Permissions
- Allez dans **Permissions** pour définir ce que chaque rôle (ADMIN, MANAGER, STAFF) peut faire.
- Cochez/décochez puis **Enregistrer**.

### 3.12 Paramètres
- Allez dans **Paramètres** pour :
  - Changer le nom de l'application.
  - Modifier le message d'accueil.
  - Choisir le ton (vouvoiement/tutoiement).
  - Renseigner le numéro de service Signal.
  - Activer/désactiver le son.

---

## 4. Installation sur mobile (PWA)

SignalShop peut être installé sur votre téléphone comme une application.

### Android (Chrome)
1. Ouvrez le dashboard dans Chrome.
2. Appuyez sur les **trois points** ⋮.
3. Choisissez **Installer l'application** (ou **Ajouter à l'écran d'accueil**).
4. Validez.

### iPhone (Safari)
1. Ouvrez le dashboard dans Safari.
2. Appuyez sur **Partager** (carré avec flèche).
3. Sélectionnez **Sur l'écran d'accueil**.
4. Validez.

---

## 5. Dépannage rapide

| Problème | Solution |
|----------|----------|
| Le site ne s'affiche pas | Vérifiez que Docker Desktop tourne et que les conteneurs sont actifs (`docker compose ps`). |
| Identifiants invalides | Réinitialisez le mot de passe avec `docker exec -it signalshop_backend python -m scripts.create_initial_user`. |
| L'IA ne répond pas | Assurez-vous qu'aucun humain n'a pris la main dans la conversation. |
| Les messages Signal ne partent pas | Vérifiez que le bridge est lancé et que le numéro de service est configuré dans Paramètres. |
| Le bridge ne démarre pas | Vérifiez que Python et signal-cli sont installés et que le numéro est valide. |

---

## 6. Support

Pour toute question, contactez votre administrateur technique.
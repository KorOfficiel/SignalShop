# Guide d'utilisation de SignalShop

Bienvenue dans votre espace professionnel SignalShop. Ce guide vous explique comment utiliser toutes les fonctionnalités de votre assistant commercial.

## Table des matières
1. Installation
2. Connexion au tableau de bord
3. Découvrir le tableau de bord
4. Gérer le catalogue
5. Gérer les commandes
6. Gérer les créneaux et la livraison
7. Gérer les clients
8. Gérer les conversations
9. Gérer les utilisateurs et les permissions
10. Notifications
11. Statistiques
12. Paramètres
13. Dépannage rapide

---

## 1. Installation

Pour installer SignalShop sur votre ordinateur, suivez ces étapes :

### Prérequis
- Avoir un PC Windows ou Linux.
- Avoir Docker Desktop installé (téléchargeable sur https://www.docker.com/products/docker-desktop).
- Avoir Git installé (https://git-scm.com/downloads).

### Étapes d'installation
1. Double-cliquez sur le fichier `install.bat` (Windows) ou exécutez `install.sh` (Linux).
2. Le script vérifie Docker et Git.
3. Il vous demande l'email et le mot de passe administrateur (par défaut : `admin@example.com` / `admin1234`).
4. Le script crée le fichier `.env` et lance les services.
5. Une fois terminé, le tableau de bord est accessible sur `http://localhost:3000`.

---

## 2. Connexion au tableau de bord

1. Ouvrez votre navigateur (Chrome ou Edge recommandé).
2. Allez sur `http://localhost:3000`.
3. Entrez l'email administrateur et le mot de passe définis lors de l'installation.
4. Cliquez sur **Se connecter**.

---

## 3. Découvrir le tableau de bord

Le tableau de bord se compose de :
- **Barre latérale** : les différents modules (Produits, Commandes, etc.).
- **En-tête** : le nom de l'application et le bouton de déconnexion.
- **Contenu principal** : les informations du module sélectionné.

Sur mobile, la barre latérale se replie ; utilisez le bouton ☰ pour la faire apparaître.

---

## 4. Gérer le catalogue

### Catégories
- Allez dans **Catégories**.
- Cliquez sur **Ajouter une catégorie**.
- Remplissez le nom, la description, la position.
- Cliquez sur **Enregistrer**.

### Produits
- Allez dans **Produits**.
- Cliquez sur **Ajouter un produit**.
- Remplissez le nom, la description, le prix (en centimes : 1400 = 14 €), l'unité, le mode de stock, la quantité, la catégorie (liste déroulante).
- Cliquez sur **Enregistrer**.

### Variantes et Options
Vous pouvez ajouter des variantes (ex : Chocolat Noir, Lait, Blanc) et des options (ex : taille, emballage) via les menus correspondants.

---

## 5. Gérer les commandes

- Allez dans **Commandes**.
- Vous voyez la liste des commandes avec leur statut.
- Cliquez sur **Détails** pour voir les articles et modifier le statut.
- Utilisez **Annuler la commande** pour annuler (libère le stock et le créneau).
- Utilisez **Supprimer définitivement** pour effacer la commande.

### Créer une commande manuellement
- Cliquez sur **Nouvelle commande**.
- Sélectionnez le client, le créneau de livraison (optionnel), la zone de livraison (optionnel).
- Ajoutez un ou plusieurs articles (produit + quantité).
- Cliquez sur **Créer la commande**.

---

## 6. Gérer les créneaux et la livraison

### Créneaux
- Allez dans **Créneaux**.
- Cliquez sur **Ajouter un créneau**.
- Définissez le début, la fin, la capacité.
- Enregistrez.

### Zones de livraison
- Allez dans **Livraison**.
- Ajoutez une zone avec son nom, ses frais, son minimum.
- Activez/désactivez selon besoin.

---

## 7. Gérer les clients

- Allez dans **Clients**.
- Ajoutez un client en renseignant son numéro Signal (sous forme de hash pour l'instant).
- Modifiez ou supprimez des clients.

---

## 8. Gérer les conversations

- Allez dans **Conversations**.
- Sélectionnez une conversation dans la liste.
- Visualisez l'historique des messages.
- Envoyez un message en tapant et en appuyant sur **Entrée** ou sur le bouton **Envoyer**.
- Utilisez les boutons **Prendre la main**, **Repasser à l'IA**, **Stop IA**, **Fermer** selon la situation.

> **Note** : Tant que vous n'avez pas pris la main, l'IA répond automatiquement aux clients. Quand vous prenez la main, l'IA se tait.

---

## 9. Gérer les utilisateurs et les permissions

### Utilisateurs
- Allez dans **Utilisateurs**.
- Ajoutez des comptes pour vos employés (STAFF, MANAGER, etc.).
- Modifiez leurs informations ou supprimez-les.

### Permissions
- Allez dans **Permissions**.
- Cochez/décochez les permissions pour chaque rôle.
- Enregistrez.

---

## 10. Notifications

- Allez dans **Notifications** pour voir la liste des événements (nouvelles commandes, stock faible, etc.).
- Marquez-les comme lues ou tout marquer comme lu.

---

## 11. Statistiques

- Allez dans **Statistiques**.
- Consultez le chiffre d'affaires, les commandes par jour et les produits les plus vendus.

---

## 12. Paramètres

- Allez dans **Paramètres**.
- Changez le nom de l'application, le message d'accueil, le ton (vouvoiement/tutoiement), activez/désactivez le son.
- Enregistrez.

---

## 13. Dépannage rapide

| Problème | Solution |
|----------|----------|
| Le dashboard ne s'affiche pas | Vérifiez que Docker tourne et que le conteneur frontend est actif (`docker compose ps`). |
| Impossible de se connecter | Vérifiez l'email et le mot de passe. Si oubli, exécutez le script de création d'utilisateur initial. |
| L'IA ne répond pas | Assurez-vous d'être en état `AI_ACTIVE` dans la conversation. Si un humain a pris la main, l'IA est en pause. |
| Stock faible | Une notification est créée ; ajustez le stock dans Produits. |
| Les commandes ne passent pas | Vérifiez la capacité du créneau et le stock disponible. |
| Le tunnel Cloudflare ne marche pas | Relancez `cloudflared tunnel --url http://localhost:3000` et gardez la fenêtre ouverte. |

---

## Support

Pour toute question, contactez votre administrateur technique.
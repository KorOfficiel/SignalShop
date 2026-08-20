# Guide d'utilisation de SignalShop

Bienvenue ! Ce guide vous explique comment installer, configurer et utiliser SignalShop, votre assistant commercial connecté à Signal.

---

## 1. Installation simplifiée

### Méthode 1 : Utiliser l'installateur graphique (recommandé)
1. Double-cliquez sur `SignalShop_Installer.exe`.
2. Remplissez les champs (email, mot de passe, numéro Signal).
3. Cliquez sur **Installer**.
4. Attendez la fin de l'installation.
5. Ouvrez votre navigateur sur `http://localhost:3000`.

### Méthode 2 : Utiliser le script batch
1. Double-cliquez sur `install.bat`.
2. Suivez les instructions.
3. Ouvrez `http://localhost:3000`.

---

## 2. Démarrage et arrêt

### Démarrer
- Double-cliquez sur `start_system.bat`.

### Arrêter
- Double-cliquez sur `stop_system.bat`.

---

## 3. Utilisation du tableau de bord

### 3.1 Tableau de bord
La page d'accueil affiche des indicateurs. Cliquez sur une carte pour accéder à la section.

### 3.2 Gérer les produits
- Allez dans **Produits**.
- Cliquez sur **Ajouter un produit**.
- Remplissez et enregistrez.

### 3.3 Gérer les catégories
- Allez dans **Catégories**.
- Ajoutez/modifiez/supprimez.

### 3.4 Gérer les variantes et options
- Utilisez les pages correspondantes.

### 3.5 Gérer les commandes
- Allez dans **Commandes**.
- **Nouvelle commande** pour créer manuellement.
- Changez statut, annulez, supprimez.

### 3.6 Gérer les clients
- Allez dans **Clients**.

### 3.7 Conversations
- Allez dans **Conversations**.
- Sélectionnez une conversation, envoyez un message.

### 3.8 Notifications
- Allez dans **Notifications**.

### 3.9 Évaluations
- Consultez/supprimez.

### 3.10 Statistiques
- Visualisez CA, commandes par jour, top produits.

### 3.11 Permissions
- Allez dans **Permissions**.

### 3.12 Paramètres
- Changez nom, message, ton, numéro Signal, son.

---

## 4. Installation sur mobile (PWA)

### Android (Chrome)
1. Ouvrez le dashboard.
2. Menu ⋮ → **Installer l'application**.

### iPhone (Safari)
1. Bouton Partager → **Sur l'écran d'accueil**.

---

## 5. Dépannage rapide

| Problème | Solution |
|----------|----------|
| Le site ne s'affiche pas | Vérifiez Docker Desktop et les conteneurs. |
| Identifiants invalides | Réinitialisez avec `docker exec -it signalshop_backend python -m scripts.create_initial_user`. |
| L'IA ne répond pas | Vérifiez qu'aucun humain n'a pris la main. |
| Messages Signal ne partent pas | Vérifiez que le bridge est lancé. |

---

## 6. Support

Contactez votre administrateur technique.
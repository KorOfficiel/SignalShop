# Déployer SignalShop sur un VPS (24/7)

Ce guide explique comment installer SignalShop sur un serveur VPS Ubuntu pour un fonctionnement permanent, même quand votre PC est éteint.

## 1. Achetez un VPS
- Choisissez Ubuntu 22.04 ou 24.04.
- 2 Go RAM minimum recommandé.
- Notez l'adresse IP du serveur.

## 2. Connectez-vous en SSH
Ouvrez un terminal (PowerShell, cmd, ou terminal Linux/macOS) et tapez :

ssh root@IP_DU_SERVEUR

## 3. Téléchargez le script d'installation
wget https://raw.githubusercontent.com/KorOfficiel/SignalShop/main/deploy_vps.sh

## 4. Lancez le script
bash deploy_vps.sh

## 5. Suivez les instructions
Le script vous demandera :
- Email administrateur
- Mot de passe administrateur
- Domaine (ex: monsite.com)
- Clé de chiffrement (vous pouvez appuyer sur Entrée pour générer automatiquement)
- Phrase secrète pour les sauvegardes
- Numéro Signal de service (peut être vide)

## 6. Accédez à votre dashboard
Ouvrez https://votre-domaine.com
Connectez-vous avec l'email et le mot de passe choisis.

C'est tout ! Le service tourne 24/7.
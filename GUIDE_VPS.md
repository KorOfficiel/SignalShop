# Déployer SignalShop sur un VPS (24/7)

Suivez ces 5 étapes simples.

## 1. Achetez un VPS
- Choisissez Ubuntu 22.04 ou 24.04.
- 2 Go RAM minimum.
- Prenez note de l'adresse IP.

## 2. Connectez-vous en SSH
- Windows : utilisez PowerShell ou PuTTY.
- Mac/Linux : terminal.

Tapez :
ssh root@IP_DU_SERVEUR

## 3. Téléchargez le script
wget https://raw.githubusercontent.com/KorOfficiel/SignalShop/main/deploy_vps.sh

## 4. Lancez le script
bash deploy_vps.sh

Le script vous posera des questions. Répondez simplement.

## 5. Accédez à votre dashboard
Ouvrez https://votre-domaine.com
Connectez-vous avec l'email et le mot de passe choisis.

C'est tout ! Le service tourne 24/7.
#!/bin/bash
set -e

echo "==========================================="
echo " SignalShop - Déploiement VPS automatique"
echo "==========================================="
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "Installation de Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

# Vérifier Git
if ! command -v git &> /dev/null; then
    echo "Installation de Git..."
    apt update && apt install -y git
fi

# Demander les informations
read -p "Email administrateur: " ADMIN_EMAIL
read -p "Mot de passe administrateur: " ADMIN_PASSWORD
read -p "Votre domaine (ex: monsite.com): " DOMAIN
read -p "Clé de chiffrement (appuyez sur Entrée pour générer): " ENCRYPTION_KEY
if [ -z "$ENCRYPTION_KEY" ]; then
    ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
fi
read -p "Phrase secrète pour sauvegardes: " BACKUP_PASSPHRASE
read -p "Numéro Signal de service (peut être vide): " SIGNAL_SERVICE_PHONE

# Générer des secrets forts
POSTGRES_PASSWORD=$(openssl rand -base64 16)
SECRET_KEY=$(openssl rand -base64 32)

# Cloner le dépôt
git clone https://github.com/KorOfficiel/SignalShop.git SignalShop
cd SignalShop

# Créer .env
cat > .env <<EOF
POSTGRES_USER=signaluser
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=signal_shop
DATABASE_URL=postgresql://signaluser:$POSTGRES_PASSWORD@db:5432/signal_shop
REDIS_URL=redis://redis:6379/0
SECRET_KEY=$SECRET_KEY
BACKEND_PORT=8000
FRONTEND_PORT=3000
ADMIN_EMAIL=$ADMIN_EMAIL
ADMIN_PASSWORD=$ADMIN_PASSWORD
SIGNAL_SERVICE_PHONE=$SIGNAL_SERVICE_PHONE
ENCRYPTION_KEY=$ENCRYPTION_KEY
BACKUP_PASSPHRASE=$BACKUP_PASSPHRASE
DOMAIN=$DOMAIN
EOF

# Configurer Caddy avec le domaine
sed -i "s/ton-domaine.com/$DOMAIN/g" docker/Caddyfile

# Déployer
docker compose --env-file .env -f docker/docker-compose.prod.yml up -d --build

# Cron de sauvegarde quotidienne
(crontab -l 2>/dev/null; echo "0 3 * * * cd $PWD && bash src/backend/scripts/backup.sh") | crontab -

echo ""
echo "==========================================="
echo " Déploiement terminé !"
echo " Accédez à : https://$DOMAIN"
echo " Email admin : $ADMIN_EMAIL"
echo " Mot de passe : $ADMIN_PASSWORD"
echo "==========================================="
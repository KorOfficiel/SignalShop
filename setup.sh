#!/bin/bash
set -e

echo "=========================================="
echo " Installation de SignalShop sur Linux"
echo "=========================================="

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé. Installation..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

# Vérifier Git
if ! command -v git &> /dev/null; then
    apt update && apt install -y git
fi

# Cloner le dépôt
git clone https://github.com/KorOfficiel/SignalShop.git
cd SignalShop

# Configurer .env
cp .env.example .env
read -p "Email admin [admin@example.com]: " ADMIN_EMAIL
ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}
read -p "Mot de passe admin [admin1234]: " ADMIN_PASSWORD
ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin1234}
read -p "Numéro Signal (vide si pas encore): " SIGNAL_PHONE

sed -i "s/ADMIN_EMAIL=.*/ADMIN_EMAIL=$ADMIN_EMAIL/" .env
sed -i "s/ADMIN_PASSWORD=.*/ADMIN_PASSWORD=$ADMIN_PASSWORD/" .env
sed -i "s/SIGNAL_SERVICE_PHONE=.*/SIGNAL_SERVICE_PHONE=$SIGNAL_PHONE/" .env

# Lancer
docker compose --env-file .env -f docker/docker-compose.prod.yml up -d --build

echo "Terminé ! Accédez à http://votre-ip:3000"
#!/bin/bash

echo "=========================================="
echo "Installation de SignalShop"
echo "=========================================="

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "[ERREUR] Docker n'est pas installé."
    echo "Installez Docker : https://docs.docker.com/engine/install/"
    exit 1
fi

# Vérifier Git
if ! command -v git &> /dev/null; then
    echo "[ERREUR] Git n'est pas installé."
    echo "Installez Git : https://git-scm.com/download/linux"
    exit 1
fi

read -p "Adresse email administrateur (défaut: admin@example.com) : " ADMIN_EMAIL
ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}

read -p "Mot de passe administrateur (défaut: admin1234) : " ADMIN_PASSWORD
ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin1234}

if [ ! -f .env ]; then
    echo "Création du fichier .env..."
    cat > .env <<EOF
POSTGRES_USER=signaluser
POSTGRES_PASSWORD=change_this_strong_password
POSTGRES_DB=signal_shop
DATABASE_URL=postgresql://signaluser:change_this_strong_password@db:5432/signal_shop
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change_this_secret_key
BACKEND_PORT=8000
FRONTEND_PORT=3000
SIGNAL_SERVICE_PHONE=+33...
SIGNAL_PRO_PHONE=+33...
SIGNAL_CLI_VERSION=0.12.0
ADMIN_EMAIL=$ADMIN_EMAIL
ADMIN_PASSWORD=$ADMIN_PASSWORD
EOF
else
    echo "Le fichier .env existe déjà, il ne sera pas modifié."
fi

echo "Construction et démarrage des services..."
docker compose --env-file .env -f docker/docker-compose.yml up --build -d

if [ $? -ne 0 ]; then
    echo "[ERREUR] Échec du démarrage des services."
    exit 1
fi

echo "Initialisation de la base de données..."
sleep 10
docker exec -it signalshop_backend python -m scripts.init_db
docker exec -it signalshop_backend python -m scripts.create_initial_user

echo "=========================================="
echo "Installation terminée !"
echo "Accédez au dashboard : http://localhost:3000"
echo "Email admin : $ADMIN_EMAIL"
echo "Mot de passe : $ADMIN_PASSWORD"
echo "=========================================="
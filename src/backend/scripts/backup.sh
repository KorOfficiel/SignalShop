#!/bin/bash

# Script de sauvegarde PostgreSQL pour SignalShop
# Usage : bash scripts/backup.sh

# Créer le dossier de sauvegarde s'il n'existe pas
mkdir -p backups

# Nom du fichier avec date
FILENAME="backups/signalshop_$(date +%Y%m%d_%H%M%S).sql"

# Utiliser docker exec pour lancer pg_dump à l'intérieur du conteneur
docker exec signalshop_db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > "$FILENAME"

echo "Sauvegarde créée : $FILENAME"
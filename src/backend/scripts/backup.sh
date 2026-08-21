#!/bin/bash
# Script de sauvegarde chiffrée
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

# Dump de la base
docker exec signalshop_db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > $BACKUP_DIR/signalshop_$TIMESTAMP.sql

# Chiffrement avec GPG
gpg --symmetric --batch --passphrase "$BACKUP_PASSPHRASE" $BACKUP_DIR/signalshop_$TIMESTAMP.sql

# Supprimer le fichier non chiffré
rm $BACKUP_DIR/signalshop_$TIMESTAMP.sql

echo "Sauvegarde chiffrée : $BACKUP_DIR/signalshop_$TIMESTAMP.sql.gpg"
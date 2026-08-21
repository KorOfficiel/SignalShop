import os
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.deploy_token import DeployToken
from app.core.config import settings

# Récupérer les clés depuis l'environnement
OLD_KEY = os.environ.get("OLD_ENCRYPTION_KEY", "")
NEW_KEY = os.environ.get("NEW_ENCRYPTION_KEY", settings.encryption_key)

if not OLD_KEY or not NEW_KEY:
    raise RuntimeError("Les variables OLD_ENCRYPTION_KEY et NEW_ENCRYPTION_KEY sont requises.")

old_fernet = Fernet(OLD_KEY.encode())
new_fernet = Fernet(NEW_KEY.encode())

def recrypt():
    db = SessionLocal()
    try:
        tokens = db.query(DeployToken).all()
        for token in tokens:
            if token.ssh_key_encrypted:
                # Déchiffrer avec l'ancienne clé
                plaintext = old_fernet.decrypt(token.ssh_key_encrypted.encode()).decode()
                # Rechiffrer avec la nouvelle clé
                token.ssh_key_encrypted = new_fernet.encrypt(plaintext.encode()).decode()
        db.commit()
        print(f"{len(tokens)} clé(s) rechiffrée(s).")
    finally:
        db.close()

if __name__ == "__main__":
    recrypt()
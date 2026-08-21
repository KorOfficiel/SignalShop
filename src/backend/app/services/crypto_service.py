from cryptography.fernet import Fernet
import os

# Récupérer la clé depuis l'environnement, sinon en générer une temporaire
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key().decode())

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    """Chiffre une chaîne et retourne le résultat en base64."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Déchiffre une chaîne chiffrée."""
    return fernet.decrypt(encrypted_data.encode()).decode()
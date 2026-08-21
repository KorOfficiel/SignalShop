from cryptography.fernet import Fernet
import os
from app.core.config import settings

# Récupérer la clé de chiffrement depuis la configuration
ENCRYPTION_KEY = settings.encryption_key or Fernet.generate_key().decode()
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_secret(plaintext: str) -> str:
    """Chiffre un secret et retourne le texte chiffré."""
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_secret(ciphertext: str) -> str:
    """Déchiffre un secret."""
    return fernet.decrypt(ciphertext.encode()).decode()

def rotate_key():
    """Génère une nouvelle clé et l'affiche (à utiliser manuellement)."""
    new_key = Fernet.generate_key().decode()
    print(f"Nouvelle clé : {new_key}")
    return new_key
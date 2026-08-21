import os
import sys
from cryptography.fernet import Fernet

# Chemin du fichier .env (peut être passé en argument)
ENV_FILE = sys.argv[1] if len(sys.argv) > 1 else ".env"

def load_env():
    """Charge le fichier .env dans un dictionnaire."""
    env_vars = {}
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key] = value
    return env_vars

def save_env(env_vars):
    """Sauvegarde le dictionnaire dans .env."""
    with open(ENV_FILE, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

def rotate():
    new_key = Fernet.generate_key().decode()
    env_vars = load_env()
    env_vars["ENCRYPTION_KEY"] = new_key
    save_env(env_vars)
    print("Clé de chiffrement mise à jour. Redémarrez le backend.")

if __name__ == "__main__":
    rotate()
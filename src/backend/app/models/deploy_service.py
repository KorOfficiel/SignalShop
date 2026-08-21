import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.deploy_token import DeployToken
from app.services.vault_service import encrypt_secret, decrypt_secret

def generate_token(db: Session, email: str, domain: str, vps_host: str, vps_user: str, ssh_key: str) -> str:
    token = secrets.token_urlsafe(32)
    encrypted_key = encrypt_secret(ssh_key)
    expires = datetime.utcnow() + timedelta(hours=1)
    record = DeployToken(
        token=token,
        email=email,
        domain=domain,
        vps_host=vps_host,
        vps_user=vps_user,
        ssh_key_encrypted=encrypted_key,
        expires_at=expires
    )
    db.add(record)
    db.commit()
    return token

def consume_token(db: Session, token: str) -> DeployToken:
    record = db.query(DeployToken).filter(DeployToken.token == token).first()
    if not record or record.used or record.expires_at < datetime.utcnow():
        return None
    record.used = True
    db.commit()
    # Déchiffrer la clé SSH
    record.ssh_key_encrypted = decrypt_secret(record.ssh_key_encrypted)
    return record
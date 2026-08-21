from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import subprocess
import smtplib
from email.message import EmailMessage
import os

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.deploy_service import generate_token, consume_token
from app.models.deploy_token import DeployToken

router = APIRouter(prefix="/deployer", tags=["deployer"])

class TokenRequest(BaseModel):
    email: EmailStr
    domain: str
    vps_host: str
    vps_user: str = "root"
    ssh_key: str

class DeployWithToken(BaseModel):
    token: str

@router.post("/request-token")
def request_deploy_token(payload: TokenRequest, db: Session = Depends(get_db)):
    """Génère un token et envoie un email."""
    token = generate_token(
        db,
        email=payload.email,
        domain=payload.domain,
        vps_host=payload.vps_host,
        vps_user=payload.vps_user,
        ssh_key=payload.ssh_key
    )
    send_token_email(payload.email, token)
    return {"message": "Token envoyé par email"}

@router.post("/deploy-with-token")
def deploy_with_token(payload: DeployWithToken, db: Session = Depends(get_db)):
    """Exécute le déploiement avec un token valide."""
    record = consume_token(db, payload.token)
    if not record:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")

    script = f"""#!/bin/bash
set -e
cd /root
wget -q https://raw.githubusercontent.com/KorOfficiel/SignalShop/main/deploy_vps.sh
bash deploy_vps.sh <<EOF
{record.email}
password_temporaire
{record.domain}
EOF
"""
    # Utiliser la clé SSH déchiffrée
    ssh_key = record.ssh_key_encrypted
    try:
        result = subprocess.run(
            [
                "ssh",
                "-i", ssh_key,
                "-o", "StrictHostKeyChecking=no",
                f"{record.vps_user}@{record.vps_host}",
                script
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Erreur SSH: {result.stderr}")
        return {"status": "deployed", "dashboard_url": f"https://{record.domain}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def send_token_email(to_email: str, token: str):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print(f"[EMAIL TEST] Token pour {to_email}: {token}")
        return

    msg = EmailMessage()
    msg.set_content(f"Votre token de déploiement : {token}")
    msg['Subject'] = "Votre token de déploiement SignalShop"
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
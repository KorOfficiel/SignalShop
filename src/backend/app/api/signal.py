from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message_metadata import MessageMetadata
from app.api.auth import get_current_user
from app.services.conversation_engine import ConversationEngine
from app.core.config import settings

router = APIRouter(prefix="/signal", tags=["signal"])

class ReceiveMessage(BaseModel):
    from_number: str
    body: str

@router.post("/receive")
def receive_signal_message(
    message: ReceiveMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Réception manuelle (authentifiée)."""
    return process_message(message, db)

@router.post("/internal/receive")
def internal_receive(
    message: ReceiveMessage,
    x_internal_key: str = Header(None),
    db: Session = Depends(get_db)
):
    """Réception depuis le bridge (clé interne)."""
    if x_internal_key != settings.internal_api_key:
        raise HTTPException(status_code=403, detail="Clé interne invalide")
    return process_message(message, db)

def process_message(message: ReceiveMessage, db: Session):
    # Récupérer le premier utilisateur comme tenant par défaut
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=500, detail="Aucun utilisateur configuré")

    hash_phone = f"hash_{message.from_number}"
    customer = db.query(Customer).filter(
        Customer.tenant_id == user.tenant_id,
        Customer.signal_phone_hash == hash_phone
    ).first()
    if not customer:
        customer = Customer(tenant_id=user.tenant_id, signal_phone_hash=hash_phone)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    conversation = db.query(Conversation).filter(
        Conversation.tenant_id == user.tenant_id,
        Conversation.customer_id == customer.id,
        Conversation.closed == False
    ).first()
    if not conversation:
        conversation = Conversation(
            tenant_id=user.tenant_id,
            customer_id=customer.id,
            state="AI_ACTIVE"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    metadata = MessageMetadata(
        conversation_id=conversation.id,
        sender="customer",
        timestamp=datetime.utcnow(),
        content_hash=str(hash(message.body)),
        content_length=len(message.body),
        content=message.body
    )
    db.add(metadata)
    db.commit()

    engine = ConversationEngine()
    response_text = engine.process_message(
        db=db,
        tenant_id=user.tenant_id,
        conversation_id=str(conversation.id),
        customer_id=customer.id,
        customer_message=message.body
    )

    ai_metadata = MessageMetadata(
        conversation_id=conversation.id,
        sender="ai",
        timestamp=datetime.utcnow(),
        content_hash=str(hash(response_text)),
        content_length=len(response_text),
        content=response_text
    )
    db.add(ai_metadata)
    db.commit()

    return {"conversation_id": str(conversation.id), "response": response_text}
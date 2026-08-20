from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message_metadata import MessageMetadata
from app.models.customer import Customer
from app.api.auth import get_current_user
from app.services.signal_adapter import SignalAdapter
from app.services.permission_service import has_permission

router = APIRouter(prefix="/conversations", tags=["conversations"])
signal_adapter = SignalAdapter()

class MessageMetadataRead(BaseModel):
    id: UUID
    sender: str
    timestamp: datetime
    content: Optional[str] = None
    content_hash: Optional[str] = None
    content_length: Optional[int] = None

    class Config:
        from_attributes = True

class ConversationRead(BaseModel):
    id: UUID
    customer_id: UUID
    state: str
    timer_expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    closed: bool

    class Config:
        from_attributes = True

class SendMessage(BaseModel):
    body: str

@router.get("", response_model=List[ConversationRead])
def list_conversations(
    include_closed: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "view_conversations"):
        raise HTTPException(status_code=403, detail="Permission manquante : voir les conversations")
    query = db.query(Conversation).filter(Conversation.tenant_id == current_user.tenant_id)
    if not include_closed:
        query = query.filter(Conversation.closed == False)
    return query.all()

@router.get("/{conversation_id}", response_model=ConversationRead)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    return conversation

@router.get("/{conversation_id}/messages", response_model=List[MessageMetadataRead])
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    messages = db.query(MessageMetadata).filter(
        MessageMetadata.conversation_id == conversation_id
    ).order_by(MessageMetadata.timestamp.asc()).all()
    return messages

@router.post("/{conversation_id}/message", response_model=ConversationRead)
def professional_message(
    conversation_id: UUID,
    message: SendMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "take_handoff"):
        raise HTTPException(status_code=403, detail="Permission manquante : prendre la main")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")

    metadata = MessageMetadata(
        conversation_id=conversation.id,
        sender="professional",
        timestamp=datetime.utcnow(),
        content_hash=str(hash(message.body)),
        content_length=len(message.body),
        content=message.body
    )
    db.add(metadata)
    conversation.state = "HUMAN_ACTIVE"
    conversation.timer_expires_at = None
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)

    customer = db.query(Customer).filter(Customer.id == conversation.customer_id).first()
    if customer:
        signal_adapter.send_message(to=customer.signal_phone_hash, body=message.body)
    else:
        signal_adapter.send_message(to="unknown", body=message.body)

    return conversation

@router.post("/{conversation_id}/handoff", response_model=ConversationRead)
def human_handoff(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "take_handoff"):
        raise HTTPException(status_code=403, detail="Permission manquante : prendre la main")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    conversation.state = "HUMAN_ACTIVE"
    conversation.timer_expires_at = None
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    return conversation

@router.post("/{conversation_id}/ai-resume", response_model=ConversationRead)
def ai_resume(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "take_handoff"):
        raise HTTPException(status_code=403, detail="Permission manquante : prendre la main")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    conversation.state = "AI_ACTIVE"
    conversation.timer_expires_at = None
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    return conversation

@router.post("/{conversation_id}/stop-ai", response_model=ConversationRead)
def stop_ai(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "take_handoff"):
        raise HTTPException(status_code=403, detail="Permission manquante : prendre la main")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    conversation.state = "HUMAN_ACTIVE"
    conversation.timer_expires_at = None
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    return conversation

@router.post("/{conversation_id}/close", response_model=ConversationRead)
def close_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(db, current_user, "take_handoff"):
        raise HTTPException(status_code=403, detail="Permission manquante : prendre la main")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    conversation.closed = True
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    return conversation
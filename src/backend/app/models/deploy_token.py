import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class DeployToken(Base):
    __tablename__ = "deploy_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    vps_host = Column(String, nullable=False)
    vps_user = Column(String, default="root")
    ssh_key_encrypted = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)
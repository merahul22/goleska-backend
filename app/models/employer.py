import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Employer(Base):
    __tablename__ = 'employers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_auth_id = Column(String, unique=True, index=True, nullable=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    gstin = Column(String)
    hiring_mode = Column(String, default='MANUAL')
    is_verified = Column(Boolean, default=False)
    business_document_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

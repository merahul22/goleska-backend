import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Employer(Base):
    __tablename__ = 'employers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_auth_id = Column(String, unique=True, index=True, nullable=True)
    account_type = Column(String, default='REGISTERED_BUSINESS') # REGISTERED_BUSINESS, REGISTERED_INDUSTRY, UNREGISTERED_BUSINESS
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    
    # Business Details
    business_category = Column(String)
    website_url = Column(String)
    annual_revenue = Column(String)
    description = Column(String)
    services_required = Column(JSON)
    
    # KYC Details
    gstin = Column(String)
    pan_number = Column(String)
    cin_number = Column(String)
    director_data = Column(JSON)
    kyc_aadhaar_number = Column(String)
    
    # Unregistered Business specifics
    proprietor_name = Column(String)
    enterprise_phone = Column(String)
    num_proprietors = Column(Integer)
    udyam_number = Column(String)
    
    hiring_mode = Column(String, default='MANUAL')
    is_verified = Column(Boolean, default=False)
    business_document_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

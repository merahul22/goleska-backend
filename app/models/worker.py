import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from app.core.database import Base

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_auth_id = Column(String, unique=True, index=True, nullable=True)
    account_type = Column(String, default='EMPLOYEE') # EMPLOYEE, INDIVIDUAL
    phone = Column(String, unique=True, index=True, nullable=False)
    alternate_phone = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String)
    
    # KYC Details
    aadhaar_number = Column(String, unique=True)
    permanent_address = Column(JSON)
    current_address = Column(JSON)
    blood_group = Column(String)
    kyc_document_url = Column(String)
    
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    current_location = Column(Geometry(geometry_type='POINT', srid=4326))
    expected_salary = Column(Numeric)
    overall_rating = Column(Numeric, default=5.0)
    total_jobs = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from app.core.database import Base

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    name = Column(String)
    aadhaar_number = Column(String, unique=True)
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    kyc_document_url = Column(String)
    current_location = Column(Geometry(geometry_type='POINT', srid=4326))
    expected_salary = Column(Numeric)
    overall_rating = Column(Numeric, default=5.0)
    total_jobs = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

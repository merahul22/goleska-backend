import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from app.core.database import Base

class JobSite(Base):
    __tablename__ = 'job_sites'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id = Column(UUID(as_uuid=True), ForeignKey('employers.id'))
    name = Column(String, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

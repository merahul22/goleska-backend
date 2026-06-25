import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id = Column(UUID(as_uuid=True), ForeignKey('employers.id'))
    job_site_id = Column(UUID(as_uuid=True), ForeignKey('job_sites.id'))
    title = Column(String, nullable=False)
    headcount_required = Column(Integer, nullable=False)
    max_daily_salary = Column(Numeric)
    min_experience = Column(Integer)
    status = Column(String, default='SEARCHING')
    created_at = Column(DateTime, default=datetime.utcnow)

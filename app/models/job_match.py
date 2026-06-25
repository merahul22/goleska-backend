import uuid
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class JobMatch(Base):
    __tablename__ = 'job_matches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'))
    worker_id = Column(UUID(as_uuid=True), ForeignKey('workers.id'))
    composite_score = Column(Numeric, nullable=False)
    status = Column(String, default='PENDING')
    expires_at = Column(DateTime, nullable=False)

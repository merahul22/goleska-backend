import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class BookingHistory(Base):
    __tablename__ = 'booking_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'))
    worker_id = Column(UUID(as_uuid=True), ForeignKey('workers.id'))
    employer_id = Column(UUID(as_uuid=True), ForeignKey('employers.id'))
    job_site_id = Column(UUID(as_uuid=True), ForeignKey('job_sites.id'))
    actual_start_time = Column(DateTime)
    actual_end_time = Column(DateTime)
    worker_rating = Column(Integer)
    employer_rating = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)

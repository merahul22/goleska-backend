from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class WorkerSkill(Base):
    __tablename__ = 'worker_skills'

    worker_id = Column(UUID(as_uuid=True), ForeignKey('workers.id'), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey('skills.id'), primary_key=True)
    years_experience = Column(Integer)
    is_verified = Column(Boolean, default=False)

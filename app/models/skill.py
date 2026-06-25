import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)

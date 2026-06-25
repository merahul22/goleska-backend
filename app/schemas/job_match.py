# pyrefly: ignore [missing-import]
from pydantic import BaseModel, UUID4
from datetime import datetime
from decimal import Decimal

class JobMatchBase(BaseModel):
    job_id: UUID4
    worker_id: UUID4

class JobMatchCreate(JobMatchBase):
    composite_score: Decimal
    expires_at: datetime

class JobMatchResponse(JobMatchBase):
    id: UUID4
    composite_score: Decimal
    status: str
    expires_at: datetime

    class Config:
        from_attributes = True

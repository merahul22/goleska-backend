# pyrefly: ignore [missing-import]
from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class JobBase(BaseModel):
    title: str
    headcount_required: int
    max_daily_salary: Optional[Decimal] = None
    min_experience: Optional[int] = None

class JobCreate(JobBase):
    job_site_id: UUID4

class JobResponse(JobBase):
    id: UUID4
    employer_id: UUID4
    job_site_id: UUID4
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

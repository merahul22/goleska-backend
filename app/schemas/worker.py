# pyrefly: ignore [missing-import]
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal

class WorkerBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    is_available: bool = True
    expected_salary: Optional[Decimal] = None

class WorkerCreate(WorkerBase):
    pass

class WorkerLocationUpdate(BaseModel):
    latitude: float
    longitude: float

class WorkerResponse(WorkerBase):
    id: UUID4
    overall_rating: Decimal
    total_jobs: int
    created_at: datetime

    class Config:
        from_attributes = True

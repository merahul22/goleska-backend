# pyrefly: ignore [missing-import]
from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional
from datetime import datetime

class EmployerBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: EmailStr
    phone: str
    gstin: Optional[str] = None
    hiring_mode: str = Field(default="MANUAL", description="Can be AUTONOMOUS or MANUAL")

class EmployerCreate(EmployerBase):
    pass

class EmployerResponse(EmployerBase):
    id: UUID4
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

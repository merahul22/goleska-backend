# pyrefly: ignore [missing-import]
from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional
from datetime import datetime

class EmployerBase(BaseModel):
    account_type: Optional[str] = "REGISTERED_BUSINESS"
    company_name: str
    contact_name: Optional[str] = None
    email: EmailStr
    phone: str
    
    # Business Details
    business_category: Optional[str] = None
    website_url: Optional[str] = None
    annual_revenue: Optional[str] = None
    description: Optional[str] = None
    services_required: Optional[list] = None
    
    # KYC Details
    gstin: Optional[str] = None
    pan_number: Optional[str] = None
    cin_number: Optional[str] = None
    director_data: Optional[list] = None
    kyc_aadhaar_number: Optional[str] = None
    
    # Unregistered Business specifics
    proprietor_name: Optional[str] = None
    enterprise_phone: Optional[str] = None
    num_proprietors: Optional[int] = None
    udyam_number: Optional[str] = None
    
    hiring_mode: str = Field(default="MANUAL", description="Can be AUTONOMOUS or MANUAL")

class EmployerCreate(EmployerBase):
    pass

class EmployerResponse(EmployerBase):
    id: UUID4
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

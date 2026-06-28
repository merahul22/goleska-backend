from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PanVerificationRequest(BaseModel):
    pan_number: str

class DirectorData(BaseModel):
    name: str
    din: str

class PanVerificationResponse(BaseModel):
    valid: bool
    company_name: str
    cin_number: str
    directors: List[DirectorData]

@router.post("/verify-pan", response_model=PanVerificationResponse)
async def verify_pan(request: PanVerificationRequest):
    # Mock behavior for MVP
    if len(request.pan_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid PAN format")
        
    return PanVerificationResponse(
        valid=True,
        company_name="Simulated Pvt Ltd",
        cin_number="U74999MH2024PTC123456",
        directors=[
            DirectorData(name="Rahul Director", din="01234567"),
            DirectorData(name="Aditi Signatory", din="07654321")
        ]
    )

class AadhaarVerificationRequest(BaseModel):
    aadhaar_number: str

class AadhaarVerificationResponse(BaseModel):
    valid: bool
    message: str
    name_matched: str

@router.post("/verify-aadhaar", response_model=AadhaarVerificationResponse)
async def verify_aadhaar(request: AadhaarVerificationRequest):
    if len(request.aadhaar_number) != 12:
        raise HTTPException(status_code=400, detail="Aadhaar must be 12 digits")
        
    return AadhaarVerificationResponse(
        valid=True,
        message="Aadhaar successfully verified via offline XML",
        name_matched="Verified User"
    )

class BankVerificationRequest(BaseModel):
    account_number: str
    ifsc: str

class BankVerificationResponse(BaseModel):
    valid: bool
    account_name: str

@router.post("/penny-drop", response_model=BankVerificationResponse)
async def penny_drop(request: BankVerificationRequest):
    return BankVerificationResponse(
        valid=True,
        account_name="Simulated Verified Enterprise"
    )

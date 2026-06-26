from fastapi import APIRouter, status
from app.schemas.auth import OTPRequest
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: OTPRequest):
    """
    Initiates phone number verification by sending an OTP.
    """
    await auth_service.send_otp(request.phone)
    return {"message": "OTP sent successfully"}

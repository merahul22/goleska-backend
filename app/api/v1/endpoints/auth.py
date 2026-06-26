from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(
    request: OTPVerify,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Verifies the OTP and returns a JWT token.
    """
    return await auth_service.verify_otp(session, request.phone, request.code)


@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: OTPRequest):
    """
    Initiates phone number verification by sending an OTP.
    """
    await auth_service.send_otp(request.phone)
    return {"message": "OTP sent successfully"}

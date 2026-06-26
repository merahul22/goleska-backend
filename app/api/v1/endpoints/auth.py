from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_worker
from app.models.worker import Worker
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


@router.post("/worker/upload-id")
async def upload_worker_id(
    file: UploadFile = File(...),
    current_worker: Worker = Depends(get_current_worker),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Uploads an Aadhaar/Gov ID for the worker. Requires a valid JWT.
    """
    updated_worker = await auth_service.upload_worker_id(session, current_worker, file)
    return {
        "message": "ID uploaded successfully. KYC verification pending.",
        "kyc_document_url": updated_worker.kyc_document_url
    }


@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: OTPRequest):
    """
    Initiates phone number verification by sending an OTP.
    """
    await auth_service.send_otp(request.phone)
    return {"message": "OTP sent successfully"}

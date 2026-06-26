from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_worker, get_current_employer
from app.models.worker import Worker
from app.models.employer import Employer
from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse
from app.services.auth_service import send_otp as do_send_otp, verify_otp as do_verify_otp, upload_worker_id as do_upload_worker_id, verify_worker_liveness as do_verify_worker_liveness, verify_employer_business as do_verify_employer_business

router = APIRouter()

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(
    request: OTPVerify,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Verifies the OTP and returns a JWT token.
    """
    return await do_verify_otp(session, request.phone, request.code)


@router.post("/worker/upload-id")
async def upload_worker_id(
    file: UploadFile = File(...),
    current_worker: Worker = Depends(get_current_worker),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Uploads an Aadhaar/Gov ID for the worker. Requires a valid JWT.
    """
    updated_worker = await do_upload_worker_id(session, current_worker, file)
    return {
        "message": "ID uploaded successfully. KYC verification pending.",
        "kyc_document_url": updated_worker.kyc_document_url
    }

@router.post("/worker/liveness")
async def verify_worker_liveness(
    file: UploadFile = File(...),
    current_worker: Worker = Depends(get_current_worker),
    session: AsyncSession = Depends(get_db_session)
):
    """Verifies worker liveness via selfie."""
    await do_verify_worker_liveness(session, current_worker, file)
    return {"message": "Liveness check passed. Account is fully verified."}

@router.post("/employer/verify-business")
async def verify_employer_business(
    file: UploadFile = File(...),
    gstin: str = Form(None),
    current_employer: Employer = Depends(get_current_employer),
    session: AsyncSession = Depends(get_db_session)
):
    """Uploads business documents and sets employer to verified."""
    await do_verify_employer_business(session, current_employer, file, gstin)
    return {"message": "Business verification submitted and approved."}


@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: OTPRequest):
    """
    Initiates phone number verification by sending an OTP.
    """
    await do_send_otp(request.phone)
    return {"message": "OTP sent successfully"}

from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_worker, get_current_employer
from app.models.worker import Worker
from app.models.employer import Employer
from app.schemas.auth import TokenResponse
from app.services.auth_service import (
    upload_worker_id as do_upload_worker_id, 
    verify_worker_liveness as do_verify_worker_liveness, 
    verify_employer_business as do_verify_employer_business,
    get_worker_id_url,
    get_employer_business_url
)

router = APIRouter()

@router.get("/status")
async def auth_status():
    """
    Check Auth configuration.
    Note: OTP generation and verification are now handled directly by the Supabase client.
    """
    return {"status": "Supabase Auth Active"}


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

@router.get("/worker/id-url")
async def fetch_worker_id_url(
    current_worker: Worker = Depends(get_current_worker)
):
    """Returns a short-lived signed URL to view the uploaded ID."""
    url = await get_worker_id_url(current_worker)
    if not url:
        raise HTTPException(status_code=404, detail="No ID uploaded yet.")
    return {"signed_url": url}

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


@router.get("/employer/business-url")
async def fetch_employer_business_url(
    current_employer: Employer = Depends(get_current_employer)
):
    """Returns a short-lived signed URL to view the business document."""
    url = await get_employer_business_url(current_employer)
    if not url:
        raise HTTPException(status_code=404, detail="No document uploaded yet.")
    return {"signed_url": url}

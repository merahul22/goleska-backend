import logging
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.worker import Worker
from app.models.employer import Employer
from app.core.supabase import supabase_client
import uuid

logger = logging.getLogger(__name__)

async def _upload_file_to_supabase(file: UploadFile, folder: str, user_id: str) -> str:
    """Helper to upload a file to Supabase Storage and return the public URL"""
    file_bytes = await file.read()
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "bin"
    unique_filename = f"{folder}/{user_id}/{uuid.uuid4()}.{file_extension}"
    
    supabase_client.storage.from_("kyc-documents").upload(
        path=unique_filename,
        file=file_bytes,
        file_options={"content-type": file.content_type}
    )
    
    return supabase_client.storage.from_("kyc-documents").get_public_url(unique_filename)

async def upload_worker_id(session: AsyncSession, worker: Worker, file: UploadFile) -> Worker:
    """
    Uploads the Gov ID to Supabase Storage.
    """
    public_url = await _upload_file_to_supabase(file, "worker_ids", str(worker.id))
    
    worker.kyc_document_url = public_url
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    
    return worker

async def verify_worker_liveness(session: AsyncSession, worker: Worker, file: UploadFile) -> Worker:
    if not worker.kyc_document_url:
        raise HTTPException(status_code=400, detail="Must upload ID before liveness check.")
    
    # Upload the selfie to Supabase
    public_url = await _upload_file_to_supabase(file, "worker_selfies", str(worker.id))
    
    worker.is_verified = True
    session.add(worker)
    await session.commit()
    return worker

async def verify_employer_business(session: AsyncSession, employer: Employer, file: UploadFile, gstin: str = None) -> Employer:
    if gstin:
        employer.gstin = gstin
        
    public_url = await _upload_file_to_supabase(file, "employer_docs", str(employer.id))
    
    employer.business_document_url = public_url
    employer.is_verified = True
    session.add(employer)
    await session.commit()
    return employer

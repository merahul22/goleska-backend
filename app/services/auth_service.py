import random
import logging
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, UploadFile
from app.core.config import settings
from app.models.worker import Worker
from app.models.employer import Employer
from app.core.security import create_access_token
from app.core.supabase import supabase_client
import uuid

logger = logging.getLogger(__name__)

redis_client = Redis.from_url(settings.REDIS_URI, decode_responses=True)

async def send_otp(phone: str) -> bool:
    """
    Generates a 6-digit OTP, saves it to Redis with a 5-minute TTL, 
    and mocks sending an SMS via third-party service adapter.
    """
    otp_code = f"{random.randint(100000, 999999)}"
    
    redis_key = f"otp:{phone}"
    await redis_client.set(redis_key, otp_code, ex=300)
    
    print("="*40)
    print(f"🚀 MOCK SMS PROVIDER 🚀")
    print(f"Sending OTP to {phone}")
    print(f"Your GO LESKA verification code is: {otp_code}")
    print("="*40)
    
    return True

async def verify_otp(session: AsyncSession, phone: str, code: str) -> dict:
    """
    Verifies the OTP against Redis and issues a JWT if the user exists.
    """
    redis_key = f"otp:{phone}"
    stored_code = await redis_client.get(redis_key)
    
    if not stored_code or stored_code != code:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    await redis_client.delete(redis_key)
    
    worker_stmt = select(Worker).where(Worker.phone == phone)
    worker_result = await session.execute(worker_stmt)
    worker = worker_result.scalars().first()
    
    if worker:
        token = create_access_token(subject=worker.id)
        return {"access_token": token, "token_type": "bearer", "role": "worker"}
        
    employer_stmt = select(Employer).where(Employer.phone == phone)
    employer_result = await session.execute(employer_stmt)
    employer = employer_result.scalars().first()
    
    if employer:
        token = create_access_token(subject=employer.id)
        return {"access_token": token, "token_type": "bearer", "role": "employer"}
        
    raise HTTPException(status_code=404, detail="Phone number not registered. Please register first.")

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

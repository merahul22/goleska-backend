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

async def upload_worker_id(session: AsyncSession, worker: Worker, file: UploadFile) -> Worker:
    """
    Mocks uploading the Gov ID to an S3 bucket and triggers async KYC.
    """
    mock_s3_url = f"https://goleska-mock-s3.com/kyc/{worker.id}/{file.filename}"
    print("="*40)
    print(f"📁 MOCK S3 UPLOAD 📁")
    print(f"Uploading {file.filename} to {mock_s3_url}")
    print("="*40)
    
    worker.kyc_document_url = mock_s3_url
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    
    return worker

async def verify_worker_liveness(session: AsyncSession, worker: Worker, file: UploadFile) -> Worker:
    if not worker.kyc_document_url:
        raise HTTPException(status_code=400, detail="Must upload ID before liveness check.")
    worker.is_verified = True
    session.add(worker)
    await session.commit()
    return worker

async def verify_employer_business(session: AsyncSession, employer: Employer, file: UploadFile, gstin: str = None) -> Employer:
    if gstin:
        employer.gstin = gstin
    employer.business_document_url = f"https://goleska-mock-s3.com/business/{employer.id}/{file.filename}"
    employer.is_verified = True
    session.add(employer)
    await session.commit()
    return employer

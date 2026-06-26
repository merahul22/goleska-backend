import random
import logging
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.core.config import settings
from app.models.worker import Worker
from app.models.employer import Employer
from app.core.security import create_access_token

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URI, decode_responses=True)

    async def send_otp(self, phone: str) -> bool:
        """
        Generates a 6-digit OTP, saves it to Redis with a 5-minute TTL, 
        and mocks sending an SMS via third-party service adapter.
        """
        otp_code = f"{random.randint(100000, 999999)}"
        
        # Save to Redis (TTL 300 seconds = 5 mins)
        redis_key = f"otp:{phone}"
        await self.redis.set(redis_key, otp_code, ex=300)
        
        # Mock SMS Provider Logging (e.g. Twilio/SNS Adapter)
        print("="*40)
        print(f"🚀 MOCK SMS PROVIDER 🚀")
        print(f"Sending OTP to {phone}")
        print(f"Your GO LESKA verification code is: {otp_code}")
        print("="*40)
        
        return True

    async def verify_otp(self, session: AsyncSession, phone: str, code: str) -> dict:
        """
        Verifies the OTP against Redis and issues a JWT if the user exists.
        """
        redis_key = f"otp:{phone}"
        stored_code = await self.redis.get(redis_key)
        
        if not stored_code or stored_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
            
        # Clear the OTP to prevent reuse
        await self.redis.delete(redis_key)
        
        # Determine if phone belongs to Worker or Employer
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
            
        # If neither exists, they haven't registered
        raise HTTPException(status_code=404, detail="Phone number not registered. Please register first.")

auth_service = AuthService()

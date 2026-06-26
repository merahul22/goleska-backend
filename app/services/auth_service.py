import random
import logging
from redis.asyncio import Redis
from app.core.config import settings

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

auth_service = AuthService()

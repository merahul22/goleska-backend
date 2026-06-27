from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.database import get_db_session
from app.models.worker import Worker
from app.models.employer import Employer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/verify-otp")

def get_supabase_jwt_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated"
        )
        return payload
    except (jwt.PyJWTError, ValidationError) as e:
        print("JWT Error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_worker(
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
) -> Worker:
    supabase_auth_id = payload.get("sub")
    if not supabase_auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    stmt = select(Worker).where(Worker.supabase_auth_id == supabase_auth_id)
    result = await session.execute(stmt)
    worker = result.scalars().first()
    
    # Fallback to phone number for seeded data migration
    if not worker:
        phone = payload.get("phone")
        if phone:
            if not phone.startswith("+"):
                phone = "+" + phone
            stmt = select(Worker).where(Worker.phone == phone)
            worker = (await session.execute(stmt)).scalars().first()
            if worker:
                worker.supabase_auth_id = supabase_auth_id
                session.add(worker)
                await session.commit()
                return worker
                
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Worker not registered")
    return worker

async def get_current_employer(
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
) -> Employer:
    supabase_auth_id = payload.get("sub")
    if not supabase_auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    stmt = select(Employer).where(Employer.supabase_auth_id == supabase_auth_id)
    result = await session.execute(stmt)
    employer = result.scalars().first()
    
    # Fallback to phone number for seeded data migration
    if not employer:
        phone = payload.get("phone")
        if phone:
            if not phone.startswith("+"):
                phone = "+" + phone
            stmt = select(Employer).where(Employer.phone == phone)
            employer = (await session.execute(stmt)).scalars().first()
            if employer:
                employer.supabase_auth_id = supabase_auth_id
                session.add(employer)
                await session.commit()
                return employer

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Employer not found")
    return employer

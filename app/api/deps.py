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

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return user_id
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_worker(
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
) -> Worker:
    stmt = select(Worker).where(Worker.id == user_id)
    result = await session.execute(stmt)
    worker = result.scalars().first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Worker not found")
    return worker

async def get_current_employer(
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
) -> Employer:
    stmt = select(Employer).where(Employer.id == user_id)
    result = await session.execute(stmt)
    employer = result.scalars().first()
    if not employer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Employer not found")
    return employer

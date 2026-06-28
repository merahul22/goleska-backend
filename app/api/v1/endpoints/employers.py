from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.employer import EmployerCreate, EmployerResponse
from app.services.employer_service import EmployerService
from app.api.deps import get_supabase_jwt_payload

router = APIRouter()

@router.post("/register", response_model=EmployerResponse, status_code=status.HTTP_201_CREATED)
async def register_employer(
    employer_in: EmployerCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Register a new employer on the platform.
    """
    return await EmployerService.create_employer(session=session, employer_in=employer_in)

@router.get("/me", response_model=EmployerResponse)
async def get_current_employer(
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get the currently logged in employer's profile.
    Requires Supabase JWT.
    """
    jwt_phone = payload.get("phone")
    if not jwt_phone:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Phone number missing in JWT token")
        
    formatted_phone = f"+{jwt_phone}" if not jwt_phone.startswith("+") else jwt_phone
    raw_phone = jwt_phone.replace("+", "")
    
    from sqlalchemy.future import select
    from sqlalchemy import or_
    from app.models.employer import Employer
    
    result = await session.execute(
        select(Employer).where(
            or_(
                Employer.phone == formatted_phone,
                Employer.phone == raw_phone,
                Employer.phone == jwt_phone
            )
        )
    )
    employer = result.scalars().first()
    
    if not employer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Employer profile not found")
        
    return employer

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.employer import EmployerCreate, EmployerResponse
from app.services.employer_service import EmployerService

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

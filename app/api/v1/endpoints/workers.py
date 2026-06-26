from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.worker import WorkerRegistrationCombined, WorkerResponse
from app.services.worker_service import WorkerService

router = APIRouter()

@router.post("/register", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def register_worker(
    worker_in: WorkerRegistrationCombined,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Register a new worker with their initial GPS location.
    """
    return await WorkerService.create_worker(session=session, worker_in=worker_in)

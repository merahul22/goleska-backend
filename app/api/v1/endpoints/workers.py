from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_supabase_jwt_payload
from app.schemas.worker import WorkerRegistrationCombined, WorkerResponse
from app.services.worker_service import WorkerService

router = APIRouter()

@router.post("/register", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def register_worker(
    worker_in: WorkerRegistrationCombined,
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Register a new worker with their initial GPS location.
    Requires Supabase JWT.
    """
    # Prefer phone from verified JWT
    jwt_phone = payload.get("phone")
    if jwt_phone:
        worker_in.phone = f"+{jwt_phone}" if not jwt_phone.startswith("+") else jwt_phone
        
    supabase_auth_id = payload.get("sub")
    return await WorkerService.create_worker(session=session, worker_in=worker_in, supabase_auth_id=supabase_auth_id)

@router.get("/me", response_model=WorkerResponse)
async def get_current_worker(
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get the currently logged in worker's profile.
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
    from app.models.worker import Worker
    
    result = await session.execute(
        select(Worker).where(
            or_(
                Worker.phone == formatted_phone,
                Worker.phone == raw_phone,
                Worker.phone == jwt_phone
            )
        )
    )
    worker = result.scalars().first()
    
    if not worker:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Worker profile not found")
        
    return worker

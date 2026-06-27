from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_employer
from app.models.employer import Employer
from app.models.job import Job
from app.models.job_match import JobMatch
from app.models.worker import Worker
from app.schemas.job import JobCreate
from app.services.matching_service import find_candidates_for_job
from fastapi import HTTPException
from app.api.deps import get_current_worker
from sqlalchemy import update, select

router = APIRouter()

@router.post("")
async def create_job(
    request: JobCreate,
    current_employer: Employer = Depends(get_current_employer),
    session: AsyncSession = Depends(get_db_session)
):
    job = Job(
        employer_id=current_employer.id,
        job_site_id=request.job_site_id,
        title=request.title,
        headcount_required=request.headcount_required,
        max_daily_salary=request.max_daily_salary,
        min_experience=request.min_experience
    )
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    matches = await find_candidates_for_job(session, job.id)
    
    return {
        "message": "Job created. Matching engine completed.", 
        "job_id": job.id, 
        "matches_found": len(matches)
    }

@router.post("/{job_id}/accept")
async def accept_job(
    job_id: str,
    current_worker: Worker = Depends(get_current_worker),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Accepts a dispatched job match.
    Updates the JobMatch status and sets the worker to unavailable.
    """
    # Verify the match exists and is pending
    stmt = select(JobMatch).where(
        JobMatch.job_id == job_id, 
        JobMatch.worker_id == current_worker.id,
        JobMatch.status == "PENDING"
    )
    result = await session.execute(stmt)
    match = result.scalars().first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Job match not found or already processed.")
        
    # Update JobMatch
    match.status = "ACCEPTED"
    session.add(match)
    
    # Update Worker
    current_worker.is_available = False
    session.add(current_worker)
    
    await session.commit()
    return {"message": "Job successfully accepted"}

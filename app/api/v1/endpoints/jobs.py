from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_employer
from app.models.employer import Employer
from app.models.job import Job
from app.schemas.job import JobCreate
from app.services.matching_service import find_candidates_for_job

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

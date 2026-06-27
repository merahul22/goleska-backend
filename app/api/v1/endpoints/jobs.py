from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.api.deps import get_current_employer
from app.models.employer import Employer
from app.models.job import Job
from app.schemas.job import JobCreate, JobCreateNLP
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

@router.post("/nlp")
async def create_job_from_nlp(
    request: JobCreateNLP,
    current_employer: Employer = Depends(get_current_employer),
    session: AsyncSession = Depends(get_db_session)
):
    from app.services.llm_service import parse_job_request
    parsed_job = await parse_job_request(request.prompt, str(request.job_site_id))
    
    job = Job(
        employer_id=current_employer.id,
        job_site_id=parsed_job.job_site_id,
        title=parsed_job.title,
        headcount_required=parsed_job.headcount_required,
        max_daily_salary=parsed_job.max_daily_salary,
        min_experience=parsed_job.min_experience
    )
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    matches = await find_candidates_for_job(session, job.id)
    
    return {
        "message": "NLP Job created. Matching engine completed.", 
        "job_id": job.id, 
        "matches_found": len(matches),
        "parsed_data": parsed_job.model_dump(mode="json")
    }

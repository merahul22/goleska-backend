from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid

from app.core.database import get_db_session
from app.api.deps import get_supabase_jwt_payload
from app.schemas.job_site import JobSiteBase, JobSiteResponse
from app.models.employer import Employer
from app.models.job_site import JobSite

router = APIRouter()

async def get_current_employer_from_jwt(payload: dict, session: AsyncSession):
    jwt_phone = payload.get("phone")
    if not jwt_phone:
        raise HTTPException(status_code=400, detail="Phone number missing in JWT token")
        
    formatted_phone = f"+{jwt_phone}" if not jwt_phone.startswith("+") else jwt_phone
    raw_phone = jwt_phone.replace("+", "")
    
    from sqlalchemy import or_
    
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
        raise HTTPException(status_code=404, detail="Employer profile not found")
        
    return employer

@router.get("/me", response_model=List[JobSiteResponse])
async def get_my_job_sites(
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get all job sites owned by the currently logged in employer.
    """
    employer = await get_current_employer_from_jwt(payload, session)
    
    result = await session.execute(select(JobSite).where(JobSite.employer_id == employer.id))
    job_sites = result.scalars().all()
    
    return job_sites

@router.post("/", response_model=JobSiteResponse, status_code=status.HTTP_201_CREATED)
async def create_job_site(
    site_in: JobSiteBase,
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new job site for the logged in employer.
    """
    employer = await get_current_employer_from_jwt(payload, session)
    
    db_site = JobSite(
        employer_id=employer.id,
        name=site_in.name,
        location=f"POINT({site_in.longitude} {site_in.latitude})"
    )
    
    session.add(db_site)
    await session.commit()
    await session.refresh(db_site)
    
    return db_site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_site(
    site_id: uuid.UUID,
    payload: dict = Depends(get_supabase_jwt_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a job site owned by the logged in employer.
    """
    employer = await get_current_employer_from_jwt(payload, session)
    
    result = await session.execute(
        select(JobSite).where(JobSite.id == site_id, JobSite.employer_id == employer.id)
    )
    site = result.scalars().first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Job site not found or not owned by you")
        
    await session.delete(site)
    await session.commit()
    
    return None

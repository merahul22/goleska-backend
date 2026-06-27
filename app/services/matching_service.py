import json
from sqlalchemy import func, cast, select
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2 import Geography
from app.models.job import Job
from app.models.job_site import JobSite
from app.models.worker import Worker
from app.models.job_match import JobMatch
from datetime import datetime, timedelta

async def find_candidates_for_job(session: AsyncSession, job_id: str, initial_radius: int = 10000, max_radius: int = 30000):
    result = await session.execute(
        select(Job, JobSite).join(JobSite, Job.job_site_id == JobSite.id).where(Job.id == job_id)
    )
    row = result.first()
    if not row: return []
    
    job, job_site = row
    target_count = job.headcount_required * 3
    
    distance = func.ST_DistanceSphere(Worker.current_location, job_site.location)
    score_expr = (
        (1.0 - (distance / max_radius)) * 0.5 +
        (Worker.overall_rating / 5.0) * 0.3 +
        (func.least(Worker.total_jobs, 50) / 50.0) * 0.2
    )

    stmt = (
        select(Worker, score_expr.label("composite_score"))
        .where(
            func.ST_DistanceSphere(Worker.current_location, job_site.location) <= max_radius,
            Worker.is_available == True,
            Worker.is_verified == True
        )
        .order_by(score_expr.desc())
        .limit(target_count)
    )
    
    workers_res = await session.execute(stmt)
    workers_list = list(workers_res)
    
    matches = [
        JobMatch(
            job_id=job.id,
            worker_id=worker.id,
            composite_score=score,
            expires_at=datetime.utcnow() + timedelta(minutes=2)
        )
        for worker, score in workers_list
    ]
        
    if matches:
        session.add_all(matches)
        await session.commit()
    
    return matches

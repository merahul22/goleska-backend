from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException
from geoalchemy2.elements import WKTElement
from app.models.worker import Worker
from app.schemas.worker import WorkerRegistrationCombined

class WorkerService:
    @staticmethod
    async def create_worker(session: AsyncSession, worker_in: WorkerRegistrationCombined) -> Worker:
        # Check for uniqueness on phone or aadhaar
        filters = [Worker.phone == worker_in.phone]
        if worker_in.aadhaar_number:
            filters.append(Worker.aadhaar_number == worker_in.aadhaar_number)
            
        stmt = select(Worker).where(or_(*filters))
        result = await session.execute(stmt)
        existing_worker = result.scalars().first()

        if existing_worker:
            if existing_worker.phone == worker_in.phone:
                raise HTTPException(status_code=400, detail="Phone number already registered")
            if worker_in.aadhaar_number and existing_worker.aadhaar_number == worker_in.aadhaar_number:
                raise HTTPException(status_code=400, detail="Aadhaar number already registered")

        # Geospatial conversion (Longitude first, then Latitude)
        # SRID 4326 is standard WGS84
        point_wkt = f"POINT({worker_in.longitude} {worker_in.latitude})"
        location_geom = WKTElement(point_wkt, srid=4326)

        # Map Pydantic schema to SQLAlchemy model
        new_worker = Worker(
            phone=worker_in.phone,
            email=worker_in.email,
            name=worker_in.name,
            aadhaar_number=worker_in.aadhaar_number,
            is_available=worker_in.is_available,
            expected_salary=worker_in.expected_salary,
            current_location=location_geom
        )
        
        # Persist to database
        session.add(new_worker)
        await session.commit()
        await session.refresh(new_worker)
        
        return new_worker

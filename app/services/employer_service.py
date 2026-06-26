from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException
from app.models.employer import Employer
from app.schemas.employer import EmployerCreate

class EmployerService:
    @staticmethod
    async def create_employer(session: AsyncSession, employer_in: EmployerCreate) -> Employer:
        # Explicit check for unique constraints to avoid generic SQLAlchemy IntegrityErrors
        stmt = select(Employer).where(
            or_(
                Employer.email == employer_in.email,
                Employer.phone == employer_in.phone
            )
        )
        result = await session.execute(stmt)
        existing_employer = result.scalars().first()

        if existing_employer:
            if existing_employer.email == employer_in.email:
                raise HTTPException(status_code=400, detail="Email already registered")
            if existing_employer.phone == employer_in.phone:
                raise HTTPException(status_code=400, detail="Phone number already registered")

        # Map Pydantic schema to SQLAlchemy model
        new_employer = Employer(
            company_name=employer_in.company_name,
            contact_name=employer_in.contact_name,
            email=employer_in.email,
            phone=employer_in.phone,
            gstin=employer_in.gstin,
            hiring_mode=employer_in.hiring_mode
        )
        
        # Persist to database
        session.add(new_employer)
        await session.commit()
        await session.refresh(new_employer)
        
        return new_employer

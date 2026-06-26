import asyncio
from app.core.database import async_session_maker
from app.models.employer import Employer
from app.core.security import create_access_token

async def main():
    async with async_session_maker() as session:
        employer = Employer(
            company_name="Test Corp",
            email="employer@test.com",
            phone="+919999999999"
        )
        session.add(employer)
        await session.commit()
        await session.refresh(employer)
        
        token = create_access_token(subject=employer.id)
        print(f"EMPLOYER_TOKEN={token}")

if __name__ == "__main__":
    asyncio.run(main())

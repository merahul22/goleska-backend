import asyncio
from sqlalchemy.future import select
from app.core.database import async_session_maker
from app.models.employer import Employer

async def check():
    async with async_session_maker() as session:
        result = await session.execute(select(Employer))
        employers = result.scalars().all()
        for e in employers:
            print(f"Employer: id={e.id}, phone='{e.phone}', auth_id='{e.supabase_auth_id}'")

if __name__ == "__main__":
    asyncio.run(check())

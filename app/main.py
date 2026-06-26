from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import employers, workers

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(employers.router, prefix="/api/v1/employers", tags=["Employers"])
app.include_router(workers.router, prefix="/api/v1/workers", tags=["Workers"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

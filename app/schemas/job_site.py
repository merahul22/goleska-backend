# pyrefly: ignore [missing-import]
from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

class JobSiteBase(BaseModel):
    name: str
    latitude: float = Field(..., description="Latitude of the site")
    longitude: float = Field(..., description="Longitude of the site")

class JobSiteCreate(JobSiteBase):
    employer_id: UUID4

class JobSiteResponse(BaseModel):
    id: UUID4
    employer_id: UUID4
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

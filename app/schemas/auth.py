from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone: str = Field(..., description="Phone number to send OTP to")

class OTPVerify(BaseModel):
    phone: str = Field(...)
    code: str = Field(..., min_length=6, max_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

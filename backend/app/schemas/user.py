from pydantic import BaseModel, EmailStr
from pydantic import BaseModel



class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class BusinessSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CurrentUserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    business: BusinessSummary | None = None

    class Config:
        from_attributes = True
from pydantic import BaseModel


class POSBusinessContext(BaseModel):
    id: int
    name: str


class POSEmployeeContext(BaseModel):
    id: int
    full_name: str
    role: str


class POSLocationContext(BaseModel):
    id: int
    name: str
    address: str
    city: str | None = None
    state: str | None = None
    country: str | None = None


class POSWorkspaceContextResponse(BaseModel):
    business: POSBusinessContext
    employee: POSEmployeeContext
    location: POSLocationContext
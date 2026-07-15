from fastapi import APIRouter

from app.schemas.international import InternationalOptionsResponse
from app.services.international_service import (
    get_international_options_service,
)


router = APIRouter(
    prefix="/international",
    tags=["International"],
)


@router.get(
    "/options",
    response_model=InternationalOptionsResponse,
)
def get_international_options():
    return get_international_options_service()
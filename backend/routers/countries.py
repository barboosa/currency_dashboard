from fastapi import APIRouter
from services.countries_service import get_countries

router = APIRouter(
    prefix="/countries",
    tags=["countries"]
)

@router.get("")
def read_countries():
    return get_countries()

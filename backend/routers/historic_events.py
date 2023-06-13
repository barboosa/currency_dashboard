from fastapi import APIRouter
from services.historic_events_service import get_historic_events

router = APIRouter(
    prefix="/historic-events",
    tags=["historic-events"]
)


@router.get("")
def read_historic_events():
    return get_historic_events()

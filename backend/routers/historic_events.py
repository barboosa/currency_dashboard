from fastapi import APIRouter

router = APIRouter(
    prefix="/historic-events",
    tags=["historic-events"]
)


@router.get("")
def read_countries():
    return ["COVID-19", "9/11", "2008 Financial Crisis"]

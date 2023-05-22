from datetime import date
from fastapi import APIRouter
from services.currencies_service import get_currency_pairs, get_historic_prices, get_currency_calculations

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"]
)

@router.get("")
def read_currency_pairs() -> list:
    return get_currency_pairs()

@router.get("/currency-correlations")
async def read_currency_calculations(start_date: date, end_date: date) -> dict:
    return await get_currency_calculations(start_date, end_date)

@router.get("/historic-prices")
async def read_historic_prices(start_date: date, end_date: date) -> dict:
    return await get_historic_prices(start_date, end_date)

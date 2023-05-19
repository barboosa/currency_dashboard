from fastapi import APIRouter

router = APIRouter(
    prefix="/countries",
    tags=["countries"]
)

country_currencies = {
    'USA': 'USD',
    'Canada': 'CAD',
    'Japan': 'JPY',
    'Germany': 'EUR',
    'UK': 'GBP',
    'Australia': 'AUD',
    'Switzerland': 'CHF',
    'New Zealand': 'NZD'
}


@router.get("")
def read_countries() -> dict:
    return country_currencies

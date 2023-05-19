from fastapi import APIRouter
import yfinance as yf
import pandas as pd
from datetime import date

router = APIRouter()

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"]
)


def supported_currency_pairs():
    currencies = ['EUR', 'USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'NZD']
    supported_currency_pairs = [
        f'{a}{b}=X' for a in currencies for b in currencies if a != b]
    return supported_currency_pairs


@router.get("")
def read_currency_pairs() -> list:
    return supported_currency_pairs()


@router.get("/currency-correlations")
def read_currency_calculations(start_date: date, end_date: date) -> dict:
    currency_pairs = supported_currency_pairs()

    price_data = {}
    for currency_pair in currency_pairs:
        data = yf.download(currency_pair, start=start_date, end=end_date)
        if data.empty:
            continue
        price_data[currency_pair] = data['Close']

    df = pd.DataFrame(price_data)
    correlations = df.corr()

    return correlations.to_dict()


@router.get("/historic-prices")
def read_historic_prices(start_date: date, end_date: date) -> dict:
    currency_pairs = supported_currency_pairs()

    trend_data = {}
    for currency_pair in currency_pairs:
        data = yf.download(currency_pair, start=start_date, end=end_date)
        if data.empty:
            continue
        price_series = data['Close']
        trend_data[currency_pair] = price_series

    return trend_data

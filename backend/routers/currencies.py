from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
import yfinance as yf
import pandas as pd
from datetime import date
from concurrent.futures import ProcessPoolExecutor

router = APIRouter()

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"]
)


# Create a ProcessPoolExecutor
executor = ProcessPoolExecutor(max_workers=20)

def supported_currency_pairs():
    currencies = ['EUR', 'USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'NZD']
    supported_currency_pairs = [
        f'{a}{b}=X' for a in currencies for b in currencies if a != b]
    return supported_currency_pairs


@router.get("")
def read_currency_pairs() -> list:
    return supported_currency_pairs()

def fetch_data(currency_pair: str, start_date: date, end_date: date):
    print(f"Start fetching data for {currency_pair}")
    try:
        data = yf.download(currency_pair, start=start_date, end=end_date)
        if data.empty:
            print(f"No data for {currency_pair}")
            return {}
        else:
            print(f"Finished fetching data for {currency_pair}")
            return {currency_pair: data['Close']}
    except Exception as e:
        print(f"Error fetching data for {currency_pair}: {e}")
        return {}

@router.get("/currency-correlations")
async def read_currency_calculations(start_date: date, end_date: date) -> dict:
    currency_pairs = supported_currency_pairs()

    price_data = {}

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, fetch_data, currency_pair, start_date, end_date) for currency_pair in currency_pairs]

    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            price_data.update(result)

    df = pd.DataFrame(price_data)
    correlations = df.corr()

    return correlations.to_dict()

@router.get("/historic-prices")
async def read_historic_prices(start_date: date, end_date: date) -> dict:
    currency_pairs = supported_currency_pairs()

    trend_data = {}

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, fetch_data, currency_pair, start_date, end_date) for currency_pair in currency_pairs]

    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            trend_data.update(result)

    return trend_data
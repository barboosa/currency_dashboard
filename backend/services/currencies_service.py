from utils.currencies_util import supported_currency_pairs, gather_data
from datetime import date
import pandas as pd

def get_currency_pairs():
    return supported_currency_pairs()

async def get_currency_calculations(start_date: date, end_date: date):
    price_data = await gather_data(start_date, end_date)
    df = pd.DataFrame(price_data)
    correlations = df.corr()

    return correlations.to_dict()

async def get_historic_prices(start_date: date, end_date: date):
    return await gather_data(start_date, end_date)

from fastapi import FastAPI, HTTPException
import yfinance as yf
import pandas as pd
from datetime import date

app = FastAPI()


def supported_currency_pairs():
    currencies = ['EUR', 'USD', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'NZD']
    supported_currency_pairs = [
        f'{a}{b}=X' for a in currencies for b in currencies if a != b]
    return supported_currency_pairs


@app.get("/forex-pairs")
def read_forex_pairs() -> list:
    return supported_currency_pairs


@app.get("/currency-correlations")
def calculate_currency_correlations(start_date: date, end_date: date) -> dict:
    forex_pairs = supported_currency_pairs

    price_data = {}
    for forex_pair in forex_pairs:
        data = yf.download(forex_pair, start=start_date, end=end_date)
        if data.empty:
            continue
        price_data[forex_pair] = data['Close']

    df = pd.DataFrame(price_data)
    correlations = df.corr()

    return correlations.to_dict()

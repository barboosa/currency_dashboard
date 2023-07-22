import asyncio
import yfinance as yf
from datetime import date, timedelta
from concurrent.futures import ProcessPoolExecutor
import logging
from utils.supported_countries import supported_countries

logger = logging.getLogger(__name__)

executor = ProcessPoolExecutor(max_workers=20)


def supported_currency_pairs():
    currencies = list(set(country['currencyAlpha3']
                      for country in supported_countries))
    pairs = [f'{a}{b}=X' for a in currencies for b in currencies if a != b]
    return pairs


def fetch_data(currency_pair: str, start_date: date, end_date: date):
    logger.info(f"Start fetching data for {currency_pair}")
    try:
        # add one day to the end_date
        data = yf.download(currency_pair, start=start_date,
                           end=end_date + timedelta(days=1))
        if data.empty:
            logger.warning(f"No data for {currency_pair}")
            return None
        else:
            logger.info(f"Finished fetching data for {currency_pair}")
            return {currency_pair: data['Close']}
    except Exception as e:
        logger.error(f"Error fetching data for {currency_pair}: {e}")
        return None


async def gather_data(start_date: date, end_date: date):
    currency_pairs = supported_currency_pairs()
    loop = asyncio.get_event_loop()

    tasks = [loop.run_in_executor(executor, fetch_data, currency_pair,
                                  start_date, end_date) for currency_pair in currency_pairs]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    data = {}
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Error in fetching data: {result}")
        elif result is not None:
            data.update(result)

    return data

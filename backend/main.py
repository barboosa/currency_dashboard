from fastapi import FastAPI
from routers import countries
from routers import currencies
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(title='Currencies API',
              description='An API that returns currency information', version='1.0.0')
app.include_router(currencies.router)
app.include_router(countries.router)

logger.info("Currencies API has started")
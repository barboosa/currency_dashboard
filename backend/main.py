from fastapi import FastAPI, Request
from routers import countries, currencies, historic_events
import logging
from time import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='Currencies API',
              description='An API that returns currency information', version='1.0.0')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Processing time for {request.url.path}: {process_time}")
    return response

app.include_router(currencies.router)
app.include_router(countries.router)
app.include_router(historic_events.router)

logger.info("Currencies API has started")

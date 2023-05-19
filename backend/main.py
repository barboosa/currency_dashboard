from fastapi import FastAPI
from routers import countries
from routers import currencies

app = FastAPI(title='Currencies API',
              description='An API that returns currency information', version='1.0.0')
app.include_router(currencies.router)
app.include_router(countries.router)

import uvicorn
from fastapi import FastAPI

from routers import currencies

app = FastAPI()
app.include_router(currencies.router)

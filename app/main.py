import zoneinfo
from datetime import datetime
from fastapi import FastAPI, Request
from .db import create_all_tables
from .routers import customers, transactions, invoices, plans
import time

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware("http")
async def loq_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Process time: {process_time} for {request.url}")
    # response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def log_headers(request: Request, call_next):
    print(f"Headers: {request.headers}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Hola, Luis!"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}
# main.py

from fastapi import FastAPI
from api.routes import invoices, ar_balance  # import from the correct subfolder

app = FastAPI(
    title="NetSuite Financial API",
    description="Expose invoice and AR data from your local database.",
    version="0.1.0"
)

# Include your endpoint routers
app.include_router(invoices.router)
app.include_router(ar_balance.router)

@app.get("/")
def read_root():
    return {f"message": "Welcome to the NetSuite Financial API"}
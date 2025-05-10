# api/main.py
from fastapi import FastAPI
from api import core
from api.routes import chatbot
from api.routes import invoices, ar_balance  # import from the correct subfolder
app = FastAPI(title="FinBot API")

# Add all routers
app.include_router(core.router)
app.include_router(chatbot.router, prefix="/api")
app.include_router(invoices.router)
app.include_router(ar_balance.router)

# Optional: root route
@app.get("/")
async def root():
    return {"message": "FinBot is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)
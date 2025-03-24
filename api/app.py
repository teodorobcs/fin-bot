# api/app.py
from fastapi import FastAPI
from api import core

app = FastAPI(title="FinBot API")

# Add all routers
app.include_router(core.router)

# Optional: root route
@app.get("/")
async def root():
    return {"message": "FinBot is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)
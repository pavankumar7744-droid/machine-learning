from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="E-Commerce ML Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import purchase, datasets, forecast

app.include_router(purchase.router, prefix="/api/purchase", tags=["purchase"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running."}

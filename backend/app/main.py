from fastapi import FastAPI
from app.api.phase1 import router as phase1_router
from app.api.phase2 import router as phase2_router

app = FastAPI(
    title="FortiGate Automation",
    description="Phase 1 – Address Extraction",
    version="1.0"
)

app.include_router(phase1_router)
app.include_router(phase2_router)

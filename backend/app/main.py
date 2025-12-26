from fastapi import FastAPI
from app.api.phase1 import router as phase1_router
from app.api.phase2 import router as phase2_router
from app.api.phase3 import router as phase3_router
from app.api.phase4 import router as phase4_router


app = FastAPI(
    title="FortiGate Automation",
    description="Phase 1 – Address Extraction",
    version="1.0"
)

app.include_router(phase1_router)
app.include_router(phase2_router)
app.include_router(phase3_router)
app.include_router(phase4_router)

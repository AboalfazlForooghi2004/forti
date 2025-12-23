from fastapi import APIRouter, HTTPException
from app.services.fortigate_client import FortiGateClient
from app.utils.logger import logger
import json
import os

router = APIRouter(prefix="/api/phase1", tags=["Phase 1"])

@router.get("/addresses")
def get_addresses():
    try:
        client = FortiGateClient()

        addresses = client.get_address_objects()
        groups = client.get_address_groups()

        os.makedirs("data", exist_ok=True)
        with open("data/addresses.json", "w") as f:
            json.dump(addresses, f, indent=2)

        with open("data/address_groups.json", "w") as f:
            json.dump(groups, f, indent=2)

        logger.info("Phase 1 completed successfully")

        return {
            "address_objects": addresses,
            "address_groups": groups
        }

    except Exception as e:
        logger.error(f"Phase 1 failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

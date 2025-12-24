from fastapi import APIRouter, HTTPException
from app.services.fortigate_client import FortiGateClient
from app.services.analyzer import (
    find_duplicate_addresses,
    find_groups_for_ip
)
from app.utils.logger import logger

router = APIRouter(prefix="/api/phase2", tags=["Phase 2"])

@router.get("/duplicates")
def duplicate_addresses():
    try:
        client = FortiGateClient()
        addresses = client.get_address_objects()

        duplicates = find_duplicate_addresses(addresses)

        logger.info("Duplicate IP analysis completed")

        return {
            "duplicates": duplicates
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Analysis failed")


@router.post("/ip-groups")
def ip_group_lookup(payload: dict):
    try:
        ip = payload.get("ip")
        if not ip:
            raise HTTPException(status_code=400, detail="IP is required")

        client = FortiGateClient()
        addresses = client.get_address_objects()
        groups = client.get_address_groups()

        result = find_groups_for_ip(ip, addresses, groups)

        return {
            "ip": ip,
            "groups": result
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Lookup failed")

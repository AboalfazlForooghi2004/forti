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

        logger.info(f"Duplicate IP analysis completed - Found {len(duplicates)} duplicates")

        return {
            "duplicates": duplicates,
            "count": len(duplicates)
        }

    except Exception as e:
        logger.error(f"Duplicate analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/ip-groups")
def ip_group_lookup(payload: dict):
    try:
        ip = payload.get("ip")
        if not ip:
            raise HTTPException(
                status_code=400,
                detail="IP address is required"
            )

        client = FortiGateClient()
        addresses = client.get_address_objects()
        groups = client.get_address_groups()

        result = find_groups_for_ip(ip, addresses, groups)

        logger.info(f"IP lookup for {ip} - Found {len(result)} groups")

        return {
            "ip": ip,
            "groups": result,
            "count": len(result)
        }

    except Exception as e:
        logger.error(f"IP lookup failed for {ip}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lookup failed: {str(e)}"
        )
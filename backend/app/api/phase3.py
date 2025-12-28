from fastapi import APIRouter, HTTPException
from app.services.fortigate_client import FortiGateClient
from app.services.vip_manager import build_vip_payload, build_policy_update
from app.utils.logger import logger

router = APIRouter(prefix="/api/phase3", tags=["Phase 3"])

@router.post("/vip")
def create_vip(payload: dict):
    try:
        client = FortiGateClient()
        vip_payload = build_vip_payload(payload)

        result = client.post("/api/v2/cmdb/firewall/vip", vip_payload)

        logger.info(f"VIP {payload['name']} created successfully")

        return {
            "status": "success",
            "vip": payload["name"],
            "result": result
        }

    except Exception as e:
        logger.error(f"VIP creation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"VIP creation failed: {str(e)}"
        )


@router.put("/policy")
def update_policy(payload: dict):
    try:
        policy_id = payload.get("policy_id")
        vip_name = payload.get("vip_name")

        if not policy_id or not vip_name:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: policy_id, vip_name"
            )

        client = FortiGateClient()
        update_payload = build_policy_update(vip_name)

        result = client.put(
            f"/api/v2/cmdb/firewall/policy/{policy_id}",
            update_payload
        )

        logger.info(f"Policy {policy_id} updated with VIP {vip_name}")

        return {
            "status": "success",
            "policy_id": policy_id,
            "vip_name": vip_name,
            "result": result
        }

    except Exception as e:
        logger.error(f"Policy update failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Policy update failed: {str(e)}"
        )
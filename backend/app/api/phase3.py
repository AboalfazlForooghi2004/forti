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

        url = f"{client.base_url}/api/v2/cmdb/firewall/vip"
        r = client.session.post(url, json=vip_payload)
        r.raise_for_status()

        logger.info(f"VIP {payload['name']} created")

        return {"status": "success", "vip": payload["name"]}

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="VIP creation failed")


@router.put("/policy")
def update_policy(payload: dict):
    try:
        policy_id = payload.get("policy_id")
        vip_name = payload.get("vip_name")

        if not policy_id or not vip_name:
            raise HTTPException(status_code=400, detail="Missing fields")

        client = FortiGateClient()
        update_payload = build_policy_update(vip_name)

        url = f"{client.base_url}/api/v2/cmdb/firewall/policy/{policy_id}"
        r = client.session.put(url, json=update_payload)
        r.raise_for_status()

        logger.info(f"Policy {policy_id} updated with VIP {vip_name}")

        return {"status": "success"}

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Policy update failed")

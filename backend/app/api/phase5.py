from fastapi import APIRouter, HTTPException
from app.services.fortigate_client import FortiGateClient
from app.services.rollback import (
    vip_used_in_policy,
    remove_vip_from_policy,
    vip_used_in_group,
    remove_vip_from_group
)
from app.utils.logger import logger

router = APIRouter(prefix="/api/phase5", tags=["Phase 5"])

@router.post("/rollback")
def rollback_vip(payload: dict):
    vip_name = payload.get("vip_name")
    if not vip_name:
        raise HTTPException(status_code=400, detail="VIP name required")

    try:
        client = FortiGateClient()

        # 1️⃣ Policies
        policies = client.get("/api/v2/cmdb/firewall/policy")
        for p in policies["results"]:
            if vip_used_in_policy(p, vip_name):
                update = remove_vip_from_policy(p, vip_name)
                client.put(f"/api/v2/cmdb/firewall/policy/{p['policyid']}", update)
                logger.info(f"VIP {vip_name} removed from policy {p['policyid']}")

        # 2️⃣ VIP Groups
        groups = client.get("/api/v2/cmdb/firewall/vipgrp")
        for g in groups["results"]:
            if vip_used_in_group(g, vip_name):
                update = remove_vip_from_group(g, vip_name)
                client.put(f"/api/v2/cmdb/firewall/vipgrp/{g['name']}", update)
                logger.info(f"VIP {vip_name} removed from VIPGRP {g['name']}")

        # 3️⃣ Delete VIP
        client.delete(f"/api/v2/cmdb/firewall/vip/{vip_name}")
        logger.info(f"VIP {vip_name} deleted successfully")

        return {
            "status": "success",
            "vip": vip_name,
            "message": "Rollback completed"
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Rollback failed")

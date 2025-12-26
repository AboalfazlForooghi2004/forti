from fastapi import APIRouter, HTTPException
from app.services.fortigate_client import FortiGateClient
from app.services.automation import build_vip, build_vip_group
from app.utils.logger import logger

router = APIRouter(prefix="/api/phase4", tags=["Phase 4"])

@router.post("/publish")
def publish(payload: dict):
    """
    payload = {
      "external_ip": "1.1.1.1",
      "interface": "wan1",
      "policy_id": 10,
      "targets": [
        {"ip": "192.168.1.10", "port": 80},
        {"ip": "192.168.1.11", "port": 80}
      ]
    }
    """
    try:
        client = FortiGateClient()
        vip_names = []

        for t in payload["targets"]:
            vip_name = f"VIP_{t['ip']}_{t['port']}"
            vip_payload = build_vip(
                vip_name,
                payload["external_ip"],
                t["ip"],
                t["port"],
                payload["interface"]
            )

            client.post("/api/v2/cmdb/firewall/vip", vip_payload)
            vip_names.append(vip_name)

        vipgrp_name = f"VIPGRP_{payload['targets'][0]['port']}"
        vipgrp_payload = build_vip_group(vipgrp_name, vip_names)

        client.post("/api/v2/cmdb/firewall/vipgrp", vipgrp_payload)

        client.put(
            f"/api/v2/cmdb/firewall/policy/{payload['policy_id']}",
            {
                "dstaddr": [{"name": vipgrp_name}]
            }
        )

        logger.info(f"Phase 4 completed – VIPGRP {vipgrp_name}")

        return {
            "status": "success",
            "vip_group": vipgrp_name,
            "vips": vip_names
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Automation failed")

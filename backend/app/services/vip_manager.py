from app.utils.logger import logger

def build_vip_payload(data):
    return {
        "name": data["name"],
        "extip": data["external_ip"],
        "mappedip": [{"range": data["mapped_ip"]}],
        "extintf": data["interface"],
        "portforward": "enable",
        "extport": data["external_port"],
        "mappedport": data["mapped_port"],
        "protocol": "tcp"
    }


def build_policy_update(vip_name):
    return {
        "dstaddr": [
            {"name": vip_name}
        ]
    }

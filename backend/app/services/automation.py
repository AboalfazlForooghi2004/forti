def build_vip(name, ext_ip, map_ip, port, interface):
    return {
        "name": name,
        "extip": ext_ip,
        "mappedip": [{"range": map_ip}],
        "extintf": interface,
        "portforward": "enable",
        "protocol": "tcp",
        "extport": port,
        "mappedport": port
    }


def build_vip_group(name, vip_names):
    return {
        "name": name,
        "member": [{"name": v} for v in vip_names]
    }

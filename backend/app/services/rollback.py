def vip_used_in_policy(policy, vip_name):
    dstaddr = policy.get("dstaddr", [])
    return any(v["name"] == vip_name for v in dstaddr)


def remove_vip_from_policy(policy, vip_name):
    return {
        "dstaddr": [
            v for v in policy.get("dstaddr", [])
            if v["name"] != vip_name
        ]
    }


def vip_used_in_group(group, vip_name):
    members = group.get("member", [])
    return any(m["name"] == vip_name for m in members)


def remove_vip_from_group(group, vip_name):
    return {
        "member": [
            m for m in group.get("member", [])
            if m["name"] != vip_name
        ]
    }

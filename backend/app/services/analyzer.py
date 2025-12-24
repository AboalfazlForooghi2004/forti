from collections import defaultdict

def find_duplicate_addresses(addresses):
    ip_map = defaultdict(list)

    for addr in addresses:
        subnet = addr.get("subnet")
        if subnet:
            ip_map[subnet].append(addr["name"])

    duplicates = {
        ip: names
        for ip, names in ip_map.items()
        if len(names) > 1
    }

    return duplicates


def find_groups_for_ip(ip, addresses, groups):
    matched_objects = [
        addr["name"]
        for addr in addresses
        if addr.get("subnet", "").startswith(ip)
    ]

    result_groups = []

    for grp in groups:
        members = grp.get("member", [])
        for m in members:
            if m["name"] in matched_objects:
                result_groups.append(grp["name"])
                break

    return result_groups

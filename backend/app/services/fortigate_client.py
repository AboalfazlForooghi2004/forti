import os
import requests
from app.utils.logger import logger

class FortiGateClient:
    def __init__(self):
        self.base_url = os.getenv("FORTIGATE_HOST")
        self.token = os.getenv("FORTIGATE_TOKEN")
        self.verify_ssl = os.getenv("VERIFY_SSL", "false").lower() == "true"

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_address_objects(self):
        url = f"{self.base_url}/api/v2/cmdb/firewall/address"
        logger.info("Fetching Address Objects")
        r = requests.get(url, headers=self.headers, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()["results"]

    def get_address_groups(self):
        url = f"{self.base_url}/api/v2/cmdb/firewall/addrgrp"
        logger.info("Fetching Address Groups")
        r = requests.get(url, headers=self.headers, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()["results"]

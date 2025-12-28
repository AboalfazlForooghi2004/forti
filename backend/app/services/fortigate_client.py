import os
import requests
from app.utils.logger import logger

class FortiGateClient:
    def __init__(self):
        self.base_url = os.getenv("FORTIGATE_HOST")
        self.token = os.getenv("FORTIGATE_TOKEN")
        self.verify_ssl = os.getenv("VERIFY_SSL", "false").lower() == "true"

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        self.session.verify = self.verify_ssl

    def get(self, endpoint):
        """Generic GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        r = self.session.get(url, timeout=30)
        r.raise_for_status()
        return r.json()

    def post(self, endpoint, payload):
        """Generic POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        r = self.session.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def put(self, endpoint, payload):
        """Generic PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        r = self.session.put(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def delete(self, endpoint):
        """Generic DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        r = self.session.delete(url, timeout=30)
        r.raise_for_status()
        return r.json()

    def get_address_objects(self):
        """Fetch all address objects"""
        logger.info("Fetching Address Objects")
        return self.get("/api/v2/cmdb/firewall/address")["results"]

    def get_address_groups(self):
        """Fetch all address groups"""
        logger.info("Fetching Address Groups")
        return self.get("/api/v2/cmdb/firewall/addrgrp")["results"]
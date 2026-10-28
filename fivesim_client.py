import time
import requests
from typing import Optional, Tuple

class FiveSimError(Exception):
    pass

class FiveSim:
    BASE = "https://5sim.net/v1"

    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        })

    def _get(self, path: str) -> dict:
        r = self.session.get(f"{self.BASE}{path}", timeout=30)
        if r.status_code != 200:
            raise FiveSimError(f"{r.status_code}: {r.text[:300]}")
        return r.json()

    def balance(self) -> float:
        return float(self._get("/user/profile").get("balance", 0))

    def buy(self, country: str, operator: str, product: str) -> Tuple[str, str]:
        data = self._get(f"/user/buy/activation/{country}/{operator}/{product}")
        return str(data["id"]), str(data["phone"])

    def check(self, order_id: str) -> Tuple[str, Optional[str]]:
        data = self._get(f"/user/check/{order_id}")
        status = str(data.get("status", "PENDING"))
        code = None
        sms = data.get("sms") or []
        if sms and isinstance(sms[0], dict):
            code = sms[0].get("code")
        return status, code

    def cancel(self, order_id: str):
        self._get(f"/user/cancel/{order_id}")

    def finish(self, order_id: str):
        self._get(f"/user/finish/{order_id}")

    def poll_sms(self, order_id: str, timeout: int = 180, interval: int = 5) -> str:
        deadline = time.time() + timeout
        while time.time() < deadline:
            status, code = self.check(order_id)
            if status == "RECEIVED" and code:
                return code
            if status in ("CANCELED", "TIMEOUT", "BANNED"):
                raise FiveSimError(f"order {status}")
            time.sleep(interval)
        raise FiveSimError("SMS timeout")
import hashlib
import hmac
import json
import os
from typing import Any, Dict


class C0Logger:
    """
    Local C=0-style signature logger.

    Uses HMAC-SHA256 over normalized JSON payloads and writes entries
    to a log directory for audit and replay by external systems.
    """

    def __init__(self, log_dir: str = "logs/c0", secret_key: bytes = b"axiom_c0_secret") -> None:
        self.log_dir = log_dir
        self.secret_key = secret_key
        os.makedirs(self.log_dir, exist_ok=True)

    def _payload_hash(self, payload: Dict[str, Any]) -> str:
        enc = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(enc).hexdigest()

    def _sign(self, payload_hash: str) -> str:
        sig = hmac.new(self.secret_key, payload_hash.encode("utf-8"), hashlib.sha256).hexdigest()
        return sig

    def sign_and_log(self, label: str, payload: Dict[str, Any]) -> Dict[str, str]:
        h = self._payload_hash(payload)
        s = self._sign(h)
        entry = {
            "label": label,
            "hash": h,
            "signature": s,
        }
        filename = f"{label}_{h[:12]}.json"
        path = os.path.join(self.log_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
        return entry
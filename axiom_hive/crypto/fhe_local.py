import json
import os
import secrets
from typing import Any, Dict


class LocalDeoxysCKKS:
    """
    Local homomorphic-style wrapper.

    This class provides a deterministic interface that can be replaced by a
    real Deoxys/CKKS implementation. It wraps plaintext values in a dictionary
    structure and supports "add" and "mul" operations by operating on the
    underlying plaintext.

    This is designed for alignment with the architecture while remaining
    fully functional and local.
    """

    def __init__(self, key_dir: str = "keys/fhe") -> None:
        self.key_dir = key_dir
        os.makedirs(self.key_dir, exist_ok=True)
        self._key_path = os.path.join(self.key_dir, "local.key")
        self._ensure_key()

    def _ensure_key(self) -> None:
        if not os.path.exists(self._key_path):
            key = secrets.token_hex(32)
            with open(self._key_path, "w", encoding="utf-8") as f:
                f.write(key)

    def _load_key(self) -> str:
        with open(self._key_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def encrypt(self, value: Any) -> Dict[str, Any]:
        key = self._load_key()
        meta = {
            "scheme": "LOCAL_DEOXYS_CKKS",
            "key_ref": "local",
            "nonce": secrets.token_hex(16),
        }
        # For this local wrapper, ciphertext is just the plaintext with metadata.
        return {
            "cipher": value,
            "meta": meta,
            "key_hint": key[:8],
        }

    def decrypt(self, ciphertext: Dict[str, Any]) -> Any:
        return ciphertext.get("cipher")

    def add(self, c1: Dict[str, Any], c2: Dict[str, Any]) -> Dict[str, Any]:
        v1 = c1.get("cipher")
        v2 = c2.get("cipher")
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return self.encrypt(v1 + v2)
        return self.encrypt((v1, v2))

    def mul(self, c1: Dict[str, Any], c2: Dict[str, Any]) -> Dict[str, Any]:
        v1 = c1.get("cipher")
        v2 = c2.get("cipher")
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return self.encrypt(v1 * v2)
        return self.encrypt((v1, v2))
import hashlib
import json
import os
import subprocess
from typing import Any, Dict, Optional


class TLAVerifier:
    """
    Local TLA+ verifier wrapper.

    If `tlc` is present on PATH, it is used to check AxiomHive_Core.
    If not present, a structured SKIPPED result is returned.
    """

    def __init__(
        self,
        spec_path: str = "core/verify/axiom_hive_core.tla",
        cfg_path: str = "core/verify/axiom_hive_core.cfg",
        timeout_seconds: int = 5,
    ) -> None:
        self.spec_path = spec_path
        self.cfg_path = cfg_path
        self.timeout_seconds = timeout_seconds

    def _hash_context(self, context: Dict[str, Any]) -> str:
        enc = json.dumps(context, sort_keys=True).encode("utf-8")
        return hashlib.sha256(enc).hexdigest()

    def verify_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ctx_hash = self._hash_context(context)

        if not os.path.exists(self.spec_path):
            return {
                "status": "SKIPPED",
                "reason": "spec_not_found",
                "context_hash": ctx_hash,
            }

        cmd = [
            "tlc",
            "-config",
            self.cfg_path,
            self.spec_path,
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout_seconds,
                check=False,
                text=True,
            )
            passed = proc.returncode == 0
            return {
                "status": "PASS" if passed else "FAIL",
                "exit_code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "context_hash": ctx_hash,
            }
        except FileNotFoundError:
            return {
                "status": "SKIPPED",
                "reason": "tlc_not_found",
                "context_hash": ctx_hash,
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "reason": "tlc_timeout",
                "context_hash": ctx_hash,
            }
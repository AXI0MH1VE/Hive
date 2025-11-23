import time
from typing import Dict, Optional


class L402Gate:
    """
    Local L402-style gate.

    - Creates invoices for specific purposes
    - Issues tokens bound to invoice IDs
    - Verifies tokens for gating high-value operations
    """

    def __init__(self, sats_per_call: int = 1000) -> None:
        self.sats_per_call = sats_per_call
        self._invoices: Dict[str, Dict[str, str]] = {}
        self._tokens: Dict[str, Dict[str, str]] = {}

    def _now(self) -> int:
        return int(time.time())

    def create_invoice(self, purpose: str) -> Dict[str, str]:
        invoice_id = f"inv_{self._now()}_{len(self._invoices)+1}"
        invoice = {
            "id": invoice_id,
            "amount_sats": str(self.sats_per_call),
            "purpose": purpose,
            "bolt11": f"ln_stub_{invoice_id}",
        }
        self._invoices[invoice_id] = invoice
        return invoice

    def issue_token(self, invoice_id: str) -> Optional[str]:
        if invoice_id not in self._invoices:
            return None
        token = f"tok_{invoice_id}_{self._now()}"
        self._tokens[token] = {
            "invoice_id": invoice_id,
            "issued_at": str(self._now()),
        }
        return token

    def verify_token(self, token: str) -> bool:
        return token in self._tokens
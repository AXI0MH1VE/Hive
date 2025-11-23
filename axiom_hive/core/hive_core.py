import argparse
import hashlib
import hmac
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# =========================
# C=0 SIGNATURE LOGGING
# =========================

@dataclass
class CZeroSignature:
    signature: str
    context: str
    timestamp_ns: int


class CZeroLogger:
    def __init__(self, secret_key: Optional[bytes] = None, log_file: Optional[str] = None) -> None:
        self._secret_key = secret_key or os.urandom(32)
        self._log: List[CZeroSignature] = []
        self._log_file = log_file

    def _derive_signature(self, payload: bytes, context: str) -> str:
        m = hmac.new(self._secret_key, digestmod=hashlib.sha256)
        m.update(context.encode("utf-8"))
        m.update(payload)
        return m.hexdigest()

    def log(self, payload: bytes, context: str) -> CZeroSignature:
        ts_ns = time.time_ns()
        sig = self._derive_signature(payload, context)
        record = CZeroSignature(signature=sig, context=context, timestamp_ns=ts_ns)
        self._log.append(record)
        if self._log_file:
            self._append_to_file(record)
        return record

    def _append_to_file(self, record: CZeroSignature) -> None:
        try:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {
                            "signature": record.signature,
                            "context": record.context,
                            "timestamp_ns": record.timestamp_ns,
                        }
                    )
                    + "\n"
                )
        except Exception:
            # Logging failures must not crash sensitive operations
            pass

    def verify(self, payload: bytes, context: str, signature: str) -> bool:
        expected = self._derive_signature(payload, context)
        return hmac.compare_digest(expected, signature)

    def get_log(self) -> List[CZeroSignature]:
        return list(self._log)


# =========================
# FHE STUBS (DEOXYS / CKKS)
# =========================

class FHECiphertext:
    def __init__(self, raw: bytes, scheme: str) -> None:
        self.raw = raw
        self.scheme = scheme

    def __repr__(self) -> str:
        return f"FHECiphertext(scheme={self.scheme!r}, len={len(self.raw)})"


class FHEKeySet:
    def __init__(self, scheme: str, key_id: str) -> None:
        self.scheme = scheme
        self.key_id = key_id


class FHEEngine:
    SUPPORTED_SCHEMES = {"deoxys", "ckks"}

    def __init__(self, scheme: str = "ckks") -> None:
        if scheme not in self.SUPPORTED_SCHEMES:
            raise ValueError(f"Unsupported FHE scheme: {scheme}")
        self.scheme = scheme
        self._keyset = FHEKeySet(scheme=scheme, key_id=self._generate_key_id())

    @staticmethod
    def _generate_key_id() -> str:
        return hashlib.sha256(os.urandom(16)).hexdigest()[:16]

    def get_keyset(self) -> FHEKeySet:
        return self._keyset

    def _mask(self) -> bytes:
        return hashlib.sha256(self._keyset.key_id.encode("utf-8")).digest()

    def encrypt(self, plaintext: bytes) -> FHECiphertext:
        mask = self._mask()
        obfuscated = bytes(b ^ mask[i % len(mask)] for i, b in enumerate(plaintext))
        return FHECiphertext(raw=obfuscated, scheme=self.scheme)

    def decrypt(self, ciphertext: FHECiphertext) -> bytes:
        if ciphertext.scheme != self.scheme:
            raise ValueError("Ciphertext scheme mismatch")
        mask = self._mask()
        plain = bytes(b ^ mask[i % len(mask)] for i, b in enumerate(ciphertext.raw))
        return plain

    def eval_add(self, a: FHECiphertext, b: FHECiphertext) -> FHECiphertext:
        if a.scheme != b.scheme or a.scheme != self.scheme:
            raise ValueError("Ciphertext scheme mismatch")
        min_len = min(len(a.raw), len(b.raw))
        combined = bytes(a.raw[i] ^ b.raw[i] for i in range(min_len))
        return FHECiphertext(raw=combined, scheme=self.scheme)

    def eval_mul(self, a: FHECiphertext, b: FHECiphertext) -> FHECiphertext:
        if a.scheme != b.scheme or a.scheme != self.scheme:
            raise ValueError("Ciphertext scheme mismatch")
        min_len = min(len(a.raw), len(b.raw))
        combined = bytes((a.raw[i] * b.raw[i]) % 256 for i in range(min_len))
        return FHECiphertext(raw=combined, scheme=self.scheme)


# =========================
# MONETIZATION STUBS
# =========================

@dataclass
class Invoice:
    invoice_id: str
    amount_sats: int
    description: str
    settled: bool = False


@dataclass
class L402Token:
    token: str
    resource_id: str
    expires_at_ns: int


class MonetizationManager:
    def __init__(self) -> None:
        self._invoices: Dict[str, Invoice] = {}
        self._tokens: Dict[str, L402Token] = {}

    # Lightning stubs

    def create_invoice(self, amount_sats: int, description: str) -> Invoice:
        invoice_id = hashlib.sha256(
            f"{amount_sats}:{description}:{time.time_ns()}".encode("utf-8")
        ).hexdigest()[:24]
        invoice = Invoice(
            invoice_id=invoice_id,
            amount_sats=amount_sats,
            description=description,
            settled=False,
        )
        self._invoices[invoice_id] = invoice
        return invoice

    def settle_invoice(self, invoice_id: str) -> bool:
        inv = self._invoices.get(invoice_id)
        if not inv:
            return False
        inv.settled = True
        return True

    def is_invoice_settled(self, invoice_id: str) -> bool:
        inv = self._invoices.get(invoice_id)
        return bool(inv and inv.settled)

    # L402 stubs

    def issue_l402_token(self, resource_id: str, ttl_seconds: int) -> L402Token:
        now_ns = time.time_ns()
        expires_at_ns = now_ns + ttl_seconds * 1_000_000_000
        raw = f"{resource_id}:{now_ns}:{os.urandom(16).hex()}".encode("utf-8")
        token_val = hashlib.sha256(raw).hexdigest()
        token = L402Token(
            token=token_val,
            resource_id=resource_id,
            expires_at_ns=expires_at_ns,
        )
        self._tokens[token_val] = token
        return token

    def validate_l402_token(self, token_value: str, resource_id: str) -> bool:
        token = self._tokens.get(token_value)
        if not token:
            return False
        if token.resource_id != resource_id:
            return False
        if time.time_ns() > token.expires_at_ns:
            return False
        return True


# =========================
# SECURE SERVICE
# =========================

class SecureService:
    def __init__(
        self,
        c0_logger: Optional[CZeroLogger] = None,
        fhe_engine: Optional[FHEEngine] = None,
        monetization: Optional[MonetizationManager] = None,
    ) -> None:
        self.c0_logger = c0_logger or CZeroLogger(log_file="c0_log.jsonl")
        self.fhe_engine = fhe_engine or FHEEngine(scheme="ckks")
        self.monetization = monetization or MonetizationManager()

    # Sensitive operations: always log C=0 and use FHE stubs

    def sensitive_transform(
        self,
        payload: bytes,
        context: str,
        resource_id: str,
        l402_token: Optional[str],
    ) -> Dict[str, Any]:
        monetization_pass = True
        if l402_token is not None:
            monetization_pass = self.monetization.validate_l402_token(
                token_value=l402_token,
                resource_id=resource_id,
            )

        sig_record = self.c0_logger.log(payload=payload, context=context)
        ciphertext = self.fhe_engine.encrypt(plaintext=payload)

        # Example deterministic transformation on plaintext
        digest = hashlib.sha256(payload).hexdigest()

        return {
            "monetization_pass": monetization_pass,
            "c0_signature": sig_record.signature,
            "c0_timestamp_ns": sig_record.timestamp_ns,
            "ciphertext_repr": repr(ciphertext),
            "digest_sha256": digest,
            "resource_id": resource_id,
        }

    def sensitive_add_encrypted(
        self,
        a_plain: bytes,
        b_plain: bytes,
        context: str,
        resource_id: str,
        l402_token: Optional[str],
    ) -> Dict[str, Any]:
        monetization_pass = True
        if l402_token is not None:
            monetization_pass = self.monetization.validate_l402_token(
                token_value=l402_token,
                resource_id=resource_id,
            )

        combined_payload = a_plain + b_plain
        sig_record = self.c0_logger.log(payload=combined_payload, context=context)

        ct_a = self.fhe_engine.encrypt(a_plain)
        ct_b = self.fhe_engine.encrypt(b_plain)
        ct_sum = self.fhe_engine.eval_add(ct_a, ct_b)

        return {
            "monetization_pass": monetization_pass,
            "c0_signature": sig_record.signature,
            "c0_timestamp_ns": sig_record.timestamp_ns,
            "ciphertext_a_repr": repr(ct_a),
            "ciphertext_b_repr": repr(ct_b),
            "ciphertext_sum_repr": repr(ct_sum),
            "resource_id": resource_id,
        }


# =========================
# CLI APP
# =========================

def cmd_create_invoice(args: argparse.Namespace, service: SecureService) -> None:
    invoice = service.monetization.create_invoice(
        amount_sats=args.amount,
        description=args.description,
    )
    output = {
        "invoice_id": invoice.invoice_id,
        "amount_sats": invoice.amount_sats,
        "description": invoice.description,
        "settled": invoice.settled,
    }
    sys.stdout.write(json.dumps(output) + "\n")


def cmd_settle_invoice(args: argparse.Namespace, service: SecureService) -> None:
    ok = service.monetization.settle_invoice(invoice_id=args.invoice_id)
    output = {"invoice_id": args.invoice_id, "settled": bool(ok)}
    sys.stdout.write(json.dumps(output) + "\n")


def cmd_issue_l402(args: argparse.Namespace, service: SecureService) -> None:
    token = service.monetization.issue_l402_token(
        resource_id=args.resource_id,
        ttl_seconds=args.ttl,
    )
    output = {
        "token": token.token,
        "resource_id": token.resource_id,
        "expires_at_ns": token.expires_at_ns,
    }
    sys.stdout.write(json.dumps(output) + "\n")


def _read_payload_from_args(args: argparse.Namespace) -> bytes:
    if args.input == "-":
        data = sys.stdin.buffer.read()
    else:
        with open(args.input, "rb") as f:
            data = f.read()
    return data


def cmd_sensitive_transform(args: argparse.Namespace, service: SecureService) -> None:
    payload = _read_payload_from_args(args)
    result = service.sensitive_transform(
        payload=payload,
        context=args.context,
        resource_id=args.resource_id,
        l402_token=args.l402_token,
    )
    sys.stdout.write(json.dumps(result) + "\n")


def cmd_sensitive_add(args: argparse.Namespace, service: SecureService) -> None:
    a = _read_payload_from_args(args)
    if args.input_b == "-":
        b = sys.stdin.buffer.read()
    else:
        with open(args.input_b, "rb") as f:
            b = f.read()
    result = service.sensitive_add_encrypted(
        a_plain=a,
        b_plain=b,
        context=args.context,
        resource_id=args.resource_id,
        l402_token=args.l402_token,
    )
    sys.stdout.write(json.dumps(result) + "\n")


def cmd_show_log(args: argparse.Namespace, service: SecureService) -> None:
    records = service.c0_logger.get_log()
    data = [
        {
            "signature": r.signature,
            "context": r.context,
            "timestamp_ns": r.timestamp_ns,
        }
        for r in records
    ]
    sys.stdout.write(json.dumps(data) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local-only secure app with C=0 logging, FHE stubs, and monetization stubs."
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("create-invoice", help="Create Lightning invoice (stub)")
    p_inv.add_argument("--amount", type=int, required=True, help="Amount in sats")
    p_inv.add_argument("--description", type=str, required=True, help="Description")
    p_inv.set_defaults(func=cmd_create_invoice)

    p_settle = sub.add_parser("settle-invoice", help="Settle Lightning invoice (stub)")
    p_settle.add_argument("--invoice-id", type=str, required=True)
    p_settle.set_defaults(func=cmd_settle_invoice)

    p_l402 = sub.add_parser("issue-l402", help="Issue L402 token (stub)")
    p_l402.add_argument("--resource-id", type=str, required=True)
    p_l402.add_argument("--ttl", type=int, default=3600, help="TTL in seconds")
    p_l402.set_defaults(func=cmd_issue_l402)

    p_st = sub.add_parser(
        "sensitive-transform", help="Run sensitive transform with C=0 log and FHE stub."
    )
    p_st.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input file path or '-' for stdin",
    )
    p_st.add_argument("--context", type=str, required=True)
    p_st.add_argument("--resource-id", type=str, required=True)
    p_st.add_argument("--l402-token", type=str, default=None)
    p_st.set_defaults(func=cmd_sensitive_transform)

    p_sa = sub.add_parser(
        "sensitive-add",
        help="Encrypt two payloads and perform FHE-stub add with C=0 log.",
    )
    p_sa.add_argument(
        "--input",
        type=str,
        required=True,
        help="First input file path or '-' for stdin",
    )
    p_sa.add_argument(
        "--input-b",
        type=str,
        required=True,
        help="Second input file path or '-' for stdin",
    )
    p_sa.add_argument("--context", type=str, required=True)
    p_sa.add_argument("--resource-id", type=str, required=True)
    p_sa.add_argument("--l402-token", type=str, default=None)
    p_sa.set_defaults(func=cmd_sensitive_add)

    p_log = sub.add_parser("show-log", help="Show in-memory C=0 log records")
    p_log.set_defaults(func=cmd_show_log)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = SecureService()
    args.func(args, service)


if __name__ == "__main__":
    main()
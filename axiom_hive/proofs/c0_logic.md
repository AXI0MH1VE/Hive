# C=0 Signature Logic

C=0 signatures are deterministic, local-only signatures designed for audit trails in sensitive operations.

## Definition

A C=0 signature is computed as HMAC-SHA256(secret_key, context + payload), where:

- `secret_key`: Local 32-byte random key, never leaves the process.
- `context`: String label for the operation.
- `payload`: Bytes of the data being signed.
- `timestamp_ns`: Nanosecond timestamp for ordering.

## Properties

- **Deterministic**: Same inputs yield same signature.
- **Local**: No external verification; for internal audit.
- **Secure**: Uses HMAC for integrity.

## Proof of Correctness

Assuming HMAC-SHA256 is collision-resistant, the signature uniquely identifies the payload under the context.

Verification: Recompute HMAC and compare.

No mathematical proof provided; this is a stub for formal proofs.

## FHE Stubs

FHE (Fully Homomorphic Encryption) stubs for Deoxys and CKKS are placeholders. Real implementations would require cryptographic proofs of security.

- Encryption: Simple XOR obfuscation (not secure).
- Decryption: Inverse XOR.
- Eval operations: Placeholder arithmetic.

For production, integrate proven FHE libraries.

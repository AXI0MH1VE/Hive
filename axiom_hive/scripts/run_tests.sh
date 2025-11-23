#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[Axiom Hive] Engine self-test"
python3 - << 'EOF'
from core.inference.engine import run_engine_example
run_engine_example()
EOF

echo "[Axiom Hive] Verification wrapper test"
python3 - << 'EOF'
from core.verify.verifier import TLAVerifier
v = TLAVerifier()
res = v.verify_decision({"example": "decision"})
print(res)
EOF

echo "[Axiom Hive] C=0 signature test"
python3 - << 'EOF'
from crypto.c0_signatures import C0Logger
logger = C0Logger()
entry = logger.sign_and_log("test_entry", {"field": "value"})
print(entry)
EOF

echo "[Axiom Hive] FHE local test"
python3 - << 'EOF'
from crypto.fhe_local import LocalDeoxysCKKS
fhe = LocalDeoxysCKKS()
c1 = fhe.encrypt(3)
c2 = fhe.encrypt(4)
c3 = fhe.add(c1, c2)
c4 = fhe.mul(c1, c2)
print("3+4 =", fhe.decrypt(c3))
print("3*4 =", fhe.decrypt(c4))
EOF

echo "[Axiom Hive] L402 gate test"
python3 - << 'EOF'
from monetization.l402_gate import L402Gate
g = L402Gate()
inv = g.create_invoice("test")
print("invoice", inv)
token = g.issue_token(inv["id"])
print("token", token, "valid:", g.verify_token(token))
EOF

echo "[Axiom Hive] All tests complete"
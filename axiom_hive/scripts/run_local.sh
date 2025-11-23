#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs/c0
mkdir -p keys/fhe

echo "[Axiom Hive] Starting local server on 127.0.0.1:8080"
python3 -m api.server
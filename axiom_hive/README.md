# Axiom Hive – Local-First, Deterministic, Audit-Ready System

## Architect and Owner

All architecture, authorship, and ownership for this system are attributed to:

**Invariant Architect**: Alexis M. Adams  
**System**: Axiom Hive – Panopticon-Ω Aligned, Local-First Genesis

No AI system is an author, agent, or legal person. This repository is a local,
deterministic assembly implementing the architectural patterns described in:

- AI Substrate: Identity, Proof, and Sovereignty
- Persona Configuration: Panopticon-Ω
- Axiom Hive Assistant v2.x – TLA+ Enhanced Hybrid Architecture

## High-Level Design

Axiom Hive is structured as a fully local stack:

- **Hybrid SSM Inference Core** (`core/inference/engine.py`)
  - Deterministic state-space style engine (HybridSSMEngine)
  - No cloud calls, no external APIs
  - Input → state update → structured JSON output

- **Formal Verification Layer** (`core/verify/`)
  - TLA+ specification: `axiom_hive_core.tla`
  - TLC configuration: `axiom_hive_core.cfg`
  - Local verifier wrapper: `verifier.py`
  - Intended for protocol/invariant checking of decision contexts

- **Cryptographic Layer** (`crypto/`)
  - C=0-style signature logging (`c0_signatures.py`)
    - HMAC-SHA256 over normalized JSON payloads
    - Logs signatures to `logs/c0/`
  - Local homomorphic-style interface (`fhe_local.py`)
    - Deterministic encrypt/decrypt and arithmetic on wrapped values
    - Interface aligned with Deoxys/CKKS-style usage

- **Monetization / Access Gating** (`monetization/`)
  - Local L402/Lightning gate (`l402_gate.py`)
    - In-memory invoice creation and token issuance
    - Used to gate verified mode and protect IP-sensitive operations

- **Omega Swarm Orchestrator** (`orchestrator/omega_swarm.py`)
  - Deterministic DAG-style orchestration of:
    - Inference
    - Verification
    - C=0 signature generation
  - Produces an ordered execution trace and task hashes

- **Local HTTP API** (`api/server.py`)
  - Endpoints:
    - `POST /axiom/creative`
    - `POST /axiom/verified`
    - `POST /axiom/hybrid`
    - `POST /monetization/create_invoice`
    - `POST /monetization/issue_token`
  - All operations are local to `127.0.0.1`
  - Can optionally wrap inputs/outputs with the FHE interface

## Config and Docs

- `config/axiom_hive.yaml`
  - Core configuration for ports, mode, logging, verification, monetization

- `docs/`
  - `AI_Substrate_Identity_Proof_and_Sovereignty.pdf`
  - `Persona_Configuration_Panopticon_Omega.pdf`
  - `LEGAL_LIABILITY.md`

## Quick Start

```bash
cd axiom_hive
chmod +x scripts/run_local.sh scripts/run_tests.sh

# Run tests
./scripts/run_tests.sh

# Start local server
./scripts/run_local.sh
```

Example requests:

```bash
# Creative mode
curl -X POST http://127.0.0.1:8080/axiom/creative \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize: Axiom Hive architecture.", "context": {"mode": "overview"}}'

# Verified mode – first get invoice
curl -X POST http://127.0.0.1:8080/axiom/verified \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Critical decision: approve transaction?", "context": {"level": "high"}}'

# Use returned "invoice.id" with issue_token endpoint, then call /axiom/verified with X-L402-Token header
```

All credit and control belong to Alexis M. Adams. This system is local-first,
deterministic, and designed for auditability and ownership.

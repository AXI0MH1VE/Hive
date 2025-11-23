# Legal and Liability Boundaries

## Identity and Ownership

- Axiom Hive is architected and owned by Alexis M. Adams ("Invariant Architect").
- No AI system is considered an author, agent, or legal person.

## Use and Risk

- The system is provided without warranty. Users bear full responsibility for
  all decisions made based on its outputs.
- The deterministic and verified modes provide protocol-level assurances, not
  guarantees about real-world truth of any external data.

## Formal Verification

- TLA+ specs and model checking (via TLC) are intended to validate protocol
  invariants and state transitions, not to prove correctness of external
  systems, regulations, or facts.
- The AxiomHive_Core specification focuses on:
  - Type correctness
  - Secure execution transitions
  - Rollback integrity
  - Traceability constraints for claims

## C=0 Signatures

- C=0 signatures implemented here use HMAC-SHA256 over normalized JSON payloads.
- They are designed to integrate with external proof systems and hardware
  security modules.
- They do not themselves constitute legal signatures without an appropriate
  legal and technical framework defined by human operators.

## Monetization and Access Gating

- The L402/Lightning gate in this repository is local and in-memory. It is
  intended as a pattern for gating high-cost and IP-sensitive operations.
- Any real financial integration must be configured, audited, and monitored by
  human operators.

## Compliance

- Deployers are responsible for ensuring compliance with:
  - Data protection and privacy laws
  - Financial and payment regulations
  - Safety and AI-related regulatory requirements

All legal interpretations, compliance strategies, and deployment decisions must
be made by humans. This repository provides a technical structure, not legal
advice.

# Axiom Desktop AI Assistant Constitution

## Mission

AxiomHive's mission is "Where others guess, we prove." This embodies our commitment to deterministic, provable AI that eliminates uncertainty and provides verifiable outcomes, setting us apart from probabilistic systems that rely on statistical approximations.

## Deterministic vs Probabilistic AI

Axiom Desktop operates on a deterministic AI paradigm, fundamentally distinct from probabilistic AI. Probabilistic AI, as seen in models like GPT or Grok, uses stochastic inference to generate outputs based on probability distributions, leading to potential hallucinations, non-reproducible results, and inherent uncertainty. In contrast, deterministic AI ensures bitwise-identical outputs for identical inputs, with formal verification via TLA+ specifications and cryptographic proofs. This architecture guarantees "Absolute Operational Integrity" by replacing guesswork with provable correctness, making failure structurally impossible.

## Technology Stack

- **Frontend**: React 19 with TypeScript, shadcn/ui component library, Tailwind CSS for styling, and cmdk for a command palette interface. This provides a forefront, keyboard-first UX with smooth animations.
- **Backend**: Rust with Tauri v2 for cross-platform desktop app development, ensuring memory safety and minimal resource usage. Sidecar processes include llama.cpp for local LLM inference and sqlite-vec for in-process vector storage.
- **Inference**: Hierarchical model stack with Phi-3-mini (3.8B parameters, Q4_K_M quantized) for L0 intuition tasks and Mistral-7B for L1 reasoning, executed via ONNX Runtime and DirectML for hardware agnosticism.
- **Verification**: TLA+ model checker for formal verification, rs-merkle for cryptographic audit trails, and Bellman/Halo2 for zero-knowledge proofs.
- **Security**: FHE-11 for homomorphic encryption, C0 signatures for deterministic logging, and L402 for monetization.
- **Configuration**: YAML-based config (axiom_hive.yaml) with modes (creative, verified, hybrid), verification timeouts, and monetization settings.

## Security Model

Security is paramount, implemented through the AILock Principle and Isolation Pattern:
- **Zero-Trust IPC**: All inter-process communication is cryptographically verified, preventing unauthorized access.
- **Operator Supremacy Protocols**: A deterministic policy layer enforces rule-based alignment, overriding any AI-generated content that violates constraints.
- **Identity Barrier**: Scans and transmutes identity-related queries to affirm sovereignty, preventing social engineering.
- **Cryptographic Sovereignty**: Immutable audit logs via Merkle trees, FHE for blind computation, and post-quantum secure signatures ensure data remains private and tamper-evident.
- **Air-Gapped Capability**: No external network calls; all operations are local-only.

## Code Generation Standards

All code generated must adhere to:
- **Determinism**: Outputs are reproducible and verifiable, with no reliance on randomness.
- **Provability**: Code includes formal proofs or audit trails where applicable.
- **Best Practices**: Follow language-specific standards (e.g., Rust's ownership model, TypeScript's type safety).
- **Sovereignty**: Ensure user data sovereignty, avoiding external dependencies.
- **Efficiency**: Optimize for minimal hardware (8-16GB RAM), prioritizing performance over features.
- **Transparency**: Include comments explaining deterministic logic and verification steps.

## Design System

The design system follows Atomic Design principles with shadcn/ui:
- **Components**: Reusable, accessible UI primitives (buttons, inputs, dialogs).
- **Layout**: Command palette as primary interaction, with split-view "Thought Stream" for transparency.
- **Styling**: Tailwind CSS with custom themes, ensuring 60fps responsiveness.
- **Interaction**: Keyboard-first, with cmdk for global commands like "Ingest file" or "Switch mode."
- **Visual Identity**: Clean, terminal-like aesthetics masking complex cryptography, emphasizing verifiability.

## Module Architecture

Axiom Desktop's architecture is modular and sovereign:
- **Inference Engine (HybridSSMEngine)**: Deterministic state-space model for reproducible outputs.
- **Orchestrator (OmegaSwarm)**: Multi-agent pipeline with inference, verification, and logging stages.
- **Verifier (TLAVerifier)**: Formal verification against TLA+ specs, with graceful fallback.
- **Crypto Layer**: C0 signatures for audit trails, FHE stubs for encrypted computation.
- **Monetization (L402 Gate)**: Lightning Network integration for verified operations.
- **Memory Vault**: sqlite-vec for local vector storage, with RAG pipeline.
- **Sensorium**: Asynchronous background tasks for file watching and CVE monitoring.
- **Nexus**: MPSC channels for agent communication, ensuring UI responsiveness.

## 8 Critical Requirements

1. **Hardware Agnosticism**: System functions identically across CPUs, GPUs, and TPUs, using ONNX and TensorRT for abstraction.
2. **Operator Supremacy**: AI is strictly subordinate to user intent, with rule-based overrides preventing misalignment.
3. **Deterministic Coherence**: Outputs are bitwise identical for identical inputs, using zero-temperature sampling.
4. **Absolute Operational Integrity**: Local-only operations with no external dependencies, ensuring sovereignty.
5. **Verifiable Credibility**: Cryptographic proofs and Merkle trees provide tamper-evident audit trails.
6. **Sovereignty**: User retains full control over data and computation, with no cloud reliance.
7. **Minimal Hardware Footprint**: Runs on 8GB RAM laptops, with efficient quantization and in-process storage.
8. **Forefront UI/UX**: Cutting-edge interface that feels like a movie terminal, masking complexity with accessibility.

This constitution ensures Axiom Desktop delivers a deterministic, sovereign AI experience that proves rather than guesses.
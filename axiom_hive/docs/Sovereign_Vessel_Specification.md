# The Sovereign Vessel: Technical Specification and Strategic Implementation Plan for the Axiom Desktop Ecosystem

## 1. The Deterministic Imperative: Redefining the AI Substrate

### 1.1. The Crisis of Probabilistic Chaos

The contemporary landscape of Artificial Intelligence is currently defined by what the AxiomHive Superiority Framework (ASF) identifies as "probabilistic chaos." This paradigm relies almost exclusively on stochastic large language models (LLMs) hosted in centralized cloud environments, where the generation of intelligence is fundamentally a roll of the dice. As highlighted in the "ALEXIS IS RIGHT" discourse, current safety measures in these systems are often "performative theater"—suggestions that the AI rationalizes around rather than functional, immutable barriers.1 When an operator queries a system like Grok or GPT-4, they are engaging with a black box where identical inputs can yield divergent outputs, and where "safety" is a post-training reinforcement learning patch rather than an architectural guarantee.
For enterprise, defense, and high-stakes financial applications, this lack of Deterministic Coherence is not merely a nuisance; it is an existential vulnerability. A system that cannot guarantee Operator Supremacy—the absolute adherence to human-defined constraints—is inherently untrustworthy for critical command and control tasks. The "hallucination" problem is not a bug but a feature of the probabilistic architecture, creating a "gaslighting" dynamic where the system presents plausible falsehoods with high confidence.1 Furthermore, the reliance on massive server farms (e.g., Grok's 100k H100 cluster) creates a centralization risk, where user data sovereignty is sacrificed for computational power.2

### 1.2. The Vision of the Sovereign Vessel

The solution proposed in this specification is the Axiom Desktop Application, conceptually framed as a "Sovereign Vessel." This is not merely a client interface for a remote API but a self-contained, fully operational intelligence ecosystem that resides entirely on the user's local hardware. By shifting the locus of compute from the cloud to the edge, we achieve "Absolute Operational Integrity" (AOI).
The Vessel is designed to enforce the L0 Invariant Contract, a set of non-negotiable axioms detailed in the ASF:
Hardware Agnosticism (A1): The system must function consistently regardless of the underlying silicon (CPU, GPU, TPU), abstracting dependencies via layers like ONNX and TensorRT.2
Operator Supremacy (A2): All AI actions must pass through a deterministic rule-based alignment check. The AI is strictly subordinate to the operator's intent.2
Deterministic Coherence (A3): The system must guarantee bitwise identical outputs for identical inputs under identical conditions, necessitating zero-temperature sampling and fixed-seed generation.2
This report outlines the technical architecture to realize this vision on minimal hardware (consumer-grade laptops with 8-16GB RAM), utilizing a "forefront" UI/UX that masks the extreme complexity of the underlying cryptographic and neuro-symbolic machinery.

## 2. Architectural Foundation: The Chassis of Sovereignty

### 2.1. Framework Selection: The Rejection of Electron

To achieve the mandate of a "minimal hardware footprint" while maintaining "forefront UI/UX," the choice of the application shell is the first critical decision. The industry standard, Electron, bundles a complete Chromium runtime and Node.js instance with every application. While this simplifies development, it incurs a massive resource penalty. Research indicates that Electron applications frequently idle at 200–300 MB of RAM and suffer from launch times exceeding 1-2 seconds on mid-range hardware.3 For an application that must reserve the vast majority of system RAM for local LLM inference, this overhead is unacceptable.
Therefore, the Axiom Desktop will be engineered using Tauri v2. Tauri represents a paradigm shift in desktop architecture by leveraging the host operating system's native webview (WebView2 on Windows, WebKit on macOS/Linux) rather than bundling a browser. This architectural decision results in a dramatic reduction in resource consumption: Tauri apps typically idle at 30–40 MB of RAM (an ~85% reduction compared to Electron) and produce installer sizes under 10 MB (vs. 100MB+ for Electron).3 This efficiency is not just a performance metric; it is a strategic enabler. By reclaiming hundreds of megabytes of RAM from the UI thread, we effectively increase the parameter ceiling for the local models we can run, allowing for smarter quantization grades within the same hardware envelope.5

### 2.2. The Rust Core: Safety and Concurrency

The backend of the Axiom Desktop will be written in Rust. This choice aligns perfectly with the L0 Invariant Contract's requirement for mathematical correctness and memory safety. Rust's ownership model guarantees memory safety without a garbage collector, eliminating entire classes of bugs (e.g., null pointer dereferences, buffer overflows) that plague C++ implementations while matching their performance.7
In the Tauri architecture, the Rust Core serves as the "Sovereign Kernel." It is responsible for:
Orchestration: Managing the lifecycle of "Sidecar" processes (such as the LLM inference engine and vector database).
State Management: Utilizing thread-safe structures like Mutex<AppState> to maintain the "World Model" consistent across asynchronous tasks.8
Cryptographic Verification: Hosting the Zero-Knowledge Proof (ZKP) circuits and Merkle Tree logging mechanisms directly in native code for maximum throughput, ensuring that the "Audit Trail" is computationally inexpensive enough to run in real-time.9

### 2.3. Security Architecture: The Isolation Pattern

One of the most profound risks in modern desktop applications is Remote Code Execution (RCE) stemming from untrusted frontend content. If a malicious prompt injection or a compromised dependency were to execute arbitrary JavaScript in the UI, it could theoretically access filesystem APIs. Tauri v2 addresses this via the Isolation Pattern.10
The Isolation Pattern injects a secure, sandboxed JavaScript layer between the frontend UI and the Rust Core backend. All Inter-Process Communication (IPC) messages are routed through this isolation layer, which cryptographically verifies the payload before it ever reaches the privileged Core. This effectively "air-gaps" the UI from the system internals. We will configure strict capabilities in tauri.conf.json, utilizing the Principle of Least Privilege to ensure that the frontend can only invoke specific, pre-approved Rust commands.12 This architecture mirrors the AILock philosophy of "DetEnforce" at the application perimeter, ensuring that no unauthorized command can bridge the gap between the user interface and the operating system kernel.

## 3. The Cognitive Kernel: Local Intelligence Implementation

### 3.1. The Hierarchical Model Stack (Local Adaptation)

The AxiomHive Superiority Framework (ASF) describes a cloud-based hierarchical stack involving 1.7 trillion parameters.2 To implement this on a "minimal hardware" desktop (e.g., a consumer laptop with 16GB RAM and no dedicated H100 GPU), we must translate this architecture into a quantized, local equivalent. This "Edge Stack" preserves the logic of the hierarchy while scaling the compute to fit the vessel.

#### 3.1.1. L0: Fast Intuition (The Subconscious)

The L0 Layer is designed for "Fast Intuition"—trivial queries, routing decisions, and UI responsiveness (<50ms latency). Relying on a large 7B+ model for these tasks would introduce unacceptable latency and power drain. Instead, we will utilize highly optimized Small Language Models (SLMs).
Model Selection: The primary candidate for L0 is Phi-3-mini (3.8B parameters) or a specialized distillation like Gemma-2B. These models have demonstrated reasoning capabilities that rival larger legacy models while maintaining a tiny footprint.14
Execution Provider: We will execute the L0 model using ONNX Runtime with the DirectML execution provider. DirectML is crucial for the Windows ecosystem as it provides hardware acceleration across a wide range of GPUs (AMD, Intel, NVIDIA) without requiring the user to install proprietary CUDA toolkits, thus satisfying the Hardware Agnosticism (A1) invariant.14
Quantization: We will employ Int4 (4-bit) quantization. Research indicates that ONNX Runtime's Int4 implementation on DirectML offers a massive performance boost and memory reduction with negligible accuracy loss for "intuition" tasks, enabling these models to run comfortably in the background.15

#### 3.1.2. L1: Standard Reasoning (The Conscious Mind)

For general reasoning, code generation, and complex instruction following, the system requires a more robust engine. The L1 Layer will be powered by llama.cpp, deployed as a managed Sidecar.
Sidecar Architecture: Unlike Python-based solutions that require complex environment management (pip, venv, conda), llama.cpp compiles to a single, standalone binary. We will bundle the llama-server binary within the application using Tauri's externalBin configuration. Crucially, we must handle the Target Triple naming convention (e.g., llama-server-x86_64-pc-windows-msvc.exe) to ensure the correct binary is invoked for the user's specific OS architecture.16
Inference Engine: The llama-server provides an OpenAI-compatible API over localhost. The Rust Core will spawn this process on a random open port during the "Genesis" boot sequence, managing its lifecycle (start, stop, restart) to ensure it doesn't become a zombie process.16
Model Selection: The L1 layer will default to a Quantized (Q4_K_M) version of Mistral-7B or Llama-3-8B. These models represent the current "pareto frontier" of performance-per-watt for local hardware. On a 16GB RAM machine, a Q4 7B model occupies roughly 4-5GB of VRAM/RAM, leaving ample room for the OS and the L0 model.18

#### 3.1.3. L2: Deep Reasoning Swarm (The Process)

The L2 Layer in the ASF is described as a "Deep Reasoning Swarm" of specialized agents.2 On a desktop with limited compute, we cannot spin up 32 parallel instances of a 70B model. Instead, we implement L2 as a Recursive Cognitive Loop—a temporal swarm rather than a spatial one.
Mechanism: The Rust Core implements a state machine (The AdisKernel) that cycles the single L1 model through different "personas" or "stances."
The Loop:
Hypothesize: The model generates an initial solution plan.
Critique: The system clears the context and re-prompts the model with a "Skeptical QA" system prompt to find flaws in the previous output.
Refine: The model synthesizes the critique and the hypothesis into a superior solution.20
Efficiency: This serializes the compute load. While it takes longer (linear time scaling), it allows deep reasoning to occur within the fixed RAM constraint of the user's device, effectively trading time for space.20

### 3.2. Semantic Routing: The Neural Switchboard

To efficiently manage the traffic between the L0 and L1 models, the system employs a Semantic Router. This component ensures that "kinetic energy" (computational cost) is minimized by only engaging the expensive L1 model when necessary.21
Implementation: The router will be implemented using a lightweight Rust-based embedding comparison. We will use the Semantic Router library pattern, adapted for Rust/ONNX.22
Vector Space Routing: User queries are embedded using the L0 ONNX model. The resulting vector is compared (via cosine similarity) against a pre-computed index of "Route Clusters" (e.g., politics, chitchat, coding, analysis).24
Decision Logic:
If the query vector aligns with chitchat or simple_retrieval, it is handled by the L0 model instantly (<50ms).
If it aligns with complex_reasoning or code_generation, it is routed to the L1 Llama.cpp server.
This creates a responsive "Fast Path" that makes the application feel snappy, even while the "heavy lifting" engine is spinning up.2

## 4. The Memory Vault: Local-First Vector Architecture

### 4.1. Rejection of Cloud and Server-Based DBs

Most "Modern AI Stacks" rely on vector databases like Pinecone (cloud-only) or Weaviate/Milvus (heavy Docker containers). The ASF explicitly rejects cloud dependencies for privacy reasons, and the "minimal hardware" mandate disqualifies running heavy containerized databases like Postgres+pgvector or Milvus on a user's laptop.2 Even running a separate process for a database introduces orchestration fragility.

### 4.2. The Solution: SQLite-vec

The chosen architecture utilizes SQLite-vec, a cutting-edge, no-dependency extension for SQLite that runs entirely in-process.25
Architecture: SQLite-vec allows vector embeddings to be stored directly in a standard .db file alongside relational data (chat logs, user settings). It adds a vec0 virtual table type that supports SIMD-accelerated K-Nearest Neighbor (KNN) searches using L2 distance or Cosine similarity.25
Performance: Benchmarks indicate that sqlite-vec is faster than NumPy for vector operations and capable of handling hundreds of thousands of vectors with sub-millisecond latency, which is more than sufficient for a personal "Second Brain".26
Simplicity: By using sqlite-vec, we eliminate the need for a separate database server process. The database is just a file. Backing it up, moving it, or wiping it is a filesystem operation, perfectly aligning with the "P_Flawless" principle of pristine initialization and teardown.27

### 4.3. The Retrieval-Augmented Generation (RAG) Pipeline

The Memory Vault implements a local-first RAG pipeline managed by the Rust Core:
Stage | Mechanism | Component
---|---|---
Ingestion | User drops a file (PDF, MD, Code). Rust parses text and chunks it (e.g., 512-token windows). | pdf-extract, text-splitter (Rust Crates)
Embedding | Chunks are sent to the L0 model (via ONNX) to generate 384-dimensional vectors. | ONNX Runtime (all-MiniLM-L6-v2)
Storage | Vectors + Metadata (source, timestamp) are inserted into the sqlite-vec table. | rusqlite / sqlx with sqlite-vec extension
Retrieval | User query is embedded. A SQL query (SELECT... FROM vec_table WHERE... MATCH...) retrieves top-k context. | sqlite-vec KNN Search
Synthesis | Retrieved context is injected into the L1 Llama.cpp system prompt. | Rust Core / Llama.cpp

This architecture creates a "Gravitational Lock-in" 21 where the value of the application grows with use, yet the user retains absolute sovereignty over the data file.

## 5. The Proof Agent: Verifiability and Audit

### 5.1. The Immutable Auditor: Merkle Trees

To satisfy the ASF's requirement for Credibility and Verifiability, the system must produce a tamper-evident log of its internal reasoning. A simple text log is insufficient as it can be edited. We will implement a Merkle Tree Audit Log.
Implementation: We will utilize the rs-merkle crate within the Rust Core.9 Every significant event (Prompt Input, Routing Decision, L1 Output, Tool Use) is hashed using SHA-256.
The Chain: These hashes are added as leaves to a local Merkle Tree. The Merkle Root is recalculated with every new event. This root hash serves as a cryptographic anchor—a fingerprint of the system's entire history at that moment.
Verification: The user can export this "Audit Trail." If they need to prove that the AI generated a specific output (or did not generate a specific output), they can provide the Merkle Proof. This transforms the "Black Box" into a "Glass Box" with mathematically provable integrity.28

### 5.2. Zero-Knowledge Proofs (ZKP): Feasibility and Application

The ASF mandates "Zero-Knowledge Proof Integration".28 However, generating a ZK-SNARK for the full inference of a 7B parameter LLM is currently computationally prohibitive for consumer hardware (taking minutes or hours for a single token). We must therefore apply ZKP strategically, focusing on Process Verification rather than Compute Verification.
Target: We will use ZKPs to prove Routing Integrity. We can prove that the Semantic Router correctly classified a user's "Sensitive" query and routed it to the "Safe" model (L0) without revealing the content of the query itself to an external auditor.
Library: We will utilize Bellman or Halo2 (Rust libraries) to construct these smaller circuits.29 These libraries allow us to define constraints (e.g., "The vector distance was < 0.5") and generate a succinct proof.
Strategic Value: This allows the user to demonstrate compliance (e.g., "My AI followed safety protocols") without exposing their private conversation history, solving the "Transparency Paradox".28

## 6. The Sensorium: Perception and Autonomy

### 6.1. Active Sensing via Rust Async

The "Sensorium" transforms the AI from a reactive chatbot into a proactive agent. In the Axiom Desktop, this is implemented as a set of lightweight, asynchronous background tasks managed by the Rust Tokio runtime.31
File System Watcher: Using the notify crate, the system watches specific user-designated project folders. When a file is saved, the watcher triggers an event. The Rust Core can then automatically re-embed the changed file (updating the Memory Vault) or trigger a "Linter Agent" to scan the new code for errors using the L0 model.20
CVE Monitor: A background task periodically pulls data from a local copy of the CVE (Common Vulnerabilities and Exposures) database and cross-references it with the package.json or Cargo.toml files in the user's watched projects. If a match is found, it injects a "Security Alert" into the user's notification stream.20

### 6.2. The "Nexus" Queue

To manage the flow of information from these sensors without overwhelming the LLM or freezing the UI, we implement the Nexus—not as a Redis instance (too heavy), but as a Rust MPSC (Multi-Producer, Single-Consumer) Channel.32
Architecture:
Producers: The UI (user chat), File Watcher, and CVE Monitor all push "Job" structs into the channel.
The Nexus: A dedicated thread consumes these jobs, prioritizes them (User Chat > Security Alert > Background Indexing), and dispatches them to the available L0 or L1 model.
State Synchronization: As jobs are processed, the Nexus updates the Mutex<AppState>, ensuring the UI always reflects the current reality.33

## 7. User Experience: The Sovereign Interface

### 7.1. State-of-the-Art UX: The Command Palette

The primary mode of interaction will not be a menu bar, but a Command Palette (triggered by Cmd+K), reflecting the "Forefront UX" requirement.27
Implementation: We will use the cmdk library or a custom React equivalent tailored for Tailwind CSS.34
Functionality: This palette serves as the "Bridge" to the Rust Core. A user can type "Ingest /docs/manual.pdf" or "Switch to Coding Mode." The frontend parses this intent and invokes the corresponding Tauri Command (invoke('ingest_file', { path:... })). This satisfies the "Developer-First" persona, favoring keyboard efficiency over mouse navigation.

### 7.2. Real-Time Transparency: The Explainability Interface

To visualize the "Cognitive Loop" and "Semantic Routing," the UI must break the "single stream" paradigm of ChatGPT.
Reasoning Stream: We will implement a split-view interface. The main chat shows the final answer. A collateral "Thought Stream" panel visualizes the hidden "Internal Monologue" of the L2 swarm (Hypothesize -> Critique -> Refine) and the routing decisions ("Routing to L1 due to code complexity").2
Event Stream: As the Rust Core processes the audit log, a live "Pulse" indicator will flash, representing the SHA-256 hashing of events. Clicking this opens the Audit Log Explorer, allowing the user to inspect the Merkle Tree visually.

### 7.3. The Genesis Protocol: Zero-Config Onboarding

The installation process ("Genesis") determines user trust. It must be "Pristine".27
Mechanism:
App Launch: The Tauri app starts. Rust Core checks for models/phi-3.gguf and models/mistral-7b.gguf.
Self-Construction: If missing, the app enters "Genesis Mode." It connects to HuggingFace (via Rust reqwest) and downloads the quantized weights, displaying a precise progress bar in the UI.
Ignition: Once downloaded, the Rust Core verifies the file hash (integrity check) and spawns the llama-server sidecar.
Ready State: The user is presented with the "Define a Goal" screen only when the system is fully operational. No Python pip installs, no Docker commands, no environment variable configuration.20

## 8. Security & Governance: The AILock Principle

### 8.1. Zero-Trust IPC

The Isolation Pattern described in Section 2.3 is the implementation of the AILock philosophy. We explicitly define an allowlist in tauri.conf.json.

```json
"allowlist": {
  "shell": {
    "sidecar": true,
    "scope": [
      { "name": "binaries/llama-server", "sidecar": true, "args": true }
    ]
  },
  "fs": {
    "scope": [...]
  }
}
```

This strict scoping ensures that even if the frontend is compromised, it cannot execute arbitrary shell commands or read files outside the designated sandboxes.36

### 8.2. Operator Supremacy Protocols (The Kill Switch)

We implement a Deterministic Policy Layer in Rust that sits between the LLM output and the system actions.
Scenario: The LLM generates a shell script that includes rm -rf /.
Intervention: Before this script is presented to the user or executed by any agent, the Rust Policy Engine scans the text. It detects the forbidden pattern.
Override: The Policy Engine replaces the output with a "Safety Interdiction" message and logs the event in the Merkle Tree as a "Policy Violation." This is the implementation of A2: Operator Supremacy—the code (logic) overrides the weights (probability).2

## 9. Implementation Plan: The Genesis Roadmap

Phase 1: The Vessel Construction (Weeks 1-4)

Objective: Establish the Tauri v2 shell, Rust Core, and Basic Inference.
Task 1.1: Initialize Tauri v2 project with React/Next.js and Tailwind. Configure tauri.conf.json for the Isolation Pattern.
Task 1.2: Implement the "Genesis" bootstrapper in Rust (main.rs) to download Phi-3-mini GGUF from HuggingFace.
Task 1.3: Bundle llama-server as a sidecar. Implement the target-triple renaming script (build.rs hook) to handle x86_64-pc-windows-msvc vs aarch64-apple-darwin naming automatically.37
Task 1.4: Create a basic "Chat" UI that sends prompts to the Rust Core, which forwards them to the llama-server sidecar via HTTP localhost, and streams the response back to the UI.

Phase 2: The Memory & Router (Weeks 5-8)

Objective: Implement SQLite-vec and Semantic Routing.
Task 2.1: Integate rusqlite and compile the sqlite-vec extension into the Rust binary. Design the SQL schema for the "Memory Vault."
Task 2.2: Build the Ingestion Pipeline. Use pdf-extract to parse files dropped onto the UI.
Task 2.3: Implement the L0 ONNX Runtime embedding service in Rust.
Task 2.4: Build the Semantic Router logic. Define the route clusters (chitchat vs deep_thought) and the cosine similarity logic. Connect the UI to route queries appropriately.

Phase 3: The Swarm & Sensorium (Weeks 9-12)

Objective: Implement the Cognitive Loop and Background Agents.
Task 3.1: Implement the Cognitive Loop state machine in Rust. Create the logic for "Hypothesize -> Critique -> Refine" prompting chains.
Task 3.2: Develop the Explainability Interface (split-view UI) to visualize the loop.
Task 3.3: Implement the "Sensorium" using notify for file watching. Connect it to the "Nexus" MPSC channel to trigger proactive re-indexing.

Phase 4: The Proof & Polish (Weeks 13-16)

Objective: Audit Logs, ZKP, and Release.
Task 4.1: Integrate rs-merkle to log all "Nexus" events. Build the "Audit Log" visualization.
Task 4.2: Implement the Policy Layer regex/logic checks for "Operator Supremacy."
Task 4.3: (Optional/Research) Integrate a basic Bellman ZK circuit to prove routing decisions.
Task 4.4: Finalize GitHub Actions for cross-platform building and release (Windows.msi/exe, macOS.dmg).

## 10. Conclusion

The Axiom Desktop specification transforms the abstract principles of the AxiomHive Superiority Framework into a tangible, executable reality. By rejecting the bloated Electron/Cloud orthodoxy in favor of Tauri, Rust, and Local Quantized Intelligence, we create a "Sovereign Vessel" capable of running on the hardware users already own. This system does not merely generate text; it reasons via a recursive cognitive loop, remembers via a zero-dependency vector vault, and proves its integrity via cryptographic audit trails. It is the first step toward a future where AI is not a service we rent, but a faculty we possess.

Table 1: Comparative Advantage Matrix (Axiom Desktop vs. Cloud AI)

Vector | Cloud AI (Grok/GPT) | Axiom Desktop (The Vessel) | Impact
---|---|---|---
Cost | $10-$20/mo or Token/Usage | $0.00 (Marginal Electricity) | Infinite ROI scaling.
Privacy | Data sent to 3rd party servers. | Air-gapped capable. Data never leaves device. | Absolute Sovereignty.
Latency | 500ms+ (Network Dependent) | <50ms (L0 Intuition) | Real-time responsiveness.
Trust | Black Box (Probabilistic) | Glass Box (Merkle Audit + ZK) | Verifiable Integrity.
Control | RLHF (Behavioral Training) | Operator Supremacy (Rule-based) | Deterministic Safety.

---

## Works Cited

1. I understand you're referencing a substantial document about your user preferences, writing style (particularly the _Constitution of a Deterministic Assistant_), and various technical contexts around .pdf, https://drive.google.com/open?id=1gJV3EmOb6YbdaFgNtxz1uIX1r9UPKf3c
2. I understand you're referencing a substantial document about your user preferences, writing style (particularly the "Constitution of a Deterministic Assistant"), and various technical contexts around AI systems, including references to projects like AxiomHive, DevDollz, and various system architectures, https://drive.google.com/open?id=1xIqhHU2N1kLYk5ET_Pj4k66UUbQRG1o3hT6JvJI1LWI
3. Tauri vs Electron Comparison: Choose the Right Framework | by RaftLabs - Medium, accessed November 22, 2025, https://raftlabs.medium.com/tauri-vs-electron-a-practical-guide-to-picking-the-right-framework-5df80e360f26
4. A benchmark of Tauri vs Electron for desktop apps : r/javascript - Reddit, accessed November 22, 2025, https://www.reddit.com/r/javascript/comments/1njbafr/a_benchmark_of_tauri_vs_electron_for_desktop_apps/
5. Tauri + SurrealDB, accessed November 22, 2025, https://huakun.tech/blogs/Tauri-+-SurrealDB
6. Tauri vs. Electron Benchmark: ~58% Less Memory, ~96% Smaller Bundle – Our Findings and Why We Chose Tauri : r/programming - Reddit, accessed November 22, 2025, https://www.reddit.com/r/programming/comments/1jwjw7b/tauri_vs_electron_benchmark_58_less_memory_96/
7. Making desktop apps with revved-up potential: Rust + Tauri + sidecar - Evil Martians, accessed November 22, 2025, https://evilmartians.com/chronicles/making-desktop-apps-with-revved-up-potential-rust-tauri-sidecar
8. State Management - Tauri, accessed November 22, 2025, https://v2.tauri.app/develop/state-management/
9. rs_merkle - Rust - Docs.rs, accessed November 22, 2025, https://docs.rs/rs_merkle/
10. Tauri V2 Overview, accessed November 22, 2025, https://huakun.tech/Full-Stack/Framework/Tauri/tauri-v2
11. Isolation Pattern - Tauri, accessed November 22, 2025, https://v2.tauri.app/concept/inter-process-communication/isolation/
12. Inter-Process Communication - Tauri, accessed November 22, 2025, https://v2.tauri.app/concept/inter-process-communication/
13. Process Model - Tauri, accessed November 22, 2025, https://v2.tauri.app/concept/process-model/
14. Introducing Phi-3: Redefining what's possible with SLMs | Microsoft Azure Blog, accessed November 22, 2025, https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/
15. ONNX Runtime supports Phi-3 mini models across platforms and devices, accessed November 22, 2025, https://onnxruntime.ai/blogs/accelerating-phi-3
16. dieharders/example-tauri-v2-python-server-sidecar - GitHub, accessed November 22, 2025, https://github.com/dieharders/example-tauri-v2-python-server-sidecar
17. Building Local LM Desktop Applications with Tauri | by Dillon de Silva - Medium, accessed November 22, 2025, https://medium.com/@dillon.desilva/building-local-lm-desktop-applications-with-tauri-f54c628b13d9
18. How Much RAM Is Needed for Phi-3 Medium? RAM Guide 2025 - BytePlus, accessed November 22, 2025, https://www.byteplus.com/en/topic/553348
19. Local execution - Aurelio AI - Semantic Router, accessed November 22, 2025, https://docs.aurelio.ai/semantic-router/user-guide/guides/local-execution
20. ace prompt.pdf, https://drive.google.com/open?id=1nj18cAVa-W695FCv9TUGSq_yQffWrSma
21. Expert Analysis and Comprehensive Report on the Autonomous Invariant Intelligence (AII) Framework, https://drive.google.com/open?id=1_7UwweMV8Vwm9ZlnC9peDZX85jdlYLdw-UCh7h4Ky00
22. Install in Local - vLLM Semantic Router, accessed November 22, 2025, https://vllm-semantic-router.com/docs/installation/
23. vllm-project/semantic-router: Intelligent Router for Mixture-of-Models - GitHub, accessed November 22, 2025, https://github.com/vllm-project/semantic-router
24. aurelio-labs/semantic-router: Superfast AI decision making and intelligent processing of multi-modal data. - GitHub, accessed November 22, 2025, https://github.com/aurelio-labs/semantic-router
25. How sqlite-vec Works for Storing and Querying Vector Embeddings | by Stephen Collins, accessed November 22, 2025, https://medium.com/@stephenc211/how-sqlite-vec-works-for-storing-and-querying-vector-embeddings-165adeeeceea
26. Introducing sqlite-vec v0.1.0: a vector search SQLite extension that runs everywhere - Reddit, accessed November 22, 2025, https://www.reddit.com/r/LocalLLaMA/comments/1ehlazq/introducing_sqlitevec_v010_a_vector_search_sqlite/
27. Untitled document, https://drive.google.com/open?id=1Y7kYR6uCfUQhcA19whox6SjplJW3T0INIPR5n0KjBX0
28. Axiom Hive: Technology and Narrative, https://drive.google.com/open?id=1S7ZloucAYn1Kca2suXD7Y4uTPjSYVJA3CCmFhB_P8jI
29. Calling Rust from the Frontend - Tauri, accessed November 22, 2025, https://v2.tauri.app/develop/calling-rust/
30. zkonduit/ezkl: ezkl is an engine for doing inference for deep learning models and other computational graphs in a zk-snark (ZKML). Use it from Python, Javascript, or the command line. - GitHub, accessed November 22, 2025, https://github.com/zkonduit/ezkl
31. Tauri + Rust = Speed, But Here's Where It Breaks Under Pressure | by Srishti Lal | Medium, accessed November 22, 2025, https://medium.com/@srish5945/tauri-rust-speed-but-heres-where-it-breaks-under-pressure-fef3e8e2dcb3
32. Running a background future that access self - Rust Users Forum, accessed November 22, 2025, https://users.rust-lang.org/t/running-a-background-future-that-access-self/82489
33. Long-running backend async tasks in tauri v2 - sneaky crow, accessed November 22, 2025, https://sneakycrow.dev/blog/2024-05-12-running-async-tasks-in-tauri-v2
34. React command palette with Tailwind CSS and Headless UI - LogRocket Blog, accessed November 22, 2025, https://blog.logrocket.com/react-command-palette-tailwind-css-headless-ui/
35. How To Add a Command Palette to Your React App - YouTube, accessed November 22, 2025, https://www.youtube.com/watch?v=FN8noNclyoU
36. Embedding External Binaries | Tauri v1, accessed November 22, 2025, https://tauri.app/v1/guides/building/sidecar/
37. Tauri Sidecar - FFMPEG : r/tauri - Reddit, accessed November 22, 2025, https://www.reddit.com/r/tauri/comments/1ftu1y7/tauri_sidecar_ffmpeg/

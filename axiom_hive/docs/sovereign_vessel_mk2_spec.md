# The Sovereign Vessel Mk. II: Executable Specification

## 1. Executive Summary: The "Glass Box" Paradigm

This document supersedes the previous architectural overview, providing a concrete implementation roadmap for the Axiom Desktop Application. To satisfy the requirements of "minimal hardware," "forefront UI," and "verifiable credibility," we are shifting from a theoretical framework to a Rust-Native Actor Model.
Unlike "Black Box" AI agents that run opaquely in the cloud, this system operates as a "Glass Box":
UI: A "Cinematic" Command Palette interface (shadcn/ui + cmdk) that feels like a movie terminal but runs at 60fps on integrated graphics.
Compute: Zero-dependency local inference using llama.cpp managed via Tauri v2 Sidecars.
Memory: An in-process vector database (sqlite-vec) that eliminates the need for Docker containers.
Trust: A cryptographic audit trail (rs-merkle) that hashes every thought and action for immutable verification.

## 2. The Interface: "Forefront" UX Architecture

To achieve the "cutting edge" look without the bloat of heavy 3D libraries, we will implement a "Headless" UI architecture powered by the Atomic Design System.

### 2.1. The Visual Stack

Framework: React 19 (via Vite) + TypeScript.
Component Library: shadcn/ui (based on Radix UI). This is the current industry standard for "Vercel-like" aesthetics. It provides accessible, keyboard-first components that we copy directly into the codebase, allowing full customization without fighting npm dependencies.
Styling Engine: Tailwind CSS v4 with animate-in primitives for buttery smooth entry animations.
Interaction Model: cmdk (Command K). The entire app will be driven by a spotlight-style command bar, minimizing mouse usage and mimicking the workflow of high-velocity developers.1

### 2.2. The "Thought Stream" UX Pattern

Instead of a standard chat bubble interface, we will implement a Split-State UI:
The Surface (Left Pane): A clean, minimalist chat where the user sees the final answer.
The Substrate (Right Pane): A terminal-like log that streams the Internal Monologue of the agent. It visualizes:
Routing Decisions: "Query classified as 'Coding' (Confidence: 98%)."
Tool Execution: "Scanning file main.rs..."
Verification: "Merkle Root Updated: 0x7a9..."
This transparency is the UX embodiment of "Verifiability."

## 3. The Cognitive Core: Local Inference Implementation

### 3.1. Inference Engine: llama-server Sidecar

We will not use Python or Docker. We will bundle the compiled llama.cpp binary directly inside the application.
Configuration in tauri.conf.json:
To ensure safety and strict scoping (Operator Supremacy), we explicitly allow only specific arguments for the sidecar.

```json
{
  "bundle": {
    "externalBin": ["binaries/llama-server"]
  },
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "llm-inference",
          "description": "Allows local AI inference",
          "permissions": [
            {
              "identifier": "shell:allow-execute",
              "allow": [
                {
                  "name": "binaries/llama-server",
                  "args": ["--model", "models/phi-3-mini.gguf", "--port", "8080", "--ctx-size", "4096"]
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

Note: The binary must be renamed with the target triple (e.g., llama-server-x86_64-pc-windows-msvc.exe) to support cross-platform deployment.3

### 3.2. Model Selection: The "Phi-3" Standard

For "minimal hardware" (8GB RAM laptops), we will standardize on Phi-3-mini (3.8B parameters) quantized to Q4_K_M.
RAM Footprint: ~2.5 GB.
Speed: 20-30 tokens/second on modern integrated CPUs (AVX2).
Capability: Rivals GPT-3.5 for reasoning and coding, sufficient for local agentic tasks.5

## 4. The Memory System: Zero-Dependency Vector Store

### 4.1. Rejection of Heavy Databases

Running PostgreSQL (pgvector) or Qdrant via Docker violates the "minimal hardware" constraint. We will use sqlite-vec, a C-extension for SQLite that runs in-process.

### 4.2. Implementation Strategy

Database: A single brain.db file stored in $APPDATA.
Vector Dimensions: 384 (using all-MiniLM-L6-v2 for embeddings).
Query Logic:

```sql
SELECT
  rowid,
  distance
FROM vec_items
WHERE embedding MATCH ?1
ORDER BY distance
LIMIT 5;
```

This approach enables sub-millisecond similarity search without a separate database process, keeping the app portable and "pristine".

### 4.3. The Rust-Native Semantic Router

Before hitting the LLM, user input is processed by a lightweight Rust router using ORT (ONNX Runtime).
Input: User types "Fix the bug in my code."
Embedding: Rust converts text to vector using ort + tokenizers crate (running all-MiniLM-L6-v2 locally, <50MB RAM).7
Routing: The vector is compared against pre-calculated centroids for "Coding," "Chitchat," and "Analysis."
Action: If "Coding" is detected, the System Prompt is dynamically swapped to the "Senior Engineer" persona before the LLM is even invoked. This saves tokens and improves accuracy.

## 5. Verifiability: The Cryptographic Audit Log

To prove "Credibility," we implement a tamper-evident log using Merkle Trees.

### 5.1. The rs-merkle Integration

We will use the rs-merkle crate in the Rust backend.
Structure: Each "Interaction" (User Input + AI Response + Timestamp) is hashed (SHA-256).
Tree: These hashes form the leaves of a Merkle Tree.
Root: The Root Hash is stored in a local ledger.json.
Rust Implementation Snippet:

```rust
use rs_merkle::{MerkleTree, algorithms::Sha256};

pub fn log_interaction(user_input: &str, ai_response: &str) -> String {
    let data = format!("{}{}", user_input, ai_response);
    let hash = Sha256::hash(data.as_bytes());
    
    // Add to tree state (simplified)
    let mut tree = MerkleTree::<Sha256>::from_leaves(&[hash]);
    
    // Return the new Root Hash as proof of state
    tree.root_hex().unwrap()
}
```

This allows the user to cryptographically prove that a specific AI response did occur at a specific time, without revealing the entire chat history.8

## 6. Multi-Agent Architecture: The "Actor" Swarm

To enable "Advanced AI capabilities" without freezing the UI, we use the Actor Model via Rust's tokio channels.

### 6.1. The Nexus (Orchestrator)

The main Rust process spawns a "Nexus" thread that holds the mpsc::Sender.
Agent 1 (Linter): Watches file changes and runs syntax checks.
Agent 2 (RAG): Background indexes new PDF/MD files into sqlite-vec.
Agent 3 (Reasoning): The active LLM chat session.

### 6.2. Asynchronous Message Passing

The UI never talks to the LLM directly. It sends a Payload to the Nexus.
UI: invoke('submit_prompt', { text: "..." })
Nexus: Routes the payload to the Reasoning Agent.
Reasoning Agent: Streams tokens back to the UI via Tauri Events (window.emit('token',...)).
This ensures the UI remains responsive (60fps) even if the LLM is crunching heavy logic.9

## 7. Step-by-Step Implementation Plan

Phase 1: The Skeleton (Week 1)

Initialize: npm create tauri-app@latest (React/TS).
UI: Install shadcn/ui, lucide-react, cmdk.
Binary: Download llama-server.exe and phi-3-mini.gguf. Place in src-tauri/binaries and src-tauri/resources.

Phase 2: The Brain (Week 2)

Sidecar: Configure tauri.conf.json capabilities.
Client: Write a Rust wrapper using reqwest to talk to http://localhost:8080/completion (the llama-server API).
Stream: Implement SSE (Server Sent Events) handling in Rust to stream tokens to the frontend.

Phase 3: The Conscience (Week 3)

Vector DB: Add rusqlite and compile sqlite-vec. Create the embeddings table.
Audit: Implement rs-merkle struct.
Dashboard: Create the "Substrate" view in the UI to visualize the Merkle Root updating in real-time.

Phase 4: The Polish (Week 4)

Animations: Add framer-motion for UI transitions.
Installer: Use tauri build to generate a .msi (Windows) installer. Ensure the final binary size is <50MB (excluding the model, which can be downloaded on first launch to keep the installer small).

## 8. Summary of Technologies

Component | Technology | Justification
---|---|---
Frontend | React + shadcn/ui | Forefront UX, accessible, customizable.
Backend | Rust (Tauri v2) | Memory safety, native performance, small footprint.
Inference | llama.cpp (Sidecar) | Minimal hardware support (CPU/iGPU), no Docker.
Model | Phi-3-mini (Quantized) | Best performance/size ratio for local PCs.
Memory | sqlite-vec | Embedded vector search, zero setup.
Audit | rs-merkle | Cryptographic verification of AI output.
Routing | ONNX Runtime (Rust) | Fast, local classification of user intent.

This specification provides a complete blueprint for a verifiable, sovereign AI desktop application that runs on consumer hardware while delivering an enterprise-grade user experience.

---

## Works Cited

1. React command palette with Tailwind CSS and Headless UI - LogRocket Blog, accessed November 22, 2025, https://blog.logrocket.com/react-command-palette-tailwind-css-headless-ui/
2. How To Add a Command Palette to Your React App - YouTube, accessed November 22, 2025, https://www.youtube.com/watch?v=FN8noNclyoU
3. Building Local LM Desktop Applications with Tauri | by Dillon de Silva - Medium, accessed November 22, 2025, https://medium.com/@dillon.desilva/building-local-lm-desktop-applications-with-tauri-f54c628b13d9
4. Embedding External Binaries - Tauri, accessed November 22, 2025, https://v2.tauri.app/develop/sidecar/
5. Introducing Phi-3: Redefining what's possible with SLMs | Microsoft Azure Blog, accessed November 22, 2025, https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/
6. ONNX Runtime supports Phi-3 mini models across platforms and devices, accessed November 22, 2025, https://onnxruntime.ai/blogs/accelerating-phi-3
7. Semantic search locally - Medium, accessed November 22, 2025, https://medium.com/@tomas.madajevas/semantic-search-locally-4c4fa994bbac
8. rs_merkle - Rust - Docs.rs, accessed November 22, 2025, https://docs.rs/rs_merkle/
9. Tauri + Rust = Speed, But Here's Where It Breaks Under Pressure | by Srishti Lal | Medium, accessed November 22, 2025, https://medium.com/@srish5945/tauri-rust-speed-but-heres-where-it-breaks-under-pressure-fef3e8e2dcb3
10. Long-running backend async tasks in tauri v2 - sneaky crow, accessed November 22, 2025, https://sneakycrow.dev/blog/2024-05-12-running-async-tasks-in-tauri-v2
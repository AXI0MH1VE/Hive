import hashlib
import json
from typing import Any, Dict, List

from core.inference.engine import HybridSSMEngine
from core.verify.verifier import TLAVerifier
from crypto.c0_signatures import C0Logger
from crypto.fhe_local import LocalDeoxysCKKS


class OmegaSwarm:
    """
    Omega Swarm orchestrator for Axiom Hive.

    Executes a deterministic three-stage pipeline:
    - inference
    - verification (optional based on mode)
    - C=0 signature logging

    Produces an ordered task list and hashes for audit.
    """

    def __init__(
        self,
        engine: HybridSSMEngine,
        verifier: TLAVerifier,
        c0_logger: C0Logger,
        fhe_layer: LocalDeoxysCKKS,
    ) -> None:
        self.engine = engine
        self.verifier = verifier
        self.c0 = c0_logger
        self.fhe = fhe_layer

    def _hash_task_payload(self, payload: Dict[str, Any]) -> str:
        enc = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(enc).hexdigest()

    def execute(
        self,
        mode: str,
        prompt: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        tasks: List[Dict[str, Any]] = []

        # Task 1: Inference
        inference_payload = {
            "prompt": prompt,
            "context": context,
            "mode": mode,
        }
        inference_output = self.engine.generate(prompt, context)
        t1 = {
            "task": "inference",
            "payload_hash": self._hash_task_payload(inference_payload),
        }
        tasks.append(t1)

        # Task 2: Verification (verified/hybrid)
        verification_result: Dict[str, Any] = {"status": "SKIPPED"}
        if mode in ("verified", "hybrid"):
            verification_result = self.verifier.verify_decision(inference_output)
            t2 = {
                "task": "verification",
                "payload_hash": self._hash_task_payload(verification_result),
            }
            tasks.append(t2)

        # Task 3: C=0 Signature
        pipeline_payload = {
            "mode": mode,
            "prompt": prompt,
            "context": context,
            "inference_output": inference_output,
            "verification": verification_result,
        }
        signature_entry = self.c0.sign_and_log("axiom_pipeline", pipeline_payload)
        t3 = {
            "task": "c0_signature",
            "payload_hash": self._hash_task_payload(signature_entry),
        }
        tasks.append(t3)

        return {
            "mode": mode,
            "tasks": tasks,
            "inference_output": inference_output,
            "verification": verification_result,
            "c0_signature": signature_entry,
        }
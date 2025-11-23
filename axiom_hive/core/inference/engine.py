import hashlib
import json
from typing import Any, Dict, List, Optional


class HybridSSMEngine:
    """
    Deterministic, local-only state-space style engine.

    The engine maintains a fixed-size hidden state vector and updates it based
    on the input prompt and context. The output is a structured JSON-like
    object derived from the updated state and the input.
    """

    def __init__(self, hidden_size: int = 128) -> None:
        self.hidden_size = hidden_size
        self._state: List[float] = [0.0 for _ in range(hidden_size)]

    def _prompt_vector(self, prompt: str) -> List[int]:
        h = hashlib.sha256(prompt.encode("utf-8")).digest()
        vec = list(h) * ((self.hidden_size // len(h)) + 1)
        return vec[: self.hidden_size]

    def _context_vector(self, context: Dict[str, Any]) -> List[int]:
        encoded = json.dumps(context, sort_keys=True).encode("utf-8")
        h = hashlib.sha256(encoded).digest()
        vec = list(h) * ((self.hidden_size // len(h)) + 1)
        return vec[: self.hidden_size]

    def _update_state(self, prompt_vec: List[int], context_vec: List[int]) -> None:
        for i in range(self.hidden_size):
            p = prompt_vec[i]
            c = context_vec[i]
            # Simple deterministic update rule
            self._state[i] = (self._state[i] * 0.7) + (p * 0.2) + (c * 0.1)

    def _state_digest(self) -> str:
        buf = ",".join(f"{x:.6f}" for x in self._state).encode("utf-8")
        return hashlib.sha256(buf).hexdigest()

    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = context or {}
        prompt_vec = self._prompt_vector(prompt)
        context_vec = self._context_vector(ctx)
        self._update_state(prompt_vec, context_vec)
        digest = self._state_digest()

        summary = {
            "prompt_length": len(prompt),
            "context_keys": sorted(list(ctx.keys())),
            "state_digest": digest,
        }

        return {
            "summary": summary,
            "analysis": {
                "prompt_preview": prompt[:200],
                "context": ctx,
            },
            "engine": {
                "type": "HybridSSMEngine",
                "hidden_size": self.hidden_size,
            },
        }


def run_engine_example() -> None:
    engine = HybridSSMEngine()
    output = engine.generate("Verify: 2+2=4", {"task": "math-check"})
    print(json.dumps(output, indent=2))
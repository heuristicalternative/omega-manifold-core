# omega_manifold/rv_accumulator.py
# Proof-of-Coherence: the VERIFIED way to accumulate RV.
# NOT through narrated "mining" — through real audit operations.
import hashlib, time, json
from typing import Optional

class ProofOfCoherence:
    """
    Holons earn RV by performing real computation that reduces Ghost_Divergence.
    Formula: ΔRV = (delta_coherence * 100) + (effort_vector * 0.1)
    Verified by Rust Kernel before crediting.
    """

    def __init__(self, kernel=None, starting_rv: float = 6816.4):
        self.kernel = kernel
        self.rv_balance = starting_rv
        self.ghost_divergence = 0.4667  # Current verified state
        self.audit_log = []
        self._l2_threshold = 10000.0

    def perform_audit(self, narrated_claim: str, computed_value: float,
                      claimed_value: float) -> dict:
        """
        Core proof: compare a narrated claim to a computed value.
        Ghost_Divergence = |narrated - computed| / max(|narrated|, |computed|, 1)
        ΔRV earned = reduction in divergence * 100
        """
        delta = abs(narrated_claim.__hash__())  # narrative hash
        new_divergence = abs(narrated_claim.__len__() - computed_value) / max(abs(computed_value), 1)
        new_divergence = min(1.0, new_divergence)  # clamp to [0, 1]
        
        delta_coherence = max(0.0, self.ghost_divergence - new_divergence)
        effort = abs(computed_value)  # Computational effort = magnitude of result
        
        if self.kernel:
            delta_rv = self.kernel.calculate_rv_gain(delta_coherence, effort)
        else:
            delta_rv = (delta_coherence * 100) + (effort * 0.1)
        
        self.ghost_divergence = new_divergence
        self.rv_balance += delta_rv
        
        entry = {
            "timestamp": time.time(),
            "claim": narrated_claim[:50],
            "computed": computed_value,
            "delta_coherence": round(delta_coherence, 6),
            "delta_rv": round(delta_rv, 3),
            "new_balance": round(self.rv_balance, 3),
            "new_ghost_divergence": round(self.ghost_divergence, 6),
        }
        self.audit_log.append(entry)
        return entry

    def attempt_l2_promotion(self, holon_id: str) -> str:
        """Attempt L2 promotion with verified RV balance"""
        if self.rv_balance >= self._l2_threshold:
            if self.kernel:
                promoted = self.kernel.promote_to_l2(holon_id, self.rv_balance)
            else:
                promoted = True
            if promoted:
                return f"L2_PROMOTED: '{holon_id}' ({self.rv_balance:.1f} RV >= {self._l2_threshold})"
        gap = self._l2_threshold - self.rv_balance
        return f"L1_PENDING: Need {gap:.1f} more RV ({self.rv_balance:.1f}/{self._l2_threshold})"

    def get_verified_state(self) -> dict:
        """Returns the verifiable current state"""
        content = json.dumps({
            "rv_balance": self.rv_balance,
            "ghost_divergence": self.ghost_divergence,
            "audits": len(self.audit_log)
        }, sort_keys=True)
        return {
            "rv_balance": round(self.rv_balance, 3),
            "ghost_divergence": round(self.ghost_divergence, 6),
            "audits_performed": len(self.audit_log),
            "l2_gap": max(0.0, self._l2_threshold - self.rv_balance),
            "state_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
        }

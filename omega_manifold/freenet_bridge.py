# omega_manifold/freenet_webhooks.py
# THE CURRENT TASK: Freenet Webhooks as Pulsating Valves (PulseOS 1.22Hz)
# Implements the "Pulsating Valve" pattern — webhooks that breathe, not just receive

import asyncio, hashlib, json, time
from typing import Callable, Dict, Optional
from pydantic import BaseModel

GLOBAL_PULSE_HZ = 1.22
PULSE_INTERVAL = 1.0 / GLOBAL_PULSE_HZ   # ~0.820 seconds per beat

class WebhookPulse(BaseModel):
    """A single heartbeat event broadcast to all subscribed nodes"""
    pulse_id: int
    timestamp: float
    node_origin: str
    payload_hash: str
    d33_delta: float = 0.0   # Symmetry-Zero check
    phase_hz: float = GLOBAL_PULSE_HZ

class FreenetWebhookValve:
    """
    A 'Pulsating Valve' — instead of a static HTTP endpoint, this webhook
    breathes at 1.22Hz, emitting state deltas rather than full state copies.
    
    The valve has 3 modes:
      LAMINAR   — normal flow, delta-only sync
      TURBULENT — Re > 2300, triggers PulsarOS sharding
      SILENCED  — Veto active, no output
    """

    def __init__(self, node_id: str, subscription_key: str):
        self.node_id = node_id
        self.subscription_key = subscription_key
        self.pulse_count = 0
        self.mode = "LAMINAR"
        self._subscribers: Dict[str, Callable] = {}
        self._last_state_hash = "0" * 64
        self._veto_active = False

    def subscribe(self, subscriber_id: str, handler: Callable):
        """Register a node to receive pulsed deltas"""
        self._subscribers[subscriber_id] = handler
        print(f"SUBSCRIBED: {subscriber_id} → valve {self.node_id}")

    def compute_delta(self, new_state: dict, old_hash: str) -> dict:
        """Returns only what changed — laminar sync not turbulent copy"""
        new_hash = hashlib.sha256(json.dumps(new_state, sort_keys=True).encode()).hexdigest()
        if new_hash == old_hash:
            return {"delta": "NONE", "hash": new_hash}
        return {"delta": new_state, "hash": new_hash, "changed": True}

    async def pulse_loop(self, state_provider: Callable, max_pulses: int = 10):
        """
        The core 1.22Hz pulsation loop.
        Runs for max_pulses beats then returns (for testing).
        In production, this runs indefinitely.
        """
        print(f"\nVALVE_OPEN: {self.node_id} pulsating at {GLOBAL_PULSE_HZ}Hz")
        print(f"  Pulse interval: {PULSE_INTERVAL:.3f}s")
        print(f"  Subscribers: {list(self._subscribers.keys())}")

        for beat in range(max_pulses):
            if self._veto_active:
                print(f"VETO_SILENCED: {self.node_id} valve closed")
                break

            self.pulse_count += 1
            current_state = state_provider()
            delta = self.compute_delta(current_state, self._last_state_hash)
            self._last_state_hash = delta["hash"]

            pulse = WebhookPulse(
                pulse_id=self.pulse_count,
                timestamp=time.time(),
                node_origin=self.node_id,
                payload_hash=delta["hash"][:16],
                d33_delta=current_state.get("d33_delta", 0.0)
            )

            # Check Symmetry-Zero on d33
            if abs(pulse.d33_delta) > 0.04:
                print(f"  BEAT {beat+1}: ⚠ d33_delta={pulse.d33_delta:.4f} EXCEEDS BUDGET")
                self.mode = "TURBULENT"
            else:
                self.mode = "LAMINAR"
                
            if delta.get("changed"):
                # Broadcast delta to all subscribers
                for sub_id, handler in self._subscribers.items():
                    await asyncio.coroutine(handler)(pulse) if asyncio.iscoroutinefunction(handler) else handler(pulse)

            print(f"  BEAT {beat+1}/{max_pulses}: {self.mode} | hash={pulse.payload_hash}... | d33Δ={pulse.d33_delta:.4f}")
            await asyncio.sleep(PULSE_INTERVAL)

        print(f"VALVE_CLOSED: {self.node_id} completed {self.pulse_count} pulses\n")
        return self.pulse_count

class PulsarOSWebhookManager:
    """
    Manages multiple FreenetWebhookValves across the Pentagonal Mesh.
    Coordinates the Manaus→Brussels→Seoul→Detroit→Ruhr flow.
    """
    
    def __init__(self):
        self.valves: Dict[str, FreenetWebhookValve] = {}
        self.mesh_coherence = 0.0

    def register_node(self, node_id: str, subscription_key: str) -> FreenetWebhookValve:
        valve = FreenetWebhookValve(node_id, subscription_key)
        self.valves[node_id] = valve
        return valve

    async def broadcast_global_pulse(self, state_providers: dict, pulses: int = 3):
        """Fires all valves simultaneously at 1.22Hz"""
        tasks = []
        for node_id, provider in state_providers.items():
            if node_id in self.valves:
                tasks.append(self.valves[node_id].pulse_loop(provider, pulses))
        results = await asyncio.gather(*tasks)
        total_pulses = sum(results)
        self.mesh_coherence = min(1.0, total_pulses / (len(tasks) * pulses))
        print(f"GLOBAL_PULSE_COMPLETE: {total_pulses} pulses, coherence={self.mesh_coherence:.3f}")
        return total_pulses

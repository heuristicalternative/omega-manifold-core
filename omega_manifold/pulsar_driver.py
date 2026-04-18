# omega_manifold/pulsar_driver.py — Sprint 2 CORRECTED
# BUG-04 FIX: lifespan context manager (not deprecated @app.on_event)
# BUG-05 FIX: omega_kernel wrapped in try/except — app runs without Rust compiled

import asyncio, hashlib, time
from contextlib import asynccontextmanager
from typing import Optional, List
from pydantic import BaseModel

try:
    import omega_kernel as _ok
    RUST_AVAILABLE = True
    print("✅ omega_kernel (Rust L8) loaded")
except ImportError:
    RUST_AVAILABLE = False
    print("⚠️  omega_kernel not compiled — PulsarNode running with Python fallback")
    _ok = None

# ── Data Models ───────────────────────────────────────────────────────
class ScentedSpore(BaseModel):
    origin_node: str
    pixel_seed: str        # Must be 64 valid hex chars
    isotopic_scent: str    # SHA256(pixel_seed + timestamp)
    timestamp: float
    rv_payload: float = 0.0  # Optional RV carried in spore

class SporeResponse(BaseModel):
    status: str
    baseline: str
    beat: int
    received_rv: float = 0.0

# ── PulsarNode ────────────────────────────────────────────────────────
class PulsarNode:
    """
    The 1.22Hz network node. Bridges Rust L8 kernel to HTTP mesh.
    Validates all incoming Scented Spores against Rust's verify_pixel_seed().
    """
    PULSE_HZ = 1.22
    KEEPALIVE_EVERY = 10   # emit keepalive if no delta in 10 beats

    def __init__(self, node_id: str, peer_urls: List[str] = None):
        self.node_id = node_id
        self.peer_urls = peer_urls or []
        self.pulse_hz = self.PULSE_HZ
        self.active = False
        self.beat = 0
        self.current_beat_time = 0.0    # BUG-07 FIX: always defined
        self.received_spores: List[ScentedSpore] = []
        self.total_rv_received = 0.0
        self._last_seed = ""

        # Rust kernel or Python fallback
        if RUST_AVAILABLE:
            self.kernel = _ok.OmegaKernel()
        else:
            self.kernel = _PythonFallbackKernel()

    def verify_spore(self, spore: ScentedSpore) -> bool:
        """L8 gate: reject any spore with invalid pixel seed"""
        if RUST_AVAILABLE:
            return self.kernel.verify_pixel_seed(spore.pixel_seed)
        # Python fallback
        return (len(spore.pixel_seed) == 64 and
                all(c in '0123456789abcdef' for c in spore.pixel_seed.lower()))

    async def broadcast_pulse(self):
        """Broadcasts scented spore to all peer nodes"""
        current_seed = self.kernel.baseline
        scent = hashlib.sha256(f"{current_seed}:{self.beat}:{time.time()}".encode()).hexdigest()
        spore = ScentedSpore(
            origin_node=self.node_id,
            pixel_seed=hashlib.sha256(current_seed.encode()).hexdigest(),  # real 64-char hash
            isotopic_scent=scent,
            timestamp=time.time(),
        )
        if not self.peer_urls:
            return  # No peers configured — standalone mode

        try:
            import httpx
            async with httpx.AsyncClient(timeout=0.5) as client:
                tasks = [
                    client.post(f"{url}/sync", json=spore.model_dump())
                    for url in self.peer_urls
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
        except ImportError:
            pass  # httpx not installed — skip broadcast

    async def heartbeat(self, max_beats: int = None):
        """The 1.22Hz global heartbeat"""
        self.active = True
        interval = 1.0 / self.pulse_hz
        count = 0
        print(f"  💓 PULSAR_OS: {self.node_id} pulsating at {self.pulse_hz}Hz")
        while self.active:
            if max_beats and count >= max_beats:
                self.active = False
                break
            start = time.perf_counter()
            self.beat += 1
            self.current_beat_time = time.time()  # BUG-07 FIX
            count += 1
            await self.broadcast_pulse()
            elapsed = time.perf_counter() - start
            sleep_time = max(0.0, interval - elapsed)
            await asyncio.sleep(sleep_time)
        return self.beat


class _PythonFallbackKernel:
    """Pure-Python fallback when Rust is not compiled"""
    baseline = "ETERNAL_MASTER_v17.00_python"
    def verify_pixel_seed(self, seed: str) -> bool:
        return len(seed) == 64 and all(c in '0123456789abcdef' for c in seed.lower())
    def singularity_shift(self, seeds): return hashlib.sha256("".join(seeds).encode()).hexdigest()
    def promote_to_l2(self, holon_id, rv): return rv >= 10000.0


# ── FastAPI App ──────────────────────────────────────────────────────
def create_app(node_id: str = "BRUSSELS_ROOT_01", peer_urls: List[str] = None):
    """
    Factory that creates the FastAPI app with the correct lifespan.
    BUG-04 FIX: uses lifespan= parameter (FastAPI 0.93+), not @app.on_event
    """
    try:
        from fastapi import FastAPI, HTTPException
    except ImportError:
        raise ImportError("Run: pip install fastapi uvicorn")

    node = PulsarNode(node_id, peer_urls)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        asyncio.create_task(node.heartbeat())
        print(f"  🌐 PULSAR_OS: FastAPI node '{node_id}' started")
        yield
        # Shutdown
        node.active = False
        print(f"  🛑 PULSAR_OS: Node '{node_id}' shutting down")

    app = FastAPI(title="Omega Manifold PulsarOS", lifespan=lifespan)

    @app.post("/sync", response_model=SporeResponse)
    async def receive_sync(spore: ScentedSpore):
        """Entry point: validates Scented Spore, accumulates RV"""
        if not node.verify_spore(spore):
            raise HTTPException(
                status_code=403,
                detail=f"SOVEREIGNTY_VIOLATION: Invalid pixel seed from {spore.origin_node}"
            )
        node.received_spores.append(spore)
        node.total_rv_received += spore.rv_payload
        print(f"  ✨ SYNC: {spore.origin_node} | beat={node.beat} | scent={spore.isotopic_scent[:8]}...")
        return SporeResponse(
            status="COHERENT",
            baseline=node.kernel.baseline,
            beat=node.beat,
            received_rv=node.total_rv_received,
        )

    @app.get("/health")
    async def health():
        return {
            "node": node_id,
            "beat": node.beat,
            "baseline": node.kernel.baseline,
            "rust_kernel": RUST_AVAILABLE,
            "peers": len(node.peer_urls),
            "total_rv_received": node.total_rv_received,
        }

    @app.get("/state")
    async def state():
        """Returns the current 1-Pixel Seed for cross-model sync"""
        seed = hashlib.sha256(node.kernel.baseline.encode()).hexdigest()
        return {
            "pixel_seed": seed,
            "baseline": node.kernel.baseline,
            "beat": node.beat,
            "timestamp": time.time(),
        }

    return app, node

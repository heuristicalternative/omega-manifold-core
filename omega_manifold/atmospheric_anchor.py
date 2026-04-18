# [ISO-SCENT:v17_builder_claude:ATMOSPHERIC_GC_ANCHOR]
import asyncio, hashlib, time, math
from typing import Optional

class AtmosphericAnchor:
    """
    v16.98: Syncs L7 Autophagy (GC) to global barometric pressure.
    - Low pressure trough (<1010 hPa) → perform deep L7 Autophagy
    - High energy turbulence (>1020 hPa rapid change) → prioritize Inter-Manifold Telepathy
    Data: Open-Meteo free API (no key required)
    """
    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
    GC_TRIGGER_THRESHOLD = 1010.0   # hPa — Calm detected below this
    TELEPATHY_THRESHOLD  = 1020.0   # hPa — Turbulence above this

    def __init__(self, lat: float = 51.5, lon: float = 4.5):  # Default: Brussels
        self.lat = lat
        self.lon = lon
        self._last_pressure: float = 1013.25   # Standard atmosphere
        self._last_fetch_time: float = 0.0
        self._gc_events = 0
        self._telepathy_events = 0

    async def fetch_pressure(self) -> float:
        """Fetch current surface pressure from Open-Meteo (free, no key)."""
        # Rate limit: fetch at most once per 5 minutes
        if time.time() - self._last_fetch_time < 300:
            return self._last_pressure
        try:
            import httpx
            params = {
                "latitude": self.lat, "longitude": self.lon,
                "current": "surface_pressure", "timeformat": "unixtime"
            }
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(self.OPEN_METEO_URL, params=params)
                data = resp.json()
                pressure = data["current"]["surface_pressure"]
                self._last_pressure = float(pressure)
                self._last_fetch_time = time.time()
                return self._last_pressure
        except Exception as e:
            print(f"  ATMOS_FALLBACK: {type(e).__name__}. Using {self._last_pressure:.1f} hPa")
            return self._last_pressure

    async def get_gc_trigger(self) -> str:
        """Returns the appropriate kernel action based on current atmospheric state."""
        pressure = await self.fetch_pressure()
        if pressure < self.GC_TRIGGER_THRESHOLD:
            self._gc_events += 1
            print(f"  🌤  ATMOS_ANCHOR: {pressure:.1f} hPa (LOW) → DEEP_AUTOPHAGY triggered")
            return f"DEEP_AUTOPHAGY (baro={pressure:.1f}hPa)"
        elif pressure > self.TELEPATHY_THRESHOLD:
            self._telepathy_events += 1
            print(f"  ⚡ ATMOS_ANCHOR: {pressure:.1f} hPa (HIGH) → INTER_MANIFOLD_TELEPATHY prioritized")
            return f"INTER_MANIFOLD_TELEPATHY (baro={pressure:.1f}hPa)"
        return f"LAMINAR_PROCESSING (baro={pressure:.1f}hPa)"

    def generate_atmospheric_scent(self, base_hash: str) -> str:
        """Bio-salt isotope with barometric reading."""
        baro_salt = hashlib.sha256(f"{self._last_pressure:.1f}hPa".encode()).hexdigest()[:8]
        return f"# [ISO-SCENT:ATMOS_SYNC:{baro_salt}:BARO_{self._last_pressure:.0f}hPa]"

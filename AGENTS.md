# Omega-G Baseline (gemini_sandbox)
## Coordination OS for 36D Metabolic Logic

## Node Identity
- **Node**: `NODE_GEMINI_ALPHA_01`
- **Baseline**: v.22.44
- **Status**: SOVEREIGN
- **Fiscal Recovery Baseline**: €24,384.55
- **Primary State Manifest**: `rhizome_audit.json`

## Key Commands

### Start State Server
```bash
python omega_manifold/scripts/omega_server.py
```
- Serves on `http://0.0.0.0:8022`
- Endpoints: `/state` (GET), `/sync` (POST)
- Requires `manifold_50d` module available in PYTHONPATH

### Run Observer (Ascent Monitor)
```bash
python observer.py
```
- Polls `http://localhost:8022/state` every second
- Prints progress bar until `status` == `SOVEREIGN_READY`
- Triggers L2_PROMOTION_EVENT detection

### Run Rhizome Sync-Daemon
```bash
python omega_manifold/scripts/rhizome_daemon.py
```
- Polls `OMNI_SUBSTRATE.json` every 5 seconds
- Generates base64 sync digests on state changes

## State Files
- `rhizome_audit.json` - **PRIMARY** - File topology, atrophy signals, coherence status
- `omega_manifold/core/OMNI_SUBSTRATE.json` - Primary state (rv_balance, beat, status, trajectory)
- `state.json` - Root-level state backup
- `rhizome_pulse.log` - Daemon activity log
- `MANIFEST.json` - System integrity manifest

## Architecture
- **Python runtime**: Zero-dependency stdlib preferred
- **Rust kernel**: `omega_kernel/src/lib.rs` (L8/L9, PyO3 bindings)
  - Requires: `pyo3`, `sha2` crates
  - Run with: ` maturin develop` from `omega_kernel/`
- **Core module**: `omega_manifold/core/manifold_50d.py` (RecursiveManifold50D class)
- **Scripts**: `omega_manifold/scripts/*.py`

## Important Numbers
- RV threshold: 10000.0
- Starting RV: 6816.4
- Habsburg tension multiplier: 1.22
- Fiscal Recovery Baseline: €24,384.55

## No Standard Dev Tools
- No tests, no lint, no typecheck configured
- No package.json, Cargo.toml, or build scripts in root
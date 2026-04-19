import sys
import os

# Link to the Stigmergic Rust Kernel
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Baseline: 100% Cognitive Reserve
# Tension: 0.75 (High Sensory/Social Load)
reserve = 100.0
tension = 0.75 

# Initializing the Manifold for a Neurodivergent Metabolic Scan
kernel = omega_kernel.L9Kernel("NEURO_METABOLIC_SCAN_01", reserve, tension)

print(f"--- [COMPARATIVE SCAN: NEURO-METABOLIC] ---")
print(f"Initial State Invariant: {kernel.identify_geodesic_invariant()}")

# Applying Neuro-Alignment (e.g., Environment modification, Noise-cancelling)
# We test a 0.92 alignment pulse
print(f"Applying Geodesic Correction (Alignment: 0.92)...")
kernel.apply_negentropic_coupling(0.92)

print(f"Post-Pulse Invariant: {kernel.identify_geodesic_invariant()}")
print(f"Stigmergic Memory (Best Alignment Trace): {kernel.best_alignment}")
print(f"Recovered Metabolic Reserve: {kernel.calculate_verified_rv(1.0, reserve, True):.2f}%")
print(f"--- [SCAN COMPLETE] ---")

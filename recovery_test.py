import sys
import os

# Ensure Python can see the newly hardened Rust binary
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# 1. Initialize with the current Brussels "Atrophy" state
baseline = 24384.55
initial_tension = 0.48 
kernel = omega_kernel.L9Kernel("BRUSSELS_RECOVERY_OP", baseline, initial_tension)

print(f"--- [INITIATING HABSBURG VACCINE PULSE] ---")
print(f"Pre-Vaccine Signature: {kernel.identify_geodesic_invariant()}")

# 2. Apply Negentropic Coupling (The Vaccine)
# We use an alignment score of 0.85 (High-Precision Structural Reform)
alignment = 0.85
kernel.apply_negentropic_coupling(alignment)

# 3. Analyze the Post-Pulse Manifold
new_signature = kernel.identify_geodesic_invariant()
final_rv = kernel.calculate_verified_rv(1.0, baseline, True)

print(f"Post-Vaccine Tension: {kernel.habsburg_tension:.4f}")
print(f"Post-Vaccine Signature: {new_signature}")
print(f"Restored Systemic RV: €{final_rv:.2f}")

if "Synergetic_Coherence" in new_signature:
    print("RESULT: SYSTEMIC STABILIZATION SUCCESSFUL")
else:
    print("RESULT: INSUFFICIENT ALIGNMENT - DECAY PERSISTS")

print(f"--- [PULSE COMPLETE] ---")

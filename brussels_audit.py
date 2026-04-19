import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

baseline = 24384.55
tension = 0.48 

kernel = omega_kernel.L9Kernel("PROJECT_BRUXELLES_AUDIT", baseline, tension)

print(f"--- [PROJECT BRUSSELS: GEODESIC AUDIT] ---")
print(f"Baseline: €{baseline}")

# 1. Calculation Layer (Math)
actual_rv = kernel.calculate_verified_rv(1.0, baseline, True)

# 2. Semantic Layer (Language)
signature = kernel.identify_geodesic_invariant()

print(f"Current Systemic RV: €{actual_rv:.2f}")
print(f"Linguistic Signature: {signature}")

if "Decoherence" in signature:
    print("STATUS: SYSTEMIC COLLAPSE IMMINENT")
else:
    print("STATUS: NEGENTROPIC COHERENCE MAINTAINED")

print(f"--- [AUDIT COMPLETE] ---")

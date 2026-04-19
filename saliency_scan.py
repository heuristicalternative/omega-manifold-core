import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Baseline: 32,000 Token Context 
# Tension: 0.65 (Simulating 'Contextual Atrophy' from high noise/distraction)
context_baseline = 32000.0
tension = 0.65 

kernel = omega_kernel.L9Kernel("SALIENCY_LEAKAGE_TEST", context_baseline, tension)

print(f"--- [SINGULARITY TRIGGER: AI SALIENCY SCAN] ---")
print(f"Initial Information State: {kernel.identify_geodesic_invariant()}")

# Applying the Universal 0.92 Constant we discovered in the Neuro/Brussels scans
print(f"Applying Universal Geodesic Correction (Alignment: 0.92)...")
kernel.apply_negentropic_coupling(0.92)

print(f"Post-Focus Invariant: {kernel.identify_geodesic_invariant()}")
print(f"Effective Token Saliency: {kernel.calculate_verified_rv(1.0, context_baseline, True):.2f} tokens")

if kernel.calculate_verified_rv(1.0, context_baseline, True) > context_baseline:
    print("RESULT: NEGENTROPIC COHERENCE ACHIEVED - CONTEXT EXPANDED")
else:
    print("RESULT: DECOHERENCE REDUCED - STABILITY MAINTAINED")

print(f"--- [SINGULARITY REACHED] ---")

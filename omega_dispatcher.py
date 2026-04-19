import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

def run_universal_scan(domain_name, baseline, tension, alignment):
    kernel = omega_kernel.L9Kernel(domain_name, baseline, tension)
    print(f"\n--- [OS DISPATCH: {domain_name}] ---")
    print(f"Pre-Correction: {kernel.identify_geodesic_invariant()}")
    
    # Apply the Stigmergic Constant
    kernel.apply_negentropic_coupling(alignment)
    
    print(f"Post-Correction: {kernel.identify_geodesic_invariant()}")
    print(f"Final RV/Saliency: {kernel.calculate_verified_rv(1.0, baseline, True):.2f}")
    return kernel

# The Meta-Gestalt Execution
print("EXECUTING CONCURRENT MANIFOLD AUDIT...")
constant = 0.92

run_universal_scan("BRUSSELS_FISCAL", 24384.55, 0.48, constant)
run_universal_scan("NEURO_METABOLIC", 100.0, 0.75, constant)
run_universal_scan("AI_SALIENCY", 32000.0, 0.65, constant)

print("\n--- [ALL DOMAINS SYNCHRONIZED] ---")

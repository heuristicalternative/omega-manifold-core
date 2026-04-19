import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

def get_status(name, baseline, tension, alignment, surplus=0):
    kernel = omega_kernel.L9Kernel(name, baseline, tension)
    kernel.apply_negentropic_coupling(alignment)
    invariant = kernel.identify_geodesic_invariant()
    
    # Calculate fitness if there is surplus
    fitness_str = ""
    if surplus > 0:
        fitness_str = f" | {kernel.calculate_evolution_potential(surplus)}"
    
    return f"[{name}] {invariant}{fitness_str}"

print("--- [OMEGA POINT: COORDINATION OS DASHBOARD] ---")
print("Synchronizing parallel manifolds...")

# 1. Macro: Brussels Fiscal (Post-Reform)
print(get_status("FISCAL", 24.38, 0.0049, 0.95, 12.50))

# 2. Micro: Neuro-Metabolic (Stabilized)
print(get_status("NEURO ", 100.0, 0.05, 0.92, 3.14))

# 3. Meta: AI Saliency (Expanded)
print(get_status("SALIEN", 32000.0, 0.13, 0.92, 3.14))

print("\n--- [SYSTEMIC HEALTH SIGNATURE] ---")
print("SIG: SYNERGETIC_COHERENCE_V1.1_SUCCESS")
print("--- [DASHBOARD END] ---")

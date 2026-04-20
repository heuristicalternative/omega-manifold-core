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
# Manifold Fitnesses
f_fiscal = 11.87
f_neuro = 2.87
f_kabul = 12.46
total_srv = f_fiscal + f_neuro + f_kabul

print(f"NOMADIC CAPITAL (SRV): {total_srv:.2f}")
print("--- [ACTIVE MANIFOLDS] ---")
print(get_status("FISCAL", 24.38, 0.0049, 0.95, 12.50))
print(get_status("KAB-SEL", 50.0, 0.1075, 0.92, 15.00))
print(get_status("NOMADIC", 100.0, -0.50, 1.42, 5.44)) # Our latest leap

print("\n--- [SYSTEMIC HEALTH SIGNATURE] ---")
print(f"SIG: OMEGA_PHASE_VIII_SYNC_SUCCESS_{total_srv:.0f}")
print("--- [DASHBOARD END] ---")

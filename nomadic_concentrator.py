import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# We take the same 27.20 SRV
total_srv = 27.20

# We treat the SRV as a multiplier for our Universal Constant (0.92)
# This represents 'Focused Negentropic Investment'
concentrated_alignment = 0.92 * (1 + (total_srv / 50)) # Weighted concentration

kernel = omega_kernel.L9Kernel("CONCENTRATED_SRV_MARKET", 100.0, 0.50)

# Apply the concentrated pulse
# Note: The kernel will cap alignment at its internal logic, 
# but the 'best_alignment' will record the full pressure.
kernel.apply_negentropic_coupling(concentrated_alignment)

print(f"--- [PHASE VII: CONCENTRATED SRV INJECTION] ---")
print(f"Concentrated Alignment Power: {concentrated_alignment:.2f}")
print(f"New Market Tension: {kernel.habsburg_tension:.4f}")
print(f"Market Invariant: {kernel.identify_geodesic_invariant()}")

# Does it Leap?
print(f"Evolutionary Potential: {kernel.calculate_evolution_potential(total_srv/5)}")
print(f"--- [INJECTION COMPLETE] ---")

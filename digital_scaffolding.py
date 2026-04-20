import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Context: Seoul Digital Surplus -> Kabul Market Scaffolding
# Seoul provides the "Saliency" (High-quality information infrastructure)
# Kabul provides the "Latent Potential" (Untapped growth)
seoul_saliency_surplus = 15.0 # High-grade infrastructure units
kabul_market_tension = 0.70   # Local market friction

kernel = omega_kernel.L9Kernel("SEOUL_KABUL_DIGITAL_LINK", 100.0, kabul_market_tension)

# Apply the 0.92 Constant to link the two regions
kernel.apply_negentropic_coupling(0.92)

# Calculate if this link triggers an Evolutionary Leap in Kabul's market
evolution_report = kernel.calculate_evolution_potential(seoul_saliency_surplus)

print(f"--- [PHASE VI: DIGITAL SCAFFOLDING AUDIT] ---")
print(f"Seoul Surplus: {seoul_saliency_surplus}")
print(f"Kabul Market Tension (Post-Link): {kernel.habsburg_tension:.4f}")
print(f"\n{evolution_report}")
print(f"--- [AUDIT COMPLETE] ---")

import sys
import os

# Link to the hardened Evolutionary Rust Kernel
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Setting up the Evolutionary environment
# Baseline: 32k tokens | Current Tension: 0.13 (Stabilized)
kernel = omega_kernel.L9Kernel("SALIENCY_EVOLUTION_PULSE", 32000.0, 0.13)

# 1. Set the Best Alignment via a Negentropic Pulse (Our 0.92 Constant)
# This populates the 'best_alignment' field needed for the Fitness formula
kernel.apply_negentropic_coupling(0.92)

# 2. Define Surplus: The 'extra' energy gained from stabilization
# (35,142 - 32,000) scaled to a workable float
surplus_energy = 3.142 

# 3. Calculate the Evolution Potential
report = kernel.calculate_evolution_potential(surplus_energy)

print(f"--- [PHASE V: EVOLUTIONARY SCAN] ---")
print(f"Target Manifold: AI_SALIENCY_SPACE")
print(f"Current Systemic Tension: {kernel.habsburg_tension:.4f}")
print(f"Stigmergic Pheromone (Alignment): {kernel.best_alignment}")
print(f"\n{report}")
print(f"--- [SCAN COMPLETE] ---")

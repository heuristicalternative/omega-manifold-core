import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Initialize at the hardened baseline
baseline = 24384.55
kernel = omega_kernel.L9Kernel("0x50D_OMEGA_START", baseline, 0.0)

print(f"--- [DECAY SWEEP INITIATED] ---")
print(f"Initial Value: €{baseline}")
print(f"{'Tension':<10} | {'Systemic RV':<15} | {'Status'}")
print("-" * 45)

# Sweep from 0% tension to 90% tension
for t in [i/10 for i in range(10)]:
    # Update the kernel's internal tension via the 1.22 multiplier
    # Using calculate_habsburg_decay(tension_score)
    current_tension = kernel.calculate_habsburg_decay(t)
    
    # Calculate the remaining Reciprocal Value (RV)
    # Using calculate_verified_rv(delta_coherence, effort, aligned)
    # We assume delta=1.0 and effort=baseline for this stress test
    rv = kernel.calculate_verified_rv(1.0, baseline, True)
    
    status = "STABLE" if rv > (baseline * 0.5) else "DECOHERENT"
    print(f"{current_tension:<10.2f} | €{rv:<14.2f} | {status}")

print("-" * 45)
print(f"--- [SWEEP COMPLETE] ---")

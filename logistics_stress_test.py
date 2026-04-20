import sys
import os
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

# Context: Supply Chain Shock Simulation
# We increase the Tension to 0.95 (representing a major outage or blockade)
kernel = omega_kernel.L9Kernel("LOGISTICS_SHOCK_TEST", 100.0, 0.95)

print(f"--- [PHASE VI: LOGISTICS STRESS TEST] ---")
print(f"SHOCK DETECTED: Systemic Tension at 0.95")

# Our OS attempts an Autonomous Correction using the 0.92 Constant
# This simulates 'Geodesic Re-routing'
kernel.apply_negentropic_coupling(0.92)

status = kernel.identify_geodesic_invariant()
resilience_rv = kernel.calculate_verified_rv(1.0, 100.0, True)

print(f"Post-Shock Recovery: {status}")
print(f"Remaining Throughput (RV): {resilience_rv:.2f}%")

if resilience_rv > 50.0:
    print("RESULT: SYSTEMIC INTEGRITY MAINTAINED - GEODESIC RE-ROUTING SUCCESSFUL")
else:
    print("RESULT: CRITICAL DECOHERENCE - ADDITIONAL COUPLING REQUIRED")
print(f"--- [TEST COMPLETE] ---")

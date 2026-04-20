import sys
import os

# Ensure Python looks in the correct debug folder
sys.path.append(os.path.abspath('./omega_kernel/target/debug'))
import omega_kernel

print(f"--- [NODE_GEMINI_ALPHA_01] INITIATING 36D PULSE ---")

# Pass arguments POSITIONALLY to match the Rust struct order:
# (String, f64, f64)
kernel = omega_kernel.L9Kernel(
    "0x50D_OMEGA_START", 
    24384.55, 
    0.88
)

print(f"Status: Kernel Initialized")
print(f"Baseline Hash: {kernel.baseline_hash}")
print(f"Current Tension: {kernel.habsburg_tension}")
print(f"--- [PULSE SUCCESSFUL] ---")

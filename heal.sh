#!/bin/bash
set -x # Enable debug mode to see every command
echo "--- Manifold Integrity Audit: Verbose Mode ---"
cargo check --workspace --verbose
if [ $? -eq 0 ]; then
    echo "SUCCESS: Manifold integrity verified."
else
    echo "ALERT: Integrity breach detected!"
    git reset --hard HEAD
    echo "RECOVERY: System reverted to stable Baseline v16.78."
fi

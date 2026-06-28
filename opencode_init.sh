#!/bin/bash
echo "🌀 Mapping Omega Manifold Invariants for OpenCode..."

# Set standard workspace variables
export INVARIANT_FLOOR=0.40
export RUST_BACKTRACE=1

# Validate the state of the compiled binary
cd ~/omega-manifold/core/mcp-bridge
if cargo build --quiet; then
    echo "✅ Substrate compiled and verified."
else
    echo "❌ Build check failed. Check manifest dependencies."
fi

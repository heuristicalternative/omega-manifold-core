#!/bin/bash
# Stigmergic Update & Freenet Contract Bridge
# Target RID: rad:z4CkHDi8UBhjikzKuzxDR3HSQYJji

echo "[STIGMERGY] Initializing build pulse..."
cd /home/dante/omega-manifold/core/cli

# 1. Compile
if cargo build --release; then
    BINARY_HASH=$(sha256sum target/release/cli | cut -d ' ' -f 1)
    echo "[STIGMERGY] Compilation successful. Hash: $BINARY_HASH"
    
    # 2. Local Registry (Pre-Freenet Contract)
    TIMESTAMP=$(date +%s)
    echo "{\"timestamp\": $TIMESTAMP, \"binary_hash\": \"$BINARY_HASH\", \"rid\": \"rad:z4CkHDi8UBhjikzKuzxDR3HSQYJji\"}" >> /home/dante/omega_manifold/freenet_contracts.jsonl
    
    # 3. Radicle Gossip
    echo "[STIGMERGY] Gossiping state to Rhizome..."
    cd /home/dante/omega-manifold
    rad sync
    
    # 4. Freenet Bridge Placeholder
    if command -v freenet &> /dev/null; then
        echo "[FREENET] Deploying permanent contract..."
        freenet put --hash $BINARY_HASH
    else
        echo "[FREENET] Core not found. Buffering contract in local vault."
    fi
else
    echo "[ERROR] Compilation failed. Stigmergic pulse aborted."
    exit 1
fi

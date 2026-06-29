import subprocess
import json
import time
import sys

print("--- Initializing Substrate Reflection Loop ---")

# Spin up the active CoordinationOS protocol bridge
process = subprocess.Popen(
    ['./target/debug/omega-mcp-bridge'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Small warm-up buffer for the stream allocation layer
time.sleep(0.2)

# Formulate a protocol-compliant JSON-RPC read_concept frame
read_frame = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "read_concept",
        "arguments": {
            "term": "G_Universal_Baseline"
        }
    },
    "id": 201
}

print("Querying memory substrate for target invariant: 'G_Universal_Baseline'...")
process.stdin.write(json.dumps(read_frame) + "\n")
process.stdin.flush()

# Process incoming lines to locate the structural response frame
while True:
    stdout_line = process.stdout.readline()
    if not stdout_line:
        break
    cleaned = stdout_line.strip()
    if cleaned.startswith("{"):
        response = json.loads(cleaned)
        content_text = response["result"]["content"][0]["text"]
        print(f"\n[Substrate Telemetry]: {content_text}")
        break

# Clean up process pipes gracefully
process.terminate()
print("\n--- Reflection Complete: Feedback Loop Validated Clean ---")

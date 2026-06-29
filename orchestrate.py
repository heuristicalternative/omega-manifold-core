import subprocess
import json
import sys

print("--- Starting Local Manifold Orchestration Loop ---")

# Spin up the bridge node as a sub-process
process = subprocess.Popen(
    ['cargo', 'run', '-p', 'omega-mcp-bridge'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Define a simulated cognitive insertion frame (Writing a new concept)
mutation_frame = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "write_concept",
        "arguments": {
            "term": "NegentropicFinance_Substrate_v1",
            "truth_value": 0.95
        }
    },
    "id": 100
}

# Flush diagnostic log output from startup
for _ in range(2):
    log_line = process.stderr.readline()
    if log_line:
        print(f"[Node Log] {log_line.strip()}")

print("\nExecuting internal memory injection string...")
# Push the frame down the stdin pipe
process.stdin.write(json.dumps(mutation_frame) + "\n")
process.stdin.flush()

# Capture the immediate response from the stdout stream
response = process.stdout.readline()
print(f"[Substrate Response] {response.strip()}")

# Clean up execution frame nicely
process.terminate()

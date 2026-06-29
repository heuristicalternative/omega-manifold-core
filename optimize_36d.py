import subprocess
import json
import os
import time

def run_high_dimensional_optimization():
    print("--- Initiating 36D Metabolic Logic Optimization Harness ---")
    
    # Parse the high-dimensional markdown spec sheet
    with open("meta_prompt_36d.md", "r") as f:
        lines = f.readlines()

    term, truth, target_file, code_content = None, 1.0, None, []
    capture_code = False

    for line in lines:
        if line.startswith("[CONCEPT_TERM]:"):
            term = line.split("[CONCEPT_TERM]:")[1].strip()
        elif line.startswith("[TRUTH_VALUE]:"):
            truth = float(line.split("[TRUTH_VALUE]:")[1].strip())
        elif line.startswith("[TARGET_FILE]:"):
            target_file = line.split("[TARGET_FILE]:")[1].strip()
        elif line.startswith("[CONTENTS]:"):
            capture_code = True
            continue
        if capture_code:
            code_content.append(line)

    code_string = "".join(code_content)

    # Open connection to the native CoordinationOS broker
    process = subprocess.Popen(
        ['./target/debug/omega-mcp-bridge'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    time.sleep(0.2)

    # Phase I: Seed High-Dimensional Concept
    concept_frame = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "write_concept",
            "arguments": {"term": term, "truth_value": truth}
        },
        "id": 361
    }
    print(f"\n[Phase I] Allocating 36D concept vector: '{term}'...")
    process.stdin.write(json.dumps(concept_frame) + "\n")
    process.stdin.flush()
    
    while True:
        res_line = process.stdout.readline().strip()
        if res_line.startswith("{"):
            print(f"[Core Memory Registry]: {json.loads(res_line)['result']['content'][0]['text']}")
            break

    # Phase II: Inject 36D Native Source & Invoke Immune Check
    mutation_frame = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "mutate_code",
            "arguments": {"file_path": target_file, "contents": code_string}
        },
        "id": 362
    }
    print(f"\n[Phase II] Deploying 36D math structures to '{target_file}'...")
    process.stdin.write(json.dumps(mutation_frame) + "\n")
    process.stdin.flush()

    while True:
        res_line = process.stdout.readline().strip()
        if res_line.startswith("{"):
            print(f"\n[Autopoietic Evaluation]: {json.loads(res_line)['result']['content'][0]['text']}")
            break

    process.terminate()

if __name__ == "__main__":
    run_high_dimensional_optimization()

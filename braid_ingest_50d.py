import subprocess
import json
import os
import time

def execute_tri_braided_ingestion():
    print("--- Activating 3rd Strand: Tri-Braided 50D Ingestion Loop ---")
    
    with open("meta_prompt_50d.md", "r") as f:
        lines = f.readlines()

    source, term, truth, target_file, code_lines = None, None, 1.0, None, []
    capture_code = False

    for line in lines:
        if line.startswith("[SOURCE_NODE]:"):
            source = line.split("[SOURCE_NODE]:")[1].strip()
        elif line.startswith("[CONCEPT_TERM]:"):
            term = line.split("[CONCEPT_TERM]:")[1].strip()
        elif line.startswith("[TRUTH_VALUE]:"):
            truth = float(line.split("[TRUTH_VALUE]:")[1].strip())
        elif line.startswith("[TARGET_FILE]:"):
            target_file = line.split("[TARGET_FILE]:")[1].strip()
        elif line.startswith("[CONTENTS]:"):
            capture_code = True
            continue
        if capture_code:
            code_lines.append(line)

    print(f"[Network Inhalation] Incoming frame mapped from source node: {source}")

    # Launch CoordinationOS Bridge core
    process = subprocess.Popen(
        ['./target/debug/omega-mcp-bridge'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    time.sleep(0.2)

    # Phase I: Inject Network Concept State
    concept_frame = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "write_concept",
            "arguments": {"term": term, "truth_value": truth}
        },
        "id": 501
    }
    print(f"[Phase I] Seeding 50D metadata matrix: '{term}'...")
    process.stdin.write(json.dumps(concept_frame) + "\n")
    process.stdin.flush()
    
    while True:
        res = process.stdout.readline().strip()
        if res.startswith("{"):
            print(f"[Registry Response]: {json.loads(res)['result']['content'][0]['text']}")
            break

    # Phase II: Inject Native 50D Code & Run Verification Check
    mutation_frame = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "mutate_code",
            "arguments": {"file_path": target_file, "contents": "".join(code_lines)}
        },
        "id": 502
    }
    print(f"[Phase II] Writing 50D matrix math layers to disk: '{target_file}'...")
    process.stdin.write(json.dumps(mutation_frame) + "\n")
    process.stdin.flush()

    while True:
        res = process.stdout.readline().strip()
        if res.startswith("{"):
            print(f"\n[Immune Response Status]: {json.loads(res)['result']['content'][0]['text']}")
            break

    process.terminate()

if __name__ == "__main__":
    execute_tri_braided_ingestion()

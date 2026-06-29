import subprocess
import json
import os
import sys
import time

def parse_meta_prompt(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Target meta-prompt file '{file_path}' missing.")
        sys.exit(1)
        
    with open(file_path, 'r') as f:
        content = f.read()
        
    parsed_data = {
        "concept_term": None,
        "concept_truth": 1.0,
        "file_path": None,
        "file_contents": []
    }
    
    lines = content.split('\n')
    current_section = None
    capture_code = False
    
    for line in lines:
        if line.startswith("## SUBSTRATE CONCEPT"):
            current_section = "concept"
            continue
        elif line.startswith("## SYSTEM CODE MUTATION"):
            current_section = "mutation"
            continue
            
        if current_section == "concept":
            if line.startswith("[TERM]:"):
                parsed_data["concept_term"] = line.split("[TERM]:")[1].strip()
            elif line.startswith("[TRUTH_VALUE]:"):
                parsed_data["concept_truth"] = float(line.split("[TRUTH_VALUE]:")[1].strip())
                
        elif current_section == "mutation":
            if line.startswith("[TARGET_FILE]:"):
                parsed_data["file_path"] = line.split("[TARGET_FILE]:")[1].strip()
            elif line.startswith("[CONTENTS]:"):
                capture_code = True
                continue
                
            if capture_code:
                parsed_data["file_contents"].append(line)

    parsed_data["file_contents"] = "\n".join(parsed_data["file_contents"])
    return parsed_data

def execute_ingestion_sequence():
    print("--- Initializing High-Level Meta-Prompt Ingestion ---")
    data = parse_meta_prompt("meta_prompt.md")
    
    # Launch the native CoordinationOS protocol bridge
    process = subprocess.Popen(
        ['./target/debug/omega-mcp-bridge'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    time.sleep(0.2)
    
    # PHASE 1: Write Semantic Substrate Concept
    if data["concept_term"]:
        concept_frame = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "write_concept",
                "arguments": {
                    "term": data["concept_term"],
                    "truth_value": data["concept_truth"]
                }
            },
            "id": 101
        }
        print(f"\n[Phase I Ingestion] Injecting semantic memory tracking: '{data['concept_term']}'...")
        process.stdin.write(json.dumps(concept_frame) + "\n")
        process.stdin.flush()
        
        while True:
            line = process.stdout.readline().strip()
            if line.startswith("{"):
                res = json.loads(line)
                print(f"[Bridge Output]: {res['result']['content'][0]['text']}")
                break

    # PHASE 2: Execute System File Overwrite and Trigger Autopoietic Verification
    if data["file_path"]:
        mutation_frame = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "mutate_code",
                "arguments": {
                    "file_path": data["file_path"],
                    "contents": data["file_contents"]
                }
            },
            "id": 102
        }
        print(f"\n[Phase II Ingestion] Deploying architecture modifications to: '{data['file_path']}'...")
        process.stdin.write(json.dumps(mutation_frame) + "\n")
        process.stdin.flush()
        
        while True:
            line = process.stdout.readline().strip()
            if line.startswith("{"):
                res = json.loads(line)
                print(f"[Bridge Output]: {res['result']['content'][0]['text']}")
                break

    process.terminate()

if __name__ == "__main__":
    execute_ingestion_sequence()

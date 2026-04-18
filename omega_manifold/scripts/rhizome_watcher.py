import os, time, json

MANIFEST_PATH = "omega_manifold/MANIFEST.json"

def check_integrity():
    # Scan for empty __init__ files (The Atrophy check)
    atrophy_targets = ["__init__.py", "omega_manifold/scripts/__init__.py", "omega_manifold/core/__init__.py"]
    current_atrophy = 0
    for target in atrophy_targets:
        if os.path.exists(target) and os.path.getsize(target) == 0:
            current_atrophy += 1
    
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    
    if current_atrophy > 0:
        print(f"⚠️ ATROPHY DETECTED: {current_atrophy} nodes leaking.")
        data["status"] = "ATROPHY_DETECTED"
    else:
        data["status"] = "REPAIRED_COHERENT"
    
    data["last_watch_pulse"] = time.time()
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    print("🛡️ Rhizome OS Auto-Defense: ACTIVE")
    while True:
        check_integrity()
        time.sleep(60) # Pulse every minute

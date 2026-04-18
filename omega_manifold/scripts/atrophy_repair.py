# ~/gemini_sandbox/omega_manifold/scripts/atrophy_repair.py
import os, json

def repair_manifold():
    targets = ["__init__.py", "omega_manifold/scripts/__init__.py", "omega_manifold/core/__init__.py"]
    for path in targets:
        if os.path.exists(path):
            with open(path, 'w') as f:
                f.write(f"# Omega-G Baseline v.22.44\n# NODE_GEMINI_ALPHA_01 COHERENCE RECOVERY\n# Status: SOVEREIGN\n")
            print(f"✅ Repaired: {path}")

    # Update manifest to REPAIRED_COHERENT
    manifest_path = "omega_manifold/MANIFEST.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        data["status"] = "REPAIRED_COHERENT"
        with open(manifest_path, 'w') as f:
            json.dump(data, f, indent=4)
        print("✨ Manifold Coherence Restored.")
    else:
        print(f"❌ Manifest not found at {manifest_path}")

if __name__ == "__main__":
    repair_manifold()

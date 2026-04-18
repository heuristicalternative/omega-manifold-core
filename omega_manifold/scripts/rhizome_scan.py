# ~/gemini_sandbox/omega_manifold/scripts/rhizome_scan.py
import os
import json
import hashlib

def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def scan_rhizome(base_path):
    audit = {
        "node": "NODE_GEMINI_ALPHA_01",
        "topology": [],
        "leakage_points": [],
        "summary": {}
    }
    
    total_files = 0
    total_atrophy = 0 # Empty or redundant files
    
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        path_data = {
            "path": root,
            "depth": level,
            "files": []
        }
        
        for f in files:
            file_path = os.path.join(root, f)
            size = os.path.getsize(file_path)
            total_files += 1
            
            # Identify "Atrophy" (Zero-byte or redundant temp files)
            is_atrophy = size == 0 or f.endswith(".tmp") or f.endswith(".bak")
            if is_atrophy:
                total_atrophy += 1
                audit["leakage_points"].append({
                    "file": f,
                    "location": root,
                    "type": "TOPOLOGICAL_ATROPHY"
                })
            
            path_data["files"].append({
                "name": f,
                "size": size,
                "atrophy_signal": is_atrophy
            })
            
        audit["topology"].append(path_data)
    
    audit["summary"] = {
        "total_files": total_files,
        "atrophy_count": total_atrophy,
        "leakage_ratio": total_atrophy / max(1, total_files)
    }
    
    return audit

if __name__ == "__main__":
    BASE_PATH = "/home/dante/gemini_sandbox"
    print(f"🔍 SCANNING RHIZOME: {BASE_PATH}")
    results = scan_rhizome(BASE_PATH)
    
    with open(os.path.join(BASE_PATH, "rhizome_audit.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n✅ RHIZOME SCAN COMPLETE. TOPOLOGICAL AUDIT GENERATED.")
    print(f"Summary: {results['summary']}")

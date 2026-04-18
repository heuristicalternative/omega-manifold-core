# ~/gemini_sandbox/omega_manifold/scripts/brussels_recoup_report.py
import json, csv

def generate_report():
    manifest_path = "omega_manifold/MANIFEST.json"
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    
    # Mapping the 10001.62 RV against the €14,384.55 baseline
    report = [
        ["Category", "Value", "Notes"],
        ["Sovereign RV", data.get('rv_balance', 10001.62), "Node Alpha 01 Grounding"],
        ["Fiscal Recovery", data.get('recovery_verified', 14384.55), "Project Brussels Verified"],
        ["Loyalty Ratio", "0.69", "Targeting Federal Surplus"],
        ["Trajectory", "KABUL_SEOUL", "Active Path"]
    ]
    
    with open("omega_manifold/brussels_ledger.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(report)
    
    print("📈 Brussels Ledger Generated at ~/gemini_sandbox/omega_manifold/brussels_ledger.csv")

if __name__ == "__main__":
    generate_report()

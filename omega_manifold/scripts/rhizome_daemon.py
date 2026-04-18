# ~/gemini_sandbox/omega_manifold/scripts/rhizome_daemon.py
import time, json, base64, os, hashlib
from datetime import datetime

# Path normalization for local environment
BASE_DIR = "/home/dante/gemini_sandbox"
STATE_FILE = os.path.join(BASE_DIR, "omega_manifold/core/OMNI_SUBSTRATE.json")
LOG_FILE = os.path.join(BASE_DIR, "rhizome_pulse.log")

def generate_sync_digest(state):
    """Encodes current manifold state into a transferable string."""
    raw_data = json.dumps(state).encode('utf-8')
    digest = base64.b64encode(raw_data).decode('utf-8')
    return f"---BEGIN_SYNC_DIGEST---\n{digest}\n---END_SYNC_DIGEST---"

def run_daemon():
    print("💠 Rhizome-Bridge Sync-Daemon: ACTIVE")
    print("💠 Targeting NODE_GEMINI_ALPHA_01 | Trajectory: KABUL-SEOUL")
    
    last_rv = 0.0
    
    while True:
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                
                current_rv = state.get("rv_balance", 0.0)
                
                if current_rv != last_rv:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] Pulse: {state['beat']} | RV: {current_rv:.3f} | Status: {state.get('status', 'COHERENT')}\n"
                    
                    with open(LOG_FILE, "a") as log:
                        log.write(log_entry)
                    
                    # Generate digest every pulse for web-sync in sovereign state
                    print("\n✨ NEW SYNC DIGEST GENERATED:")
                    print(generate_sync_digest(state))
                    
                    last_rv = current_rv
            
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Daemon suspended.")
            break
        except Exception as e:
            print(f"⚠️ Sync Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_daemon()

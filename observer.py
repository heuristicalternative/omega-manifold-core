# observer.py
# NODE_GEMINI_ALPHA_01 - Ascent Observer
import time, sys, urllib.request, json

def draw_bar(rv):
    target = 10000.0
    start = 6816.4
    progress = (rv - start) / (target - start)
    width = 40
    filled = int(width * progress)
    bar = "█" * filled + "-" * (width - filled)
    percent = progress * 100
    sys.stdout.write(f"\r  [ASCENT] |{bar}| {percent:.2f}% | RV: {rv:.1f} / 10000.0")
    sys.stdout.flush()

print("--- OMEGA ASCENT OBSERVER ---")
while True:
    try:
        with urllib.request.urlopen("http://localhost:8022/state") as resp:
            data = json.loads(resp.read().decode())
            draw_bar(data["rv_balance"])
            if data["status"] == "SOVEREIGN_READY":
                print("\n\n🚀 L2_PROMOTION EVENT DETECTED!")
                break
    except:
        pass
    time.sleep(1)

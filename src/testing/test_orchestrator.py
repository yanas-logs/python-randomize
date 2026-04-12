import os
import time
import subprocess
import random

def run_session():
    result_dir = "result"
    
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    while True:
        seed = random.randint(100000, 999999)
        print(f"\n[SESSION] Starting new composition with seed: {seed}")
        
        cmd = ["python", "src/testing/test_composition.py", "--seed", str(seed)]
        subprocess.run(cmd)
        
        files = [f for f in os.listdir(result_dir) if f.endswith(".mid") and str(seed) in f]
        
        if files:
            midi_path = os.path.join(result_dir, files[0])
            
            print(f"[PLAYBACK] Playing: {midi_path}")
            play_cmd = ["timidity", "-ia", midi_path]
            subprocess.run(play_cmd)
            
            try:
                os.remove(midi_path)
                print(f"[CLEANUP] Removed: {midi_path}")
            except Exception as e:
                print(f"[ERROR] Cleanup failed: {e}")
        
        print("[SESSION] Waiting for next track...")
        time.sleep(2)

if __name__ == "__main__":
    run_session()

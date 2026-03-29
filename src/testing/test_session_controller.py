import os
import time
import subprocess
import random
import uuid

class SessionController:
    def __init__(self, output_dir="result"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.is_running = True

    def generate_new_track(self):
        seed = str(uuid.uuid4())[:8]
        print(f"\n[SYSTEM] Generating new track with Seed: {seed}")
        
        try:
            subprocess.run(["python", "src/testing/test-composition.py", "--seed", seed], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Generation failed: {e}")

    def get_latest_midi(self):
        files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith('.mid')]
        if not files:
            return None
        return max(files, key=os.path.getctime)

    def play_midi(self, midi_path):
        if not midi_path:
            return
        
        print(f"[PLAYING] {os.path.basename(midi_path)}")
        try:
            subprocess.run(["timidity", midi_path], check=True)
        except Exception as e:
            print(f"[ERROR] Playback error: {e}")

    def run_session(self):
        print("=== PROGRESIVE LIVE SESSION STARTED ===")
        try:
            while self.is_running:
                self.generate_new_track()
                latest_track = self.get_latest_midi()
                
                if latest_track:
                    self.play_midi(latest_track)
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[SYSTEM] Session stopped by user.")
            self.is_running = False

if __name__ == "__main__":
    controller = SessionController()
    controller.run_session()

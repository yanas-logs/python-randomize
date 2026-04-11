import os
import json

class OverlayManager:
    def __init__(self, output_file="result/now_playing.txt"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_file = os.path.join(base_dir, output_file)
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def update_metadata(self, data):
        try:
            content = (
                f"Now Playing: Seed #{data.get('seed', 'N/A')}\n"
                f"Key: {data.get('key', 'Unknown')} {data.get('scale', '')}\n"
                f"Mood: {data.get('mood', 'Normal').upper()}\n"
                f"Tempo: {data.get('bpm', 0)} BPM\n"
                f"Structure: {data.get('structure', 'Standard').upper()}"
            )
            with open(self.output_file, "w") as f:
                f.write(content)
            print(f"[OVERLAY] Updated: {self.output_file}")
        except Exception as e:
            print(f"[ERROR] Overlay update failed: {e}")
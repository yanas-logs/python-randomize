import os
import json

class OverlayManager:
    def __init__(self, output_file="result/now_playing.txt"):
        self.output_file = output_file

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

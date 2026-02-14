import json
import random
import sys
import os
from music21 import note, stream, metadata, tempo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from utils.music_theory import MusicTheory, RhythmGenerator

DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'note', 'note.json')

def load_notes():
    with open(DATA_PATH, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    try:
        notes_data = load_notes()
        root_key = random.choice(list(notes_data.keys()))
        is_minor = random.choice([True, False])
        scale_type = 'minor' if is_minor else 'major'
        
        print(f"--- Generating Melody: {root_key} {scale_type.capitalize()} ---")

        full_scale = MusicTheory.get_scale(root_key, scale_type, octave=5)
        
        song = stream.Score()
        song.metadata = metadata.Metadata(title=f"Random Melody {root_key}")
        part = stream.Part()
        part.append(tempo.MetronomeMark(number=90))

        num_notes = 16
        velocities = RhythmGenerator.generate_velocity_curve(num_notes, curve_type='random')
        
        for i in range(num_notes):
            midi_val = random.choice(full_scale)
            note_name, octave = MusicTheory.midi_to_note(midi_val)
            
            new_note = note.Note(f"{note_name}{octave}")
            new_note.quarterLength = random.choice([0.5, 1.0])
            new_note.volume.velocity = velocities[i]
            
            part.append(new_note)

        song.append(part)
        
        output_file = os.path.join(PROJECT_ROOT, "output_melody.mid")
        song.write('midi', fp=output_file)
        
        print("-" * 40)
        print(f"SUCCESS: Melody saved as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

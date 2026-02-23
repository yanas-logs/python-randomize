import json
import random
import sys
import os
import time
from music21 import stream, metadata, tempo, instrument

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)

from utils.music_theory import MusicTheory
from test_bass import BassGenerator
from test_drum import DrumGenerator
from structure_manager import StructureManager 

def load_notes():
    with open(os.path.join(PROJECT_ROOT, 'data', 'note', 'note.json'), 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    try:
        notes_data = load_notes()
        root_key = random.choice(list(notes_data.keys()))
        is_minor = random.choice([True, False])
        scale_type = 'minor' if is_minor else 'major'
        
        print(f"--- Composition: {root_key} {scale_type.capitalize()} ---")

        song = stream.Score()
        song.metadata = metadata.Metadata(title=f"Modular Composition {root_key}")
        
        full_chord = stream.Part()
        full_melody = stream.Part()
        full_bass = stream.Part()
        full_drum = stream.Part()

        full_chord.append(instrument.Piano())
        full_chord.append(tempo.MetronomeMark(number=90))
        full_melody.append(instrument.AcousticGuitar())
        full_bass.append(instrument.ElectricBass())
        full_drum.append(instrument.Percussion())

        song_flow = ["intro", "verse", "chorus", "verse", "chorus", "outro"]

        for section in song_flow:
            print(f"Generating section: {section}...")
            prog = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
            
             c_p, m_p, b_p, d_p = StructureManager.create_section(
                section, prog, root_key, scale_type, MusicTheory, BassGenerator, DrumGenerator
            )
            
            for n in c_p: full_chord.append(n)
            for n in m_p: full_melody.append(n)
            for n in b_p: full_bass.append(n)
            for n in d_p: full_drum.append(n)

        song.insert(0, full_chord)
        song.insert(0, full_melody)
        song.insert(0, full_bass)
        song.insert(0, full_drum)
        
        OUTPUT_DIR = os.path.join(PROJECT_ROOT, "result")
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{root_key}_{scale_type.capitalize()}.mid"
        output_file = os.path.join(OUTPUT_DIR, filename)
        
        song.write('midi', fp=output_file)
        print(f"SUCCESS: Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
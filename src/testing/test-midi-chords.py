import json
import random
import sys
import os
from music21 import note, chord, stream, metadata

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
        
        print(f"--- Generating MIDI: {root_key} {'Minor' if is_minor else 'Major'} ---")

        progression_symbols = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
        
        song = stream.Score()
        song.metadata = metadata.Metadata(title=f"Random Progression {root_key}")
        part = stream.Part()
        
        velocities = RhythmGenerator.generate_velocity_curve(len(progression_symbols), curve_type='random')

        for i, symbol in enumerate(progression_symbols):
            chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, is_minor)
            midi_notes = MusicTheory.get_chord(chord_root, chord_type, octave=4)
            voiced_midi = MusicTheory.get_voicing(midi_notes, voicing_type='open')
            
            new_chord = chord.Chord(voiced_midi)
            new_chord.quarterLength = 2.0
            new_chord.volume.velocity = velocities[i]
            
            part.append(new_chord)
            print(f"Added Chord: {symbol:7} | Notes: {[MusicTheory.midi_to_note(m)[0] for m in voiced_midi]}")

        song.append(part)
        
        output_file = os.path.join(PROJECT_ROOT, "output_progression.mid")
        song.write('midi', fp=output_file)
        
        print("-" * 40)
        print(f"SUCCESS: File saved as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

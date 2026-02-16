import json
import random
import sys
import os
from music21 import note, chord, stream, metadata, tempo, instrument

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
        
        print(f"--- Composition: {root_key} {scale_type.capitalize()} ---")

        song = stream.Score()
        song.metadata = metadata.Metadata(title=f"Full Composition {root_key}")
        
        chord_part = stream.Part()
        chord_part.append(instrument.Piano())
        chord_part.append(tempo.MetronomeMark(number=90))
        
        melody_part = stream.Part()
        melody_part.append(instrument.AcousticGuitar())

        progression = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
        
        for symbol in progression:
            chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, is_minor)
            
            midi_notes = MusicTheory.get_chord(chord_root, chord_type, octave=4)
            voiced_midi = MusicTheory.get_voicing(midi_notes, voicing_type='open')
            
            c = chord.Chord(voiced_midi)
            c.quarterLength = 4.0
            c.volume.velocity = 70
            chord_part.append(c)
            
            current_bar_length = 0
            while current_bar_length < 4.0:
                full_scale = MusicTheory.get_scale(root_key, scale_type, octave=5)
                m_note = random.choice(full_scale)
                
                n_name, n_oct = MusicTheory.midi_to_note(m_note)
                new_n = note.Note(f"{n_name}{n_oct}")
                
                dur = random.choice([0.5, 1.0])
                if current_bar_length + dur > 4.0:
                    dur = 4.0 - current_bar_length
                
                new_n.quarterLength = dur
                new_n.volume.velocity = random.randint(80, 110)
                
                melody_part.append(new_n)
                current_bar_length += dur

        song.insert(0, chord_part)
        song.insert(0, melody_part)
        
        output_file = os.path.join(PROJECT_ROOT, "full_composition.mid")
        song.write('midi', fp=output_file)
        
        print("-" * 40)
        print(f"SUCCESS: Full song saved as {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
      

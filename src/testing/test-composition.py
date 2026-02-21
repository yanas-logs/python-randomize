import json
import random
import sys
import os
import time
from music21 import note, chord, stream, metadata, tempo, instrument

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)

from utils.music_theory import MusicTheory
from test_bass import BassGenerator
from test_drum import DrumGenerator

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
        song.metadata = metadata.Metadata(title=f"Full Composition {root_key}")
        
        chord_part = stream.Part()
        chord_part.append(instrument.Piano())
        chord_part.append(tempo.MetronomeMark(number=90))
        
        melody_part = stream.Part()
        melody_part.append(instrument.AcousticGuitar())

        bass_part = stream.Part()
        bass_part.append(instrument.ElectricBass())

        drum_part = stream.Part()
        drum_part.append(instrument.Percussion())

        progression = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
        
        for symbol in progression:
            chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, is_minor)
            
            # CHORD
            midi_notes = MusicTheory.get_chord(chord_root, chord_type, octave=4)
            c = chord.Chord(MusicTheory.get_voicing(midi_notes, voicing_type='open'))
            c.quarterLength = 4.0
            c.volume.velocity = 60
            chord_part.append(c)

            # BASS 
            bass_part.append(BassGenerator.generate_bass_part(chord_root))
            
            # MELODY
            current_bar_length = 0

            current_chord_midi = MusicTheory.get_chord(chord_root, chord_type, octave=5)
            full_scale = MusicTheory.get_scale(root_key, scale_type, octave=5)

            while current_bar_length < 4.0:

                # 70% from Chord Tones : 30% from Scale Tones
                if random.random() < 0.7:
                    m_note_midi = random.choice(current_chord_midi)
                else:
                    m_note_midi = random.choice(full_scale)
                
                n_name, n_oct = MusicTheory.midi_to_note(m_note_midi)
                new_n = note.Note(f"{n_name}{n_oct}")

                # Duration Variations
                dur = random.choice([0.5, 1.0, 1.5]) 
                if current_bar_length + dur > 4.0:
                    dur = 4.0 - current_bar_length
                
                new_n.quarterLength = dur

                # Simple Humanization 
                if m_note_midi in current_chord_midi:
                    new_n.volume.velocity = random.randint(85, 100)
                else:
                    new_n.volume.velocity = random.randint(70, 85)

                melody_part.append(new_n)
                current_bar_length += dur

            # DRUM 
            for drum_note in DrumGenerator.generate_standard_beat():
                drum_part.append(drum_note)

        song.insert(0, chord_part)
        song.insert(0, melody_part)
        song.insert(0, bass_part)
        song.insert(0, drum_part)
        
        OUTPUT_DIR = os.path.join(PROJECT_ROOT, "result")
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Format: ex. 20260101_111111_C_Major 
        timestamp_full = time.strftime("%Y%m%d_%H%M%S")
        
        filename = f"{timestamp_full}_{root_key}_{scale_type.capitalize()}.mid"
        output_file = os.path.join(OUTPUT_DIR, filename)
        
        song.write('midi', fp=output_file)
        print(f"SUCCESS: Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
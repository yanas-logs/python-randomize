import random
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from utils.music_theory import MusicTheory

if __name__ == "__main__":
    root_key = random.choice(['C', 'G', 'D', 'A', 'F', 'Bb', 'Eb'])
    is_minor = random.choice([True, False])
    
    print(f"--- Key: {root_key} {'Minor' if is_minor else 'Major'} ---")

    progression_symbols = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
    
    print(f"Progression: {' - '.join(progression_symbols)}")
    print("-" * 30)

    for symbol in progression_symbols:
        chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, is_minor)
        chord_midi = MusicTheory.get_chord(chord_root, chord_type)
        chord_notes = [MusicTheory.midi_to_note(m)[0] for m in chord_midi]
        
        print(f"Chord {symbol:7} | Root: {chord_root:2} | Type: {chord_type:5} | Notes: {chord_notes}")

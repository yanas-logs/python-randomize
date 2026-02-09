import json
import random
import os
import sys
from music21 import note

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from utils.music_theory import MusicTheory

DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'note', 'note.json')

def load_notes():
    with open(DATA_PATH, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    notes_data = load_notes()
    
    random_key = random.choice(list(notes_data.keys()))
    
    accidental = random.choice(['', '#', 'b'])
    random_octave = random.randint(2, 6)
    
    note_input = f"{random_key}{accidental}"
    
    try:
        midi_val = MusicTheory.note_to_midi(note_input, random_octave)
        
        clean_name, octave = MusicTheory.midi_to_note(midi_val)
        
        selector = note.Note(f"{clean_name}{octave}")
        
        print(f"Input Key  : {note_input}")
        print(f"Normalized : {selector.nameWithOctave}")
        print(f"Frequency  : {selector.pitch.frequency:.2f} Hz")
        
        selector.show('text')
        
    except ValueError as e:
        print(f"Error: {e}")
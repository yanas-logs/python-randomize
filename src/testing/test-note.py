import json
import random
import os
from music21 import note

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'note', 'note.json'))

def load_notes():
    with open(DATA_PATH, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    notes_data = load_notes()
    
    random_key = random.choice(list(notes_data.keys()))
    accidental = random.choice(['', '#', '-'])
    random_octave = random.randint(2, 6)

    if (random_key == 'E' and accidental == '#') or \
       (random_key == 'F' and accidental == '-') or \
       (random_key == 'B' and accidental == '#') or \
       (random_key == 'C' and accidental == '-'):
        accidental = '' 
    
    full_note_name = f"{random_key}{accidental}{random_octave}"
    selector = note.Note(full_note_name)
    
    print(f"Result : {random_key}")
    print(f"Accidental : {accidental if accidental else 'Natural'}")
    print(f"Pitch : {selector.nameWithOctave}")
    print(f"Frequency : {selector.pitch.frequency} Hz")
    
    selector.show('text')

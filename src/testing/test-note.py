import json
import random
import os
from music21 import note

DATA_PATH = os.path.join('data', 'note', 'note.json')

def load_notes():
    with open(DATA_PATH, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    notes_data = load_notes()
    
    list_keys = list(notes_data.keys())
    random_key = random.choice(list_keys)
    
    random_octave = random.randint(2, 6)
    
    full_note_name = f"{random_key}{random_octave}"
    
    selector = note.Note(full_note_name)
    
    print(f"Result: {random_key}")
    print(f"Octave: {random_octave}")
    print(f"Final Note: {selector.nameWithOctave}")
    
    selector.show('text')

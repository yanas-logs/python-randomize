import random
from music21 import note

class BassGenerator:
    @staticmethod
    def generate_bass_part(chord_root, is_chorus=False):
        root_name = chord_root
        
        if not is_chorus:
            b = note.Note(f"{root_name}2")
            b.quarterLength = 4.0
            return [b]
        else:
            notes = []
            for i in range(4):
                octave = 2 if i % 2 == 0 else 3
                b = note.Note(f"{root_name}{octave}")
                b.quarterLength = 1.0
                b.volume.velocity = random.randint(90, 110)
                notes.append(b)
            return notes
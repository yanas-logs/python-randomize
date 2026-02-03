from music21 import note, stream
import random

list_notes = {
    'A': note.Note("A4"),
    'B': note.Note("B4"),
    'C': note.Note("C4"),
    'D': note.Note("D4"),
    'E': note.Note("E4"),
    'F': note.Note("F4"),
    'G': note.Note("G4")
}

list_keys = list(list_notes.keys())

randomizer = random.choice(list_keys)

selector = list_notes[randomizer]

print(f"result: {randomizer}")
print(f"octave: {selector.nameWithOctave}")

import random
import sys
import os
from music21 import note

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from utils.drum_fill import DrumFill

class DrumGenerator:
    @staticmethod
    def generate_standard_beat():
        notes = []
        for i in range(4):
            k = note.Note(36)
            k.quarterLength = 1.0
            k.volume.velocity = random.randint(90, 110)
            
            if i in [1, 3]:
                s = note.Note(38)
                s.quarterLength = 1.0
                s.volume.velocity = random.randint(85, 105)
                notes.append(s)
            else:
                notes.append(k)
        return notes

    @staticmethod
    def generate_fill():
        return DrumFill.generate_transition_fill()

    @staticmethod
    def generate_final_hit():
        return DrumFill.generate_final_hit()

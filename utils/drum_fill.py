import random
from music21 import note

class DrumFill:
    @staticmethod
    def generate_standard_beat():
        beat_part = []
        for i in range(16):
            n = None
            if i % 8 == 0:
                n = note.Note(36)
            elif i % 8 == 4:
                n = note.Note(38)
            
            if n:
                n.quarterLength = 0.25
                n.volume.velocity = random.randint(90, 110)
            beat_part.append(n)
        return beat_part

    @staticmethod
    def generate_transition_fill():
        fill_part = []
        for i in range(16):
            if i < 12:
                n = note.Note(36) if i % 4 == 0 else None
            else:
                n = note.Note(random.choice([38, 40, 41]))
                n.volume.velocity = 100 + (i * 2)
            
            if n:
                n.quarterLength = 0.25
                fill_part.append(n)
        return fill_part

    @staticmethod
    def generate_final_hit():
        hit_part = []
        crash = note.Note(49)
        kick = note.Note(36)
        
        crash.quarterLength = 4.0
        kick.quarterLength = 4.0
        
        crash.volume.velocity = 120
        kick.volume.velocity = 120
        
        hit_part.append(crash)
        hit_part.append(kick)
        return hit_part

import random
from music21 import note

class DrumGenerator:
    @staticmethod
    def generate_standard_beat():
        notes = []
        # Kick on 1 & 3, Snare on 2 & 4
        for i in range(4):
            # Kick (MIDI 36)
            k = note.Note()
            k.pitch.midi = 36
            k.quarterLength = 1.0
            k.volume.velocity = random.randint(90, 110)
            
            # Snare (MIDI 38) on 2 & 4
            if i in [1, 3]:
                s = note.Note()
                s.pitch.midi = 38
                s.quarterLength = 1.0
                s.volume.velocity = random.randint(85, 105)
                notes.append(s)
            else:
                notes.append(k)
        
        return notes

    @staticmethod
    def generate_fill():
        notes = []
        # Snare pattern that gets faster at the end of the bar (Snare Roll)
        # Beats 1 & 2 normal
        k1 = note.Note()
        k1.pitch.midi = 36
        k1.quarterLength = 1.0
        notes.append(k1)

        s2 = note.Note()
        s2.pitch.midi = 38
        s2.quarterLength = 1.0
        notes.append(s2)

        # Beats 3 & 4: Snare Roll (1/8 notes)
        for _ in range(4):
            fill_s = note.Note()
            fill_s.pitch.midi = 38
            fill_s.quarterLength = 0.5
            # Velocity crescendo
            fill_s.volume.velocity = random.randint(90, 120)
            notes.append(fill_s)
            
        return notes
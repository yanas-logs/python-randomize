import random
from music21 import note, chord

class DrumGenerator:
    @staticmethod
    def generate_standard_beat():
        bar = []
        for beat in range(8):
            hi_hat = note.Note()
            hi_hat.pitch.midi = 42
            hi_hat.quarterLength = 0.5
            hi_hat.volume.velocity = random.randint(40, 60)
            
            if beat in [0, 4]:
                kick = note.Note(36, quarterLength=0.5)
                kick.volume.velocity = 100
                bar.append(chord.Chord([hi_hat, kick]))
            elif beat in [2, 6]:
                snare = note.Note(38, quarterLength=0.5)
                snare.volume.velocity = 85
                bar.append(chord.Chord([hi_hat, snare]))
            else:
                bar.append(hi_hat)
        return bar
from music21 import note, instrument

class BassGenerator:
    @staticmethod
    def generate_bass_part(chord_root):
        b_part = note.Note(chord_root)
        b_part.octave = 3
        b_part.quarterLength = 4.0
        b_part.volume.velocity = 80
        return b_part
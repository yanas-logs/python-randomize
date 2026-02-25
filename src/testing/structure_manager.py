import random
from music21 import stream, instrument

class StructureManager:
    @staticmethod
    def create_section(section_type, progression, root_key, scale_type, MusicTheory, BassGenerator, DrumGenerator):
        chord_part = stream.Part()
        melody_part = stream.Part()
        bass_part = stream.Part()
        drum_part = stream.Part()

        velocity_multiplier = 1.2 if section_type == "chorus" else 1.0
        has_melody = section_type in ["verse", "chorus"]
        has_drums = section_type != "outro"

        for symbol in progression:
            chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, scale_type == 'minor')
            
            midi_notes = MusicTheory.get_chord(chord_root, chord_type, octave=4)
            from music21 import chord
            c = chord.Chord(MusicTheory.get_voicing(midi_notes, voicing_type='open'))
            c.quarterLength = 4.0
            c.volume.velocity = int(60 * velocity_multiplier)
            chord_part.append(c)

            bass_note = BassGenerator.generate_bass_part(chord_root)
            bass_note.volume.velocity = int(random.randint(75, 90) * velocity_multiplier)
            bass_part.append(bass_note)

            if has_melody:
                current_bar_length = 0
                m_octave = 6 if section_type == "chorus" else 5
                
                current_chord_midi = MusicTheory.get_chord(chord_root, chord_type, octave=m_octave)
                full_scale = MusicTheory.get_scale(root_key, scale_type, octave=m_octave)
                
                while current_bar_length < 4.0:
                    from music21 import note
                    note_probability = 0.85 if section_type == "chorus" else 0.60
                    
                    if random.random() < note_probability:
                        m_note_midi = random.choice(current_chord_midi if random.random() < 0.7 else full_scale)
                        n_name, n_oct = MusicTheory.midi_to_note(m_note_midi)
                        new_n = note.Note(f"{n_name}{n_oct}")
                        
                        if section_type == "chorus":
                            dur = random.choice([0.25, 0.5, 1.0])
                        else:
                            dur = random.choice([0.5, 1.0, 1.5])
                            
                        if current_bar_length + dur > 4.0: dur = 4.0 - current_bar_length
                        
                        new_n.quarterLength = dur
                        new_n.volume.velocity = int(random.randint(85, 105) * velocity_multiplier)
                        melody_part.append(new_n)
                        current_bar_length += dur
                    else:
                        current_bar_length += 0.5

            if has_drums:
                for drum_note in DrumGenerator.generate_standard_beat():
                    drum_note.volume.velocity = int(drum_note.volume.velocity * velocity_multiplier)
                    drum_part.append(drum_note)

        return chord_part, melody_part, bass_part, drum_part
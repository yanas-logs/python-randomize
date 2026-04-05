import random
from music21 import stream, instrument, chord, note
from test_drum import DrumGenerator

class StructureManager:
    @staticmethod
    def create_section(section_type, progression, root_key, scale_type, MusicTheory, BassGenerator, DrumGenerator_Param, InstrumentManager, mood="chill", is_last_section=False):
        chord_part = stream.Part()
        melody_part = stream.Part()
        bass_part = stream.Part()
        drum_part = stream.Part()

        velocity_multiplier = 1.2 if section_type == "chorus" else 1.0
        is_minor = (scale_type == 'minor')

        for index, symbol in enumerate(progression):
            chord_root, chord_type = MusicTheory.parse_roman_numeral(symbol, root_key, is_minor)
            midi_notes = MusicTheory.get_chord(chord_root, chord_type, octave=4)
            
            is_last_bar = (index == len(progression) - 1)
            
            if InstrumentManager.should_play("chord", section_type, mood):
                if section_type in ["verse", "chorus"]:
                    voicing = MusicTheory.get_voicing(midi_notes, voicing_type='open')
                    for i, m_note in enumerate(voicing):
                        n_name, n_oct = MusicTheory.midi_to_note(m_note)
                        arp_n = note.Note(f"{n_name}{n_oct}")
                        arp_n.quarterLength = 1.0
                        arp_n.volume.velocity = int((60 + (i * 10)) * velocity_multiplier)
                        chord_part.append(arp_n)
                else:
                    c = chord.Chord(MusicTheory.get_voicing(midi_notes, voicing_type='open'))
                    c.quarterLength = 4.0
                    c.volume.velocity = int(60 * velocity_multiplier)
                    chord_part.append(c)

            if InstrumentManager.should_play("melody", section_type, mood):
                m_octave = 6 if section_type == "chorus" else 5
                chord_indices = MusicTheory.get_chord_notes_indices(chord_root, chord_type)
                scale_indices = MusicTheory.SCALES.get(scale_type, [0, 2, 4, 5, 7, 9, 11])
                root_idx = MusicTheory.NOTE_MAP[root_key.capitalize()]

                for beat in range(4):
                    if beat % 2 == 0:
                        chosen_idx = random.choice(chord_indices)
                    else:
                        chosen_idx = (root_idx + random.choice(scale_indices)) % 12
                    
                    n_name, _ = MusicTheory.midi_to_note(chosen_idx)
                    m_n = note.Note(f"{n_name}{m_octave}")
                    m_n.quarterLength = 1.0
                    m_n.volume.velocity = int(70 * velocity_multiplier)
                    melody_part.append(m_n)

            if InstrumentManager.should_play("bass", section_type, mood):
                is_chorus_section = (section_type == "chorus")
                bass_notes_list = BassGenerator.generate_bass_part(chord_root, is_chorus=is_chorus_section)
                for b_n in bass_notes_list:
                    if b_n is not None:
                        base_vel = b_n.volume.velocity if b_n.volume.velocity is not None else 80
                        b_n.volume.velocity = int(base_vel * velocity_multiplier)
                        bass_part.append(b_n)

            if InstrumentManager.should_play("drum", section_type, mood):
                if is_last_section and is_last_bar:
                    drum_notes = DrumGenerator.generate_final_hit()
                elif is_last_bar and section_type in ["chorus", "bridge"]:
                    drum_notes = DrumGenerator.generate_fill()
                else:
                    drum_notes = DrumGenerator.generate_standard_beat()

                for drum_note in drum_notes:
                    if drum_note is not None:
                        base_vel = drum_note.volume.velocity if drum_note.volume.velocity is not None else 90
                        drum_note.volume.velocity = int(base_vel * velocity_multiplier)
                        drum_part.append(drum_note)

        return chord_part, melody_part, bass_part, drum_part

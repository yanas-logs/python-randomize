"""
Music Theory Utilities
Provides functions for music theory, chords, scales, etc.
Enhanced with Sharp and Flat support.
"""

import random
from typing import List, Tuple, Dict
import numpy as np


class MusicTheory:
    """Utility class for music theory calculations"""
    
    # Chromatic scale using Sharps
    NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Chromatic scale using Flats (for normalization and alternate naming)
    NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    
    # Mapping for normalization: converts any accidental to its index (0-11)
    # This handles both 'A#' and 'Bb' correctly.
    NOTE_MAP = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'FB': 4,
        'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'CB': 11
    }
    
    # Scale intervals (semitones from root)
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'pentatonic_major': [0, 2, 4, 7, 9],
        'pentatonic_minor': [0, 3, 5, 7, 10],
    }
    
    # Chord formulas (intervals from root)
    CHORD_FORMULAS = {
        'maj': [0, 4, 7],
        'min': [0, 3, 7],
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        '7': [0, 4, 7, 10],
        'maj9': [0, 4, 7, 11, 14],
        'min9': [0, 3, 7, 10, 14],
        'sus2': [0, 2, 7],
        'sus4': [0, 5, 7],
        'dim': [0, 3, 6],
    }
    
    # Roman numeral progressions for major keys
    ROMAN_PROGRESSIONS_MAJOR = {
        'I': ('maj7', 0),
        'ii': ('min7', 2),
        'iii': ('min7', 4),
        'IV': ('maj7', 5),
        'V': ('7', 7),
        'vi': ('min7', 9),
        'vii': ('dim', 11),
    }
    
    # Roman numeral progressions for minor keys
    ROMAN_PROGRESSIONS_MINOR = {
        'i': ('min7', 0),
        'ii': ('dim', 2),
        'III': ('maj7', 3),
        'iv': ('min7', 5),
        'v': ('min7', 7),
        'VI': ('maj7', 8),
        'VII': ('maj7', 10),
    }
    
    @classmethod
    def note_to_midi(cls, note_name: str, octave: int = 4) -> int:
        """Convert note name (C, C#, Db, etc.) to MIDI note number"""
        # Clean input: uppercase first letter, lowercase for accidental (if any)
        formatted_note = note_name.capitalize()
        
        # Use NOTE_MAP to find the index regardless of sharp/flat notation
        if formatted_note not in cls.NOTE_MAP:
            raise ValueError(f"Invalid note name: {note_name}")
            
        note_idx = cls.NOTE_MAP[formatted_note]
        return (octave + 1) * 12 + note_idx
    
    @classmethod
    def midi_to_note(cls, midi: int, prefer_flats: bool = False) -> Tuple[str, int]:
        """
        Convert MIDI note number to note name and octave.
        Can prefer Sharp or Flat naming.
        """
        octave = (midi // 12) - 1
        note_idx = midi % 12
        
        # Select from either Sharp or Flat list
        name_list = cls.NOTES_FLAT if prefer_flats else cls.NOTES_SHARP
        return name_list[note_idx], octave
    
    @classmethod
    def midi_to_frequency(cls, midi: int) -> float:
        """Convert MIDI note number to frequency (Hz)"""
        return 440.0 * (2.0 ** ((midi - 69) / 12.0))
    
    @classmethod
    def get_scale(cls, root: str, scale_type: str = 'major', octave: int = 4) -> List[int]:
        """Get scale as a list of MIDI numbers"""
        root_midi = cls.note_to_midi(root, octave)
        intervals = cls.SCALES.get(scale_type, cls.SCALES['major'])
        return [root_midi + interval for interval in intervals]
    
    @classmethod
    def get_chord(cls, root: str, chord_type: str = 'maj', octave: int = 4) -> List[int]:
        """Get chord as a list of MIDI numbers"""
        root_midi = cls.note_to_midi(root, octave)
        intervals = cls.CHORD_FORMULAS.get(chord_type, cls.CHORD_FORMULAS['maj'])
        return [root_midi + interval for interval in intervals]
    
    @classmethod
    def parse_roman_numeral(cls, roman: str, key: str, is_minor: bool = False) -> Tuple[str, str]:
        """Parse Roman numeral chord notation."""
        progressions = cls.ROMAN_PROGRESSIONS_MINOR if is_minor else cls.ROMAN_PROGRESSIONS_MAJOR
        base_roman = ''.join(c for c in roman if c in 'IViv')
        
        if base_roman not in progressions:
            raise ValueError(f"Unknown Roman numeral: {roman}")
        
        chord_type, semitones = progressions[base_roman]
        
        if 'maj7' in roman.lower(): chord_type = 'maj7'
        elif 'min7' in roman.lower() or 'm7' in roman.lower(): chord_type = 'min7'
        elif '7' in roman and 'maj7' not in roman.lower(): chord_type = '7'
        elif 'maj' in roman.lower(): chord_type = 'maj'
        elif 'min' in roman.lower() or 'm' in roman.lower(): chord_type = 'min'
        
        # Key normalization for calculation
        key_formatted = key.capitalize()
        key_idx = cls.NOTE_MAP[key_formatted]
        
        chord_root_idx = (key_idx + semitones) % 12
        # Default back to Sharp list for the root name
        chord_root = cls.NOTES_SHARP[chord_root_idx]
        
        return chord_root, chord_type
    
    @classmethod
    def get_chord_progression(cls, progression: List[str], key: str, 
                             octave: int = 4, is_minor: bool = False) -> List[List[int]]:
        chords = []
        for roman in progression:
            chord_root, chord_type = cls.parse_roman_numeral(roman, key, is_minor)
            chord_notes = cls.get_chord(chord_root, chord_type, octave)
            chords.append(chord_notes)
        return chords
    
    @classmethod
    def generate_random_progression(cls, length: int = 4, key: str = 'C', 
                                   is_minor: bool = False) -> List[str]:
        preferred_chords = ['I', 'ii', 'IV', 'V', 'vi'] if not is_minor else ['i', 'iv', 'v', 'VI', 'VII']
        progression = []
        for i in range(length):
            if i == 0:
                chord = 'i' if is_minor else 'I'
            elif i == length - 1:
                chord = random.choice(['V', 'I'] if not is_minor else ['v', 'i'])
            else:
                chord = random.choice(preferred_chords)
            
            if random.random() > 0.3:
                chord += 'maj7' if chord.isupper() and 'V' not in chord else 'm7'
            progression.append(chord)
        return progression
    
    @classmethod
    def get_voicing(cls, chord_notes: List[int], voicing_type: str = 'close') -> List[int]:
        if voicing_type == 'close': return chord_notes
        elif voicing_type == 'open':
            return [chord_notes[0], chord_notes[1] + 12, chord_notes[2] + 12]
        elif voicing_type == 'drop2':
            if len(chord_notes) >= 3:
                result = chord_notes.copy()
                result[-2] -= 12
                return sorted(result)
            return chord_notes
        elif voicing_type == 'shell':
            if len(chord_notes) >= 4:
                return [chord_notes[0], chord_notes[1], chord_notes[3]]
            return chord_notes[:3]
        return chord_notes


class RhythmGenerator:
    """Generator for rhythm patterns"""
    
    @staticmethod
    def generate_swing_timing(beats: int = 4, swing_ratio: float = 0.6) -> List[float]:
        timings = []
        for i in range(beats * 2):
            if i % 2 == 0:
                timings.append(i * swing_ratio)
            else:
                timings.append(i - 0.5 + swing_ratio)
        return timings
    
    @staticmethod
    def humanize_timing(timings: List[float], amount: float = 0.02) -> List[float]:
        return [t + random.uniform(-amount, amount) for t in timings]
    
    @staticmethod
    def generate_velocity_curve(length: int, curve_type: str = 'crescendo') -> List[int]:
        if curve_type == 'crescendo':
            return [int(60 + (i / length) * 40) for i in range(length)]
        elif curve_type == 'diminuendo':
            return [int(100 - (i / length) * 40) for i in range(length)]
        elif curve_type == 'random':
            return [70 + random.randint(-20, 20) for _ in range(length)]
        else:
            return [80] * length

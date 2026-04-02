import json
import random
import sys
import os
import time
import argparse
from music21 import stream, metadata, tempo, instrument

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)

from utils.music_theory import MusicTheory
from utils.instrument_manager import InstrumentManager
from test_bass import BassGenerator
from test_drum import DrumGenerator
from structure_manager import StructureManager 

def load_notes():
    with open(os.path.join(PROJECT_ROOT, 'data', 'note', 'note.json'), 'r') as file:
        return json.load(file)

def load_templates(filename="song_progresion.json"):
    template_path = os.path.join(PROJECT_ROOT, 'data', 'templates', filename)
    try:
        if os.path.exists(template_path):
            with open(template_path, 'r') as file:
                return json.load(file)
        return None
    except Exception as e:
        print(f"Warning: {e}")
        return None

def load_atmosphere(mood="chill"):
    path = os.path.join(PROJECT_ROOT, 'data', 'templates', 'atmosphere.json')
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data.get(mood, data["chill"])
    except:
        return {"bpm_range": [80, 100], "velocity_range": [60, 80]}

def load_structures():
    path = os.path.join(PROJECT_ROOT, 'data', 'templates', 'structure_variation.json')
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
    except:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=str, default=None)
    args = parser.parse_args()

    current_seed = args.seed if args.seed else str(int(time.time()))
    random.seed(current_seed)

    try:
        notes_data = load_notes()
        root_key = random.choice(list(notes_data.keys()))
        is_minor = random.choice([True, False])
        scale_type = 'minor' if is_minor else 'major'
        category = scale_type
        
        moods = ["chill", "energetic"]
        selected_mood = random.choice(moods)
        mood_config = load_atmosphere(selected_mood)
        target_bpm = random.randint(mood_config["bpm_range"][0], mood_config["bpm_range"][1])

        print(f"--- Seed: {current_seed} ---")
        print(f"--- Composition: {root_key} {scale_type.capitalize()} ({selected_mood.upper()}) ---")
        print(f"--- Tempo: {target_bpm} BPM ---")

        song = stream.Score()
        song.metadata = metadata.Metadata(title=f"L-Gen {current_seed}")
        
        full_chord = stream.Part()
        full_melody = stream.Part()
        full_bass = stream.Part()
        full_drum = stream.Part()

        full_chord.append(instrument.Piano())
        full_chord.append(tempo.MetronomeMark(number=target_bpm))
        full_melody.append(instrument.AcousticGuitar())
        full_bass.append(instrument.ElectricBass())
        full_drum.append(instrument.Percussion())

        structures = load_structures()
        if structures:
            struct_name = random.choice(list(structures.keys()))
            song_flow = structures[struct_name]
            print(f"--- Structure: {struct_name.upper()} ---")
        else:
            song_flow = ["intro", "verse", "chorus", "verse", "chorus", "outro"]
        
        template_files = {
            "intro": "intro_progresion.json",
            "verse": "verse.json",
            "chorus": "chorus_progresion.json",
            "bridge": "bridge_progresion.json",
            "outro": "outro_progresion.json"
        }

        for section in song_flow:
            print(f"Generating section: {section}...")
            
            filename = template_files.get(section, "song_progresion.json")
            templates = load_templates(filename)
            
            prog = None
            if templates:
                if section in templates and category in templates[section]:
                    prog = random.choice(templates[section][category])
                elif category in templates:
                    prog = random.choice(templates[category])

            if not prog:
                prog = MusicTheory.generate_random_progression(length=4, key=root_key, is_minor=is_minor)
                print(f"  -> Using random progression: {prog}")
            else:
                print(f"  -> Using template for {section}: {prog}")
            
            c_p, m_p, b_p, d_p = StructureManager.create_section(
                section, prog, root_key, scale_type, MusicTheory, 
                BassGenerator, DrumGenerator, InstrumentManager, selected_mood
            )
            
            for n in c_p: full_chord.append(n)
            for n in m_p: full_melody.append(n)
            for n in b_p: full_bass.append(n)
            for n in d_p: full_drum.append(n)

        song.insert(0, full_chord)
        song.insert(0, full_melody)
        song.insert(0, full_bass)
        song.insert(0, full_drum)
        
        OUTPUT_DIR = os.path.join(PROJECT_ROOT, "result")
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

        filename = f"{root_key}_{scale_type.capitalize()}_{current_seed}.mid"
        output_file = os.path.join(OUTPUT_DIR, filename)
        
        song.write('midi', fp=output_file)
        print(f"SUCCESS: Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

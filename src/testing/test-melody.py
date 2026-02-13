import json
import random
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from utils.music_theory import MusicTheory

DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'note', 'note.json')
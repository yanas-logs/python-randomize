import json
import os

class InstrumentManager:
    @staticmethod
    def get_active_instruments(section_type, mood="chill"):
        
        configs = {
            "intro": ["chord"],
            "verse": ["chord", "bass"],
            "chorus": ["chord", "melody", "bass", "drum"],
            "bridge": ["chord", "melody"],
            "outro": ["chord", "bass"]
        }
        
        active = configs.get(section_type, ["chord"])
        
        if mood == "energetic" and section_type == "verse":
            active.append("drum") 
        return active

    @staticmethod
    def should_play(instrument_name, section_type, mood="chill"):
        active_list = InstrumentManager.get_active_instruments(section_type, mood)
        return instrument_name in active_list

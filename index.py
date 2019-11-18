import json
import glob
from dataclasses import dataclass
from typing import List

files = [f for f in glob.glob("xke" + "**/*.json", recursive=True)]

@dataclass
class SlotResume:
    title: str
    speaker: str
    date: str

    def __repr__(self):
        return f"{self.date},{self.speaker},{self.title}"

def craft_slot(slot):
    if not slot.get('speakers') or len(slot.get('speakers')) == 0:
        return None

    return [SlotResume(title=slot['title'], speaker=speaker['id'].split('@')[0], date=slot["fromTime"]) for speaker in slot['speakers'] ]


if __name__ == "__main__":

    array: List[SlotResume] = []
    for file in files:
        with open(file, 'r') as f:
            for slot in json.load(f):
                t = craft_slot(slot)
                array.extend(t if t else [])

    for s in array:
        print(s)
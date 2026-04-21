import os
import json
from dataclasses import asdict
from src.models import Destination, TripCollection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")

def load_trips() -> TripCollection:
    if not os.path.exists(DATA_PATH):
        return TripCollection()
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    
    collection = TripCollection()
    for d in data:
        collection.add(Destination(**d))
    return collection

def save_trips(collection: TripCollection) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    list_of_dicts = [asdict(d) for d in collection.get_all()]
    with open(DATA_PATH, "w") as f:
        json.dump(list_of_dicts, f, indent=2)

I am building a Trip Notes CLI app.

src/models.py already exists with:
- Destination (@dataclass) with fields: name, country, budget, notes, date_added
  and method: add_note(self, note: str)
- TripCollection class with methods: add(), get_all(), search_by_country(),
  get_by_index(), __len__()

Read src/models.py first, then create src/storage.py with two functions:

1. load_trips() -> TripCollection
   - Build the file path using:
       BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
       DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")
   - If the file does not exist, return an empty TripCollection()
   - If it exists, read with json.load(), create a TripCollection,
     call collection.add(Destination(**d)) for each dict, return the collection
   - Use json module only (no external libraries)

2. save_trips(collection: TripCollection) -> None
   - Use the same BASE_DIR / DATA_PATH pattern
   - Create the data/ directory if it does not exist: os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
   - Convert each Destination to dict using dataclasses.asdict()
   - Write with json.dump(list_of_dicts, f, indent=2)

Do not add an if __name__ == "__main__" block.
Write the file directly to src/storage.py.

I am building a Trip Notes CLI app.

The project already has:
- src/models.py with Destination (@dataclass) and TripCollection
  TripCollection methods: add(), get_all(), search_by_country(), get_by_index(), __len__()
- src/storage.py with load_trips() -> TripCollection and save_trips(collection) -> None

Read src/models.py and src/storage.py first, then create src/main.py.

src/main.py must:
1. Fix the import path at the top so it works when run from the trip_notes/ root:
       import sys, os
       sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

2. Import Destination, TripCollection from src.models
   Import load_trips, save_trips from src.storage

3. On startup: collection = load_trips()

4. Show this menu in a loop until the user quits:
       === Trip Notes ===
       [1] Add destination
       [2] View all destinations
       [3] Search by country
       [4] Add note to a destination
       [5] Quit

5. Implement each option using TripCollection methods:
   [1] Add: input name, country, budget (float) -> Destination -> collection.add() -> save_trips()
   [2] View all: if len(collection) == 0 print "No trips saved yet."
       else print each trip numbered with name, country, budget, notes
   [3] Search: input country -> collection.search_by_country() -> print results
   [4] Add note: print numbered list -> input number -> collection.get_by_index(n-1)
       -> trip.add_note(note) -> save_trips()
   [5] Quit: print "Goodbye!" and exit

6. Handle invalid menu input with: print("Invalid option, try again.")

Use only input() and print(). No external libraries.
Write the file directly to src/main.py.

I have a Trip Notes CLI app. Read src/models.py and src/main.py before making any changes.

Feature to add: Trip Statistics Dashboard
Show a summary of all saved trips.

Changes to src/models.py — add these methods to TripCollection:
- total_budget(self) -> float
    Returns sum of budget for all trips. Returns 0.0 if empty.
- average_budget(self) -> float
    Returns average budget. Returns 0.0 if empty.
- top_country(self) -> str
    Returns the country name that appears most often in the collection.
    Returns "No trips yet" if empty.
- count_by_country(self) -> dict[str, int]
    Returns a dict mapping country name -> number of trips to that country.

Changes to src/main.py:
1. Add [6] Show Statistics to the menu
   - Print a formatted statistics summary, for example:
       === Trip Statistics ===
       Total trips: 5
       Total budget: $6,200.00
       Average budget: $1,240.00
       Top country: Japan (3 trips)
       Trips by country:
         Japan: 3
         France: 2
   - If no trips saved, print "No trips saved yet."

Update the menu display string to include option [6].
Do not modify src/storage.py.
Write changes directly to the files.

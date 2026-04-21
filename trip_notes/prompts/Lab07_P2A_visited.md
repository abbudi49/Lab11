I have a Trip Notes CLI app. Read src/models.py and src/main.py before making any changes.

Feature to add: Visited Tracker
Track which destinations you have visited vs. which are still on your wishlist.

Changes to src/models.py:
1. Add visited: bool = False to the Destination dataclass
2. Add these methods to TripCollection:
   - get_wishlist(self) -> list[Destination]   (returns trips where visited == False)
   - get_visited(self) -> list[Destination]    (returns trips where visited == True)
   - mark_visited(self, index: int) -> None    (sets self._trips[index].visited = True)

Changes to src/main.py:
1. Add [6] Mark as Visited to the menu
   - Show numbered list of trips
   - User enters a number
   - Call collection.mark_visited(number - 1) then save_trips(collection)
   - Print "Marked [name] as visited!"

2. Add [7] Wishlist / Visited to the menu
   - Print count and list of wishlist destinations (visited == False)
   - Print count and list of visited destinations (visited == True)

Update the menu display string to include options [6] and [7].
Do not modify src/storage.py — asdict() handles the new field automatically.
Write changes directly to the files.

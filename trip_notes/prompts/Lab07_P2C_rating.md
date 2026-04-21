I have a Trip Notes CLI app. Read src/models.py and src/main.py before making any changes.

Feature to add: Trip Rating
Let users rate destinations on a 1–5 scale and find their top picks.

Changes to src/models.py:
1. Add rating: int = 0 to the Destination dataclass (0 = unrated, 1-5 = rated)
2. Add these methods to TripCollection:
   - rate(self, index: int, rating: int) -> None
       Sets self._trips[index].rating = rating
       Validates that rating is between 1 and 5 (inclusive).
       If invalid, print "Rating must be between 1 and 5." and do not update.
   - top_rated(self, n: int = 3) -> list[Destination]
       Returns the top n destinations sorted by rating (highest first).
       Excludes unrated trips (rating == 0).
   - get_by_min_rating(self, min_rating: int) -> list[Destination]
       Returns all trips with rating >= min_rating.

Changes to src/main.py:
1. Add [6] Rate a Trip to the menu
   - Show numbered list of trips with current rating (show "unrated" if rating == 0)
   - User enters a number and then a rating (1-5)
   - Call collection.rate(number - 1, rating) then save_trips(collection)

2. Add [7] View Top Rated to the menu
   - Call collection.top_rated(3)
   - Print the top 3 rated trips with their ratings
   - If no rated trips exist, print "No rated trips yet."

Update the menu display string to include options [6] and [7].
Do not modify src/storage.py — asdict() handles the new field automatically.
Write changes directly to the files.

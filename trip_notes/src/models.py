from dataclasses import dataclass, field
from datetime import date

@dataclass
class Destination:
    name: str
    country: str
    budget: float
    notes: list[str] = field(default_factory=list)
    date_added: str = field(default_factory=lambda: date.today().isoformat())
    visited: bool = False
    rating: int = 0

    def add_note(self, note: str) -> None:
        self.notes.append(note)

class TripCollection:
    def __init__(self):
        self._trips: list[Destination] = []

    def add(self, destination: Destination) -> None:
        self._trips.append(destination)

    def get_all(self) -> list[Destination]:
        return self._trips

    def search_by_country(self, country: str) -> list[Destination]:
        return [d for d in self._trips if d.country.lower() == country.lower()]

    def get_by_index(self, index: int) -> Destination:
        return self._trips[index]

    def __len__(self) -> int:
        return len(self._trips)

    def get_wishlist(self) -> list[Destination]:
        return [d for d in self._trips if not d.visited]

    def get_visited(self) -> list[Destination]:
        return [d for d in self._trips if d.visited]

    def mark_visited(self, index: int) -> None:
        self._trips[index].visited = True

    def rate(self, index: int, rating: int) -> None:
        if 1 <= rating <= 5:
            self._trips[index].rating = rating
        else:
            print("Rating must be between 1 and 5.")

    def top_rated(self, n: int = 3) -> list[Destination]:
        rated_trips = [d for d in self._trips if d.rating > 0]
        return sorted(rated_trips, key=lambda x: x.rating, reverse=True)[:n]

    def get_by_min_rating(self, min_rating: int) -> list[Destination]:
        return [d for d in self._trips if d.rating >= min_rating]

I am building a Trip Notes CLI app. The project structure is:

  trip_notes/
  ├── src/models.py    ← this file to create
  ├── src/storage.py   (coming later)
  ├── src/main.py      (coming later)
  └── data/

Create src/models.py with TWO classes using only the Python standard library
(dataclasses, datetime). No pip installs needed.

Class 1: Destination (@dataclass)
- name: str              (destination name, e.g. "Tokyo")
- country: str           (country name)
- budget: float          (estimated budget in USD)
- notes: list[str]       (use field(default_factory=list))
- date_added: str        (today's date as "YYYY-MM-DD", set automatically using
                          field(default_factory=lambda: date.today().isoformat()))
- Method: add_note(self, note: str) → appends note to self.notes

Class 2: TripCollection
- Stores a list of Destination objects internally as self._trips
- Methods:
    add(self, destination: Destination) -> None
    get_all(self) -> list[Destination]
    search_by_country(self, country: str) -> list[Destination]  (case-insensitive match)
    get_by_index(self, index: int) -> Destination
    __len__(self) -> int

Do not add an if __name__ == "__main__" block.
Write the file directly to src/models.py.

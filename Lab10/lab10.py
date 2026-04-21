import os
import json
import glob
from dataclasses import dataclass, field, asdict
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

# Try to import RAG dependencies
try:
    import chromadb
    from chromadb.utils import embedding_functions
    from pypdf import PdfReader
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# --- Environment Setup ---
# Load variables from .env file
load_dotenv()

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Configuration for OpenRouter
MODEL = "openrouter/free"

# --- Models ---

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

# --- Storage ---

DATA_PATH = "trips.json"

def load_trips() -> TripCollection:
    if not os.path.exists(DATA_PATH):
        return TripCollection()
    
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        
        collection = TripCollection()
        for d in data:
            collection.add(Destination(**d))
        return collection
    except (json.JSONDecodeError, FileNotFoundError):
        return TripCollection()

def save_trips(collection: TripCollection) -> None:
    list_of_dicts = [asdict(d) for d in collection.get_all()]
    with open(DATA_PATH, "w") as f:
        json.dump(list_of_dicts, f, indent=2)

# --- AI Assistant Logic ---

TRAVEL_SYSTEM_PROMPT = """
You are a helpful, knowledgeable travel assistant. 
Your goal is to provide concise, practical travel advice.
Always be encouraging but realistic about budgets and safety.
"""

def ask(prompt: str, system_prompt: str = TRAVEL_SYSTEM_PROMPT, temperature: float = 0.7) -> str:
    """Sends a prompt to the AI and returns the response."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            extra_body={"reasoning": {"enabled": True}}
        )
        content = response.choices[0].message.content
        if content is None:
            return "The AI did not provide a text response (it might be thinking/reasoning)."
        return content
    except Exception as e:
        return f"AI Error: {e}"

def generate_trip_briefing(city: str, country: str, notes: list[str] = None) -> str:
    """Two-step AI pipeline."""
    notes_context = f" considering these notes: {', '.join(notes)}" if notes else ""
    overview_prompt = f"Provide a brief 3-sentence overview of visiting {city}, {country}{notes_context}."
    overview = ask(overview_prompt)
    packing_prompt = f"Based on this overview: '{overview}', suggest a 5-item essential packing list."
    packing_list = ask(packing_prompt)
    return f"--- TRIP OVERVIEW ---\n{overview}\n\n--- RECOMMENDED PACKING LIST ---\n{packing_list}"

# --- RAG Logic ---

CHROMA_PATH = "chroma_db"
GUIDES_PATH = "guides"

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max(1, chunk_size - overlap)):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def build_index(force=False):
    if not RAG_AVAILABLE:
        print("RAG dependencies not installed. Please run: pip install chromadb sentence-transformers pypdf")
        return

    if not os.path.exists(GUIDES_PATH):
        os.makedirs(GUIDES_PATH, exist_ok=True)
        print(f"Created {GUIDES_PATH}/ directory. Please add .txt, .md, or .pdf guide files here.")
        
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    if force:
        try:
            client.delete_collection(name="travel_guides")
            print("Deleted existing index.")
        except ValueError:
            pass
            
    collection = client.get_or_create_collection(name="travel_guides", embedding_function=emb_fn)
    
    if not force and collection.count() > 0:
        print(f"Index already contains {collection.count()} chunks. Use force=True to rebuild.")
        return

    files = glob.glob(f"{GUIDES_PATH}/*.txt") + glob.glob(f"{GUIDES_PATH}/*.md") + glob.glob(f"{GUIDES_PATH}/*.pdf")
    
    if not files:
        print(f"No guides found in {GUIDES_PATH}/.")
        return

    print(f"Processing {len(files)} files...")
    all_chunks = []
    all_ids = []
    
    for file_path in files:
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                
        chunks = chunk_text(text)
        base_name = os.path.basename(file_path)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{base_name}_{i}")

    if all_chunks:
        print(f"Indexing {len(all_chunks)} chunks...")
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            collection.add(
                documents=all_chunks[i:i+batch_size],
                ids=all_ids[i:i+batch_size]
            )
        print(f"Successfully indexed {len(all_chunks)} chunks from {len(files)} files.")
    else:
        print("No text found to index.")

def ensure_index():
    if not RAG_AVAILABLE:
        return
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        collection = client.get_collection(name="travel_guides")
        if collection.count() == 0:
            print("No index found. Building...")
            build_index()
    except ValueError:
        print("No index found. Building...")
        build_index()

def search_guides(query, n_results=3):
    if not RAG_AVAILABLE:
        return []
    ensure_index()
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    try:
        collection = client.get_collection(name="travel_guides", embedding_function=emb_fn)
        if collection.count() == 0:
            return []
            
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, collection.count())
        )
        return results['documents'][0] if results['documents'] else []
    except ValueError:
        return []

def rag_ask(question: str) -> str:
    """Answers a question using only context from searched travel guides."""
    if not RAG_AVAILABLE:
        return "RAG dependencies not installed. Please install them to use this feature."
        
    print("Searching guides...")
    chunks = search_guides(question, n_results=3)
    if not chunks:
        return "No guides found or index is empty. Please add guides and rebuild the index."
        
    context = "\n\n---\n\n".join(chunks)
    system_prompt = f"""You are a helpful travel assistant. 
Answer the user's question using ONLY the provided context from travel guides. 
If the answer is not in the context, say 'I cannot answer this based on the provided guides.'

Context:
{context}"""
    
    print("Analyzing context...")
    return ask(question, system_prompt=system_prompt)

# --- Menu Logic ---

def main():
    collection = load_trips()
    
    while True:
        print("\n=== Trip Notes (AI Powered) ===")
        print("--- Management ---")
        print("[1] Add destination")
        print("[2] View all destinations")
        print("[3] Search by country")
        print("[4] Add note to a destination")
        print("[5] Mark visited / Rate / Stats")
        
        print("\n--- AI Features ---")
        print("[6] Ask AI (General Travel Assistant)")
        print("[7] Generate Trip Briefing")
        print("[8] Search my guides (RAG)")
        print("[R] Rebuild search index")
        
        print("\n[Q] Quit")
        
        choice = input("Select an option: ").strip().upper()
        
        if choice == "1":
            name = input("Enter destination name: ")
            country = input("Enter country: ")
            try:
                budget = float(input("Enter budget: "))
                dest = Destination(name, country, budget)
                collection.add(dest)
                save_trips(collection)
                print("Destination added!")
            except ValueError:
                print("Invalid budget. Please enter a number.")
            
        elif choice == "2":
            trips = collection.get_all()
            if not trips:
                print("No trips saved yet.")
            else:
                for i, trip in enumerate(trips, 1):
                    status = "Visited" if trip.visited else "Wishlist"
                    rating = f"{trip.rating}/5" if trip.rating > 0 else "unrated"
                    print(f"{i}. {trip.name} ({trip.country}) - ${trip.budget:.2f} [{status}] ({rating})")
                    if trip.notes:
                        print(f"   Notes: {trip.notes}")
        
        elif choice == "3":
            country = input("Enter country to search: ")
            results = collection.search_by_country(country)
            if not results:
                print(f"No trips found for {country}.")
            for trip in results:
                print(f"- {trip.name} ({trip.country})")
        
        elif choice == "4":
            trips = collection.get_all()
            if not trips:
                print("No trips available.")
                continue
            for i, trip in enumerate(trips, 1):
                print(f"{i}. {trip.name}")
            try:
                n = int(input("Select trip number: "))
                trip = collection.get_by_index(n - 1)
                note = input("Enter note: ")
                trip.add_note(note)
                save_trips(collection)
                print("Note added!")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == "5":
            print("\n[V] Mark Visited  [R] Rate Trip  [S] View Stats  [B] Back")
            sub_choice = input("Select sub-option: ").strip().upper()
            
            if sub_choice == "V":
                trips = collection.get_all()
                for i, trip in enumerate(trips, 1):
                    print(f"{i}. {trip.name}")
                try:
                    n = int(input("Select trip number: "))
                    collection.mark_visited(n - 1)
                    save_trips(collection)
                    print("Marked as visited!")
                except (ValueError, IndexError):
                    print("Invalid selection.")
            elif sub_choice == "R":
                trips = collection.get_all()
                for i, trip in enumerate(trips, 1):
                    print(f"{i}. {trip.name}")
                try:
                    n = int(input("Select trip number: "))
                    r = int(input("Enter rating (1-5): "))
                    collection.rate(n - 1, r)
                    save_trips(collection)
                    print("Rated!")
                except (ValueError, IndexError):
                    print("Invalid selection.")
            elif sub_choice == "S":
                top = collection.top_rated(3)
                print("\nTop 3 Rated Trips:")
                for trip in top:
                    print(f"- {trip.name}: {trip.rating}/5")
        
        elif choice == "6":
            question = input("Ask the General Travel AI: ")
            print("\nThinking...")
            answer = ask(question)
            print(f"\nAI Response:\n{answer}")

        elif choice == "7":
            trips = collection.get_all()
            if not trips:
                print("No trips saved yet.")
                continue
            for i, trip in enumerate(trips, 1):
                print(f"{i}. {trip.name}")
            try:
                n = int(input("Select trip number for briefing: "))
                trip = collection.get_by_index(n - 1)
                print(f"\nGenerating personalized briefing for {trip.name}...")
                briefing = generate_trip_briefing(trip.name, trip.country, trip.notes)
                print(f"\n{briefing}")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == "8":
            question = input("Ask a question about your guides: ")
            answer = rag_ask(question)
            print(f"\nGuide AI Response:\n{answer}")
            
        elif choice == "R":
            print("\nRebuilding index...")
            build_index(force=True)

        elif choice == "Q":
            print("Safe travels! Goodbye.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

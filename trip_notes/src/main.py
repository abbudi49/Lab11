import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.storage import load_trips, save_trips

def main():
    collection = load_trips()
    
    while True:
        print("\n=== Trip Notes ===")
        print("[1] Add destination")
        print("[2] View all destinations")
        print("[3] Search by country")
        print("[4] Add note to a destination")
        print("[5] Mark as Visited")
        print("[6] Wishlist / Visited")
        print("[7] Rate a Trip")
        
        print("\n--- AI Assistant ---")
        print("[8] Search my guides (RAG)")
        print("[9] Ask general travel AI")
        print("[10] AI Travel Agent (ReAct)")
        print("[11] Generate trip briefing")
        print("[R] Rebuild search index")
        print("[Q] Quit")
        
        choice = input("Select an option: ").upper()
        
        if choice == "1":
            name = input("Enter destination name: ")
            country = input("Enter country: ")
            budget = float(input("Enter budget: "))
            
            dest = Destination(name, country, budget)
            collection.add(dest)
            save_trips(collection)
            print("Destination added!")
            
        elif choice == "2":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                for i, trip in enumerate(collection.get_all(), 1):
                    status = "Visited" if trip.visited else "Wishlist"
                    rating = f"Rating: {trip.rating}/5" if trip.rating > 0 else "unrated"
                    print(f"{i}. {trip.name} ({trip.country}) - ${trip.budget:.2f} [{status}] ({rating})")
                    if trip.notes:
                        print(f"   Notes: {trip.notes}")
        
        elif choice == "3":
            country = input("Enter country: ")
            results = collection.search_by_country(country)
            for trip in results:
                status = "Visited" if trip.visited else "Wishlist"
                rating = f"Rating: {trip.rating}/5" if trip.rating > 0 else "unrated"
                print(f"{trip.name} ({trip.country}) - ${trip.budget:.2f} [{status}] ({rating})")
                if trip.notes:
                    print(f"   Notes: {trip.notes}")
        
        elif choice == "4":
            for i, trip in enumerate(collection.get_all(), 1):
                print(f"{i}. {trip.name}")
            
            n = int(input("Select number: "))
            trip = collection.get_by_index(n - 1)
            note = input("Enter note: ")
            trip.add_note(note)
            save_trips(collection)
            print("Note added!")
                
        elif choice == "Q":
            print("Goodbye!")
            break

        elif choice == "5":
            trips = collection.get_all()
            for i, trip in enumerate(trips, 1):
                print(f"{i}. {trip.name}")
            
            n = int(input("Select number: "))
            collection.mark_visited(n - 1)
            name = collection.get_by_index(n - 1).name
            save_trips(collection)
            print(f"Marked {name} as visited!")

        elif choice == "6":
            wishlist = collection.get_wishlist()
            visited = collection.get_visited()
            
            print(f"\nWishlist ({len(wishlist)}):")
            for trip in wishlist:
                print(f"- {trip.name} ({trip.country})")
                
            print(f"\nVisited ({len(visited)}):")
            for trip in visited:
                print(f"- {trip.name} ({trip.country})")

        elif choice == "7":
            trips = collection.get_all()
            for i, trip in enumerate(trips, 1):
                rating = f"{trip.rating}/5" if trip.rating > 0 else "unrated"
                print(f"{i}. {trip.name} ({rating})")
            
            n = int(input("Select number: "))
            r = int(input("Enter rating (1-5): "))
            collection.rate(n - 1, r)
            save_trips(collection)
            print(f"Rated {trips[n-1].name} as {r}/5!")

        elif choice == "8":
            try:
                from src.ai_assistant import rag_ask
            except Exception:
                print("RAG support not available.")
                continue
            q = input("Enter question to search your guides: ")
            ans = rag_ask(q)
            print("\n=== Answer from guides ===")
            print(ans)

        elif choice == "9":
            try:
                from src.ai_assistant import ask
            except Exception:
                print("AI support not available.")
                continue
            q = input("Enter travel question: ")
            ans = ask(q)
            print("\n=== AI Response ===")
            print(ans)
            
            save = input("\nSave this as a note to a trip? (y/n): ")
            if save.lower() == "y":
                for i, trip in enumerate(collection.get_all(), 1):
                    print(f"{i}. {trip.name}")
                n = int(input("Select trip number: "))
                trip = collection.get_by_index(n - 1)
                trip.add_note(f"AI: {ans}")
                save_trips(collection)
                print("Note saved!")

        elif choice == "10":
            try:
                from src.tools import run_agent
            except Exception as e:
                print(f"Agent support not available: {e}")
                continue
            q = input("Enter question for the AI Travel Agent: ")
            print("\nThinking...")
            ans = run_agent(q)
            print("\n=== Agent Response ===")
            print(ans)

        elif choice == "11":
            try:
                from src.ai_assistant import generate_trip_briefing
            except Exception:
                print("AI support not available.")
                continue
            
            trips = collection.get_all()
            if not trips:
                print("No trips saved.")
                continue
                
            for i, trip in enumerate(trips, 1):
                print(f"{i}. {trip.name}")
            
            n = int(input("Select number for briefing: "))
            trip = collection.get_by_index(n - 1)
            print(f"\nGenerating briefing for {trip.name}...")
            briefing = generate_trip_briefing(trip.name, trip.country, trip.notes)
            print("\n" + briefing)

        elif choice == "R":
            try:
                from src.rag import build_index
                build_index(force=True)
                print("Search index rebuilt.")
            except Exception as e:
                print(f"Failed to rebuild index: {e}")
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()

import sys
import os

# Allow importing from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import run_agent

def main():
    print("=== AI Travel Agent Test ===")
    print("Type 'quit' to exit.")
    
    while True:
        prompt = input("\nAsk the agent a question: ")
        if prompt.lower() in ["quit", "exit", "q"]:
            break
            
        print("\nThinking...")
        answer = run_agent(prompt)
        print(f"\nFinal Answer:\n{answer}")

if __name__ == "__main__":
    main()

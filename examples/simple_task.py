import sys
import os

# Add src to path for running the example directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import ailib

def main():
    print("--- Starting AI-enabled script ---")
    
    name = ailib.ask("What is your name?")
    print(f"Hello, {name}!")
    
    feeling = ailib.ask(f"How do you think {name} is feeling today?", context={"name": name})
    print(f"AI thinks: {feeling}")
    
    action = ailib.decide(
        "What should we do next?", 
        options=["stop", "continue", "tell a joke"]
    )
    
    if action == "tell a joke":
        joke = ailib.ask("Tell a short joke.")
        print(f"Joke: {joke}")
    elif action == "stop":
        print("Shutting down.")
    else:
        print("Continuing execution...")

if __name__ == "__main__":
    main()

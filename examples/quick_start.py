"""Quick start example for ConnectOnion - minimal setup."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectonion import Agent


# Step 1: Define your tools (just regular functions!)
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': Found relevant information about {query}."

def calculate(expression: str) -> float:
    """Do math calculations."""
    try:
        # Safe evaluation for demo purposes
        allowed_chars = "0123456789+-*/(). "
        if all(c in allowed_chars for c in expression):
            return eval(expression)
        else:
            raise ValueError("Invalid characters in expression")
    except Exception as e:
        raise Exception(f"Math error: {str(e)}")

def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    print("🚀 ConnectOnion Quick Start")
    print("=" * 40)
    
    # Step 2: Create agent with your functions and define its role
    agent = Agent(
        name="my_assistant",
        system_prompt="You are a friendly and helpful assistant. Be concise but warm in your responses.",
        tools=[search, calculate, get_time]
    )
    
    print(f"✅ Agent created with tools: {agent.list_tools()}")
    
    # Step 3: Use it!
    print("\n📝 Examples:")
    
    # Simple conversation
    result = agent.run("Hello! What can you help me with?")
    print(f"\n1. Greeting: {result}")
    
    # Math calculation
    result = agent.run("What is 42 * 17?")
    print(f"\n2. Math: {result}")
    
    # Multiple tools in one request
    result = agent.run("Search for AI news and tell me what time it is")
    print(f"\n3. Multiple tools: {result}")
    
    # Step 4: Check history (automatic!)
    print(f"\n📊 Completed {len(agent.history.records)} tasks")
    print(f"📂 History saved to: {agent.history.history_file}")
    
    print("\n✨ That's it! Just define functions and pass them to Agent!")


if __name__ == "__main__":
    main()
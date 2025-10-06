# Tutorial: Building Your First AI Agent in Python with ConnectOnion

A complete step-by-step guide to creating AI agents in Python. Learn how to build an intelligent assistant that can search, calculate, and answer questions using tools.

## What You'll Learn

By the end of this tutorial, you'll know how to:
- Create agents with custom tools
- Define tools that agents can use
- Handle agent responses and errors
- Add system prompts for behavior control
- Use different LLM models (OpenAI, Anthropic, etc.)
- Debug and troubleshoot your agents

**Time**: 15-20 minutes
**Level**: Beginner
**Prerequisites**: Python 3.9+, basic Python knowledge

## Project Overview

We'll build a "Research Assistant" agent that can:
1. Search for information
2. Perform calculations
3. Get current time/date
4. Remember context across multiple interactions

## Step 1: Installation and Setup

### Install Connect Onion

```bash
pip install connectonion
```

### Set Up Your API Key

Create a `.env` file in your project directory:

```env
# .env
OPENAI_API_KEY=sk-your-key-here
```

ConnectOnion auto-loads `.env` files, so you don't need to manually load them!

### Create Project Structure

```bash
mkdir research-agent
cd research-agent
touch agent.py
touch .env
```

## Step 2: Create Your First Tool

Tools are just regular Python functions! The agent uses them to perform actions.

Create `agent.py`:

```python
from connectonion import Agent

def search(query: str) -> str:
    """
    Search for information on a topic.

    Args:
        query: The search query

    Returns:
        Search results as a string
    """
    # In production, call a real search API
    # For now, we'll simulate results
    return f"Search results for '{query}':\n- Result 1\n- Result 2\n- Result 3"

# Create agent with the search tool
agent = Agent(
    name="research-assistant",
    tools=[search]
)

# Test it
agent.input("Search for information about Python")
```

**Run it:**
```bash
python agent.py
```

**Output:**
```
14:32:10 INPUT: Search for information about Python
14:32:11 → Tool: search({'query': 'Python programming'})
14:32:11 ← Result (125ms): Search results for 'Python programming':...
14:32:12 OUTPUT: Here's what I found about Python: [summary of results]
```

### How It Works

1. **Docstring = Tool Description**: The agent uses your docstring to understand what the tool does
2. **Type Hints = Parameters**: `query: str` tells the agent what parameters to pass
3. **Return Value = Result**: Whatever you return becomes the tool's result

## Step 3: Add More Tools

Let's make our agent more useful by adding calculation and time tools:

```python
from connectonion import Agent
import datetime

def search(query: str) -> str:
    """Search for information on a topic"""
    return f"Search results for '{query}':\n- Information 1\n- Information 2"

def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression: Math expression like "25 * 4" or "100 / 5"

    Returns:
        The calculation result
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

def get_current_time() -> str:
    """Get the current date and time"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Create agent with multiple tools
agent = Agent(
    name="research-assistant",
    tools=[search, calculate, get_current_time]
)

# Test with a complex query
agent.input("What time is it? Also calculate 156 * 23")
```

The agent will automatically use both tools to answer!

## Step 4: Add a System Prompt

Control your agent's behavior with a system prompt:

```python
agent = Agent(
    name="research-assistant",
    tools=[search, calculate, get_current_time],
    system_prompt="""You are a helpful research assistant.

    Your role:
    - Search for accurate information when asked
    - Perform calculations when needed
    - Provide clear, concise answers
    - Always cite your sources

    Be professional but friendly."""
)

agent.input("Find information about AI and calculate the year it was founded plus 50")
```

The agent will now follow your guidelines!

## Step 5: Handle Multi-Turn Conversations

Agents maintain conversation context automatically:

```python
from connectonion import Agent

def search(query: str) -> str:
    """Search for information"""
    return f"Found information about: {query}"

agent = Agent(
    name="assistant",
    tools=[search]
)

# First interaction
agent.input("Search for information about Paris")

# Follow-up (agent remembers context!)
agent.input("What's the population?")

# Another follow-up
agent.input("And the famous landmarks?")
```

Each `agent.input()` remembers previous context, so the agent knows "the population" refers to Paris!

## Step 6: Use Different Models

ConnectOnion supports multiple LLM providers:

### OpenAI Models

```python
# Default (gpt-4o-mini)
agent = Agent("assistant", tools=[search])

# GPT-4
agent = Agent(
    "assistant",
    tools=[search],
    model="gpt-4o"
)
```

### Anthropic Claude

```python
# Set up Anthropic key in .env
# ANTHROPIC_API_KEY=sk-ant-...

agent = Agent(
    "assistant",
    tools=[search],
    model="claude-3-5-sonnet-20241022"
)
```

### Google Gemini

```python
# Set up Google key in .env
# GOOGLE_API_KEY=...

agent = Agent(
    "assistant",
    tools=[search],
    model="gemini-2.0-flash-exp"
)
```

## Step 7: Add Error Handling

Make your agent robust:

```python
from connectonion import Agent

def search(query: str) -> str:
    """Search for information"""
    if not query or len(query) < 2:
        return "Error: Query too short. Please provide a longer search term."

    try:
        # Your search logic here
        results = perform_search(query)
        return results
    except Exception as e:
        return f"Search failed: {str(e)}. Please try a different query."

def calculate(expression: str) -> str:
    """Calculate a math expression"""
    try:
        # Validate expression first
        if any(char in expression for char in ['import', 'exec', 'eval']):
            return "Error: Invalid expression"

        result = eval(expression)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Calculation error: {str(e)}"

agent = Agent(
    "assistant",
    tools=[search, calculate]
)
```

Tools return error messages as strings - the agent will see them and can adapt!

## Step 8: Debug Your Agent

Enable interactive debugging to see what's happening:

```python
agent = Agent(
    "assistant",
    tools=[search, calculate]
)

# Enable debugging
agent.auto_debug()

# Now run a task
agent.input("Search for Python and calculate 25 * 4")
```

When a tool is called, you'll get an interactive menu:

```
@xray BREAKPOINT: search

What do you want to do?
  → Continue execution       [Enter or c]
    Ask AI for help          [a]
    Edit variables (Python)  [e]
    View execution trace     [v]
>
```

Learn more: [Interactive Debugging Guide](Interactive-Debugging-Guide)

## Complete Example

Here's a full, production-ready research assistant:

```python
from connectonion import Agent
import datetime
import requests

def search_web(query: str) -> str:
    """
    Search the web for information.

    Args:
        query: Search query

    Returns:
        Search results
    """
    # Replace with real search API (e.g., SerpAPI, Google Custom Search)
    try:
        # Simulated for example
        return f"Web results for '{query}':\n1. First result\n2. Second result"
    except Exception as e:
        return f"Search failed: {str(e)}"

def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression: Math expression (e.g., "25 * 4")

    Returns:
        Calculation result
    """
    try:
        # Security: validate expression
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"

        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_time() -> str:
    """Get the current date and time"""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y at %H:%M:%S")

def get_weather(city: str) -> str:
    """
    Get weather for a city.

    Args:
        city: City name

    Returns:
        Weather information
    """
    # Replace with real weather API (e.g., OpenWeatherMap)
    return f"Weather in {city}: 72°F, Sunny (simulated data)"

# Create the agent
agent = Agent(
    name="research-assistant",
    tools=[search_web, calculate, get_current_time, get_weather],
    system_prompt="""You are a helpful research assistant named ResearchBot.

    Your capabilities:
    - Search the web for information
    - Perform calculations
    - Provide current time/date
    - Check weather for cities

    Your style:
    - Provide clear, concise answers
    - Cite sources when searching
    - Break down complex calculations
    - Be friendly and professional

    Always verify information before presenting it.""",
    model="gpt-4o-mini"  # Fast and cost-effective
)

# Example usage
if __name__ == "__main__":
    # Single query
    agent.input("What's the weather in Tokyo and what time is it there?")

    # Follow-up conversation
    agent.input("Search for Python tutorials")
    agent.input("Calculate how many hours in a week")
    agent.input("What's 25% of 840?")
```

## Next Steps

**Master Debugging:**
- [Interactive Debugging Guide](Interactive-Debugging-Guide) - Learn `auto_debug()`
- [Debug Agent Errors](../How-To/Debug-Agent-Errors) - Troubleshoot issues

**Build More:**
- [Creating Custom Tools](Creating-Custom-Tools) - Advanced tool patterns
- [Email Agent Example](../Examples/Email-Agent-Example) - Real-world example
- [Web Scraping Agent](../Examples/Web-Scraping-Agent) - Data extraction

**Deploy:**
- [Deploy to Production](../How-To/Deploy-To-Production) - Production best practices

## Common Patterns

### Pattern: Tool Chaining
Agent uses multiple tools in sequence:

```python
# Agent will:
# 1. Call search() for information
# 2. Call calculate() to process numbers
# 3. Combine results in answer
agent.input("Find Python's release year and add 30 to it")
```

### Pattern: Conditional Tools
Agent decides which tool based on context:

```python
agent.input("What time is it?")        # Uses get_current_time()
agent.input("What's 25 * 4?")          # Uses calculate()
agent.input("Search for Python docs")  # Uses search_web()
```

### Pattern: Error Recovery
Agent handles tool errors gracefully:

```python
# If search() returns an error, agent will:
# 1. See the error message
# 2. Try a different approach
# 3. Or ask user for clarification
agent.input("Search for 'x'")  # Too short - agent sees error
```

## Troubleshooting

**Issue: Agent doesn't call tools**
- ✓ Check tool has clear docstring
- ✓ Use descriptive function names
- ✓ Add type hints to parameters

**Issue: Tool called with wrong arguments**
- ✓ Add docstring with Args section
- ✓ Use clear parameter names
- ✓ Provide examples in docstring

**Issue: Agent gives wrong answers**
- ✓ Improve system prompt with examples
- ✓ Make tool return more detailed information
- ✓ Try a better model (gpt-4 vs gpt-3.5)

More help: [Troubleshooting Guide](../Troubleshooting)

## Resources

- [Official Documentation](https://docs.connectonion.com)
- [GitHub Repository](https://github.com/wu-changxing/connectonion)
- [Discord Community](https://discord.gg/4xfD9k8AUF)

---

**Next Tutorial:** [Interactive Debugging Guide](Interactive-Debugging-Guide) - Learn to debug agents with `auto_debug()`

# Quick Start: Build Your First AI Agent in Python (5 Minutes)

Learn how to create a Python AI agent with ConnectOnion in under 5 minutes. This tutorial will guide you through installation, setup, and running your first AI-powered agent.

## What You'll Build

A simple AI agent that can search for information and answer questions using tools. By the end, you'll understand:
- How to install ConnectOnion
- How to create an AI agent in 2 lines of code
- How to add tools (functions) to your agent
- How to run tasks and see results

## Prerequisites

- Python 3.9 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Step 1: Install ConnectOnion

```bash
pip install connectonion
```

That's it! ConnectOnion is now installed.

## Step 2: Set Up Your API Key

Create a `.env` file in your project directory:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
```

Or set it as an environment variable:

```bash
export OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Create Your First Agent

Create a new file called `agent.py`:

```python
from connectonion import Agent

# Define a tool (just a regular Python function)
def search(query: str) -> str:
    """Search for information and return results"""
    # Simulate a search - replace with real API in production
    return f"Found information about: {query}"

# Create an agent with the tool
agent = Agent(
    name="assistant",
    tools=[search]
)

# Give it a task
agent.input("What is the capital of France?")
```

## Step 4: Run Your Agent

```bash
python agent.py
```

You'll see output like this:

```
14:32:10 INPUT: What is the capital of France?
14:32:11 → Tool: search({'query': 'capital of France'})
14:32:11 ← Result (340ms): Found information about: capital of France
14:32:12 OUTPUT: The capital of France is Paris.
```

**Congratulations!** You just built your first AI agent! 🎉

## How It Works

1. **Tools are functions** - Any Python function becomes a tool the agent can use
2. **Agent decides when to use tools** - The LLM determines if/when to call `search()`
3. **Automatic execution** - ConnectOnion handles tool calling and result processing

## Step 5: Add More Tools

Let's make the agent more powerful:

```python
from connectonion import Agent
import datetime

def search(query: str) -> str:
    """Search for information"""
    return f"Found: {query}"

def get_time() -> str:
    """Get the current time"""
    return datetime.datetime.now().strftime("%H:%M:%S")

def calculate(expression: str) -> str:
    """Calculate a math expression"""
    try:
        result = eval(expression)  # Use carefully in production!
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Agent with multiple tools
agent = Agent(
    name="assistant",
    tools=[search, get_time, calculate]
)

# The agent will choose which tool(s) to use
agent.input("What time is it and what's 25 * 4?")
```

The agent will intelligently use both `get_time()` and `calculate()` to answer!

## Step 6: Debug Your Agent (Optional)

Want to see what's happening inside? Enable interactive debugging:

```python
agent = Agent(
    name="assistant",
    tools=[search]
)

# Enable debugging
agent.auto_debug()

# Now when you run a task, you can inspect and control execution
agent.input("Search for Python tutorials")
```

When debugging is on, the agent will pause at tool calls and let you:
- Continue execution
- Ask AI for help
- Edit variables with Python
- View execution trace

Learn more in the [Interactive Debugging Guide](Tutorials/Interactive-Debugging-Guide).

## Common Patterns

### Pattern 1: Simple Question Answering

```python
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Weather in {city}: 72°F, Sunny"

agent = Agent("weather-bot", tools=[get_weather])
agent.input("What's the weather in Tokyo?")
```

### Pattern 2: Multi-Step Tasks

```python
def search(query: str) -> str:
    """Search for information"""
    return f"Results for: {query}"

def summarize(text: str) -> str:
    """Summarize text"""
    return f"Summary: {text[:100]}..."

agent = Agent("researcher", tools=[search, summarize])
agent.input("Find information about AI agents and summarize it")
```

The agent will:
1. Call `search()` to find information
2. Call `summarize()` on the results
3. Return a concise answer

### Pattern 3: Real-World Integration

```python
import requests

def fetch_api(url: str) -> str:
    """Fetch data from an API"""
    response = requests.get(url)
    return response.text

agent = Agent("api-bot", tools=[fetch_api])
agent.input("Get data from https://api.example.com/users")
```

## Next Steps

Now that you've built your first agent, explore more:

**Tutorials:**
- [Building Your First Agent](Tutorials/Building-Your-First-Agent) - Complete step-by-step guide
- [Creating Custom Tools](Tutorials/Creating-Custom-Tools) - Advanced tool patterns
- [Interactive Debugging](Tutorials/Interactive-Debugging-Guide) - Master `auto_debug()`

**Examples:**
- [Email Agent](Examples/Email-Agent-Example) - Search and send emails
- [Web Scraping Agent](Examples/Web-Scraping-Agent) - Extract data from websites

**Guides:**
- [Debug Agent Errors](How-To/Debug-Agent-Errors) - Fix common problems
- [Deploy to Production](How-To/Deploy-To-Production) - Production best practices

## Troubleshooting

**Problem: "No API key found"**
```
Solution: Set OPENAI_API_KEY in .env file or environment
```

**Problem: "Module not found: connectonion"**
```bash
Solution: pip install connectonion
```

**Problem: Agent doesn't call tools**
```
Solution: Make sure tools have clear docstrings describing what they do
```

More help: [Troubleshooting Guide](Troubleshooting) | [FAQ](FAQ)

## Resources

- **Official Docs**: [docs.connectonion.com](https://docs.connectonion.com)
- **GitHub**: [github.com/wu-changxing/connectonion](https://github.com/wu-changxing/connectonion)
- **Discord**: [Join community](https://discord.gg/4xfD9k8AUF)

---

**Ready for more?** → Continue to [Building Your First Agent Tutorial](Tutorials/Building-Your-First-Agent)

# Quick Start: Build Your First AI Agent in Python (2 Minutes)

Learn how to create a Python AI agent with ConnectOnion in under 2 minutes. This tutorial will guide you through installation and running your first AI-powered agent.

## What You'll Build

A ready-to-run AI agent with example tools. By the end, you'll understand:
- How to install ConnectOnion
- How to create a complete agent project instantly
- How to run your agent
- How to customize it with your own tools

## Prerequisites

- Python 3.9 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Step 1: Install ConnectOnion

```bash
pip install connectonion
```

That's it! ConnectOnion is now installed.

## Step 2: Create Your Agent Project

```bash
co create my-agent
```

The CLI will:
- Guide you through API key setup (automated!)
- Create a complete project with example code
- Set up configuration files

## Step 3: Run Your Agent

```bash
cd my-agent
python agent.py
```

You'll see output showing your agent in action! 🎉

**Congratulations!** You just created and ran your first AI agent!

## How It Works

The generated `agent.py` includes:
1. **Example tools** - Functions that the agent can use
2. **Agent configuration** - Pre-configured with your API key
3. **Ready-to-run code** - Just execute and start building

## Step 4: Customize Your Agent

Open `agent.py` in your editor and add more tools to make your agent more powerful:

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

The agent will intelligently use multiple tools to answer complex questions!

## Step 5: Use Different Templates (Optional)

ConnectOnion includes templates for specialized use cases:

```bash
# Web automation with Playwright
co create my-browser-bot --template playwright
cd my-browser-bot
```

This creates an agent with browser automation tools for web scraping, form filling, and more!

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

Learn more in the [Interactive Debugging Guide](Tutorials-Interactive-Debugging-Guide).

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
- [Building Your First Agent](Tutorials-Building-Your-First-Agent) - Complete step-by-step guide
- [Creating Custom Tools](Tutorials-Creating-Custom-Tools) - Advanced tool patterns
- [Interactive Debugging](Tutorials-Interactive-Debugging-Guide) - Master `auto_debug()`

**Examples:**
- [Email Agent](Examples-Email-Agent-Example) - Search and send emails
- [Web Scraping Agent](Examples-Web-Scraping-Agent) - Extract data from websites

**Guides:**
- [Debug Agent Errors](How-To-Debug-Agent-Errors) - Fix common problems
- [Deploy to Production](How-To-Deploy-To-Production) - Production best practices

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
- **GitHub**: [github.com/openonion/connectonion](https://github.com/openonion/connectonion)
- **Discord**: [Join community](https://discord.gg/4xfD9k8AUF)

---

**Ready for more?** → Continue to [Building Your First Agent Tutorial](Tutorials-Building-Your-First-Agent)

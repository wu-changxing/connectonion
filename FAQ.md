# Frequently Asked Questions (FAQ)

Common questions about ConnectOnion and AI agents. Can't find your question? Ask in our [Discord community](https://discord.gg/4xfD9k8AUF).

## General Questions

### What is ConnectOnion?

ConnectOnion is a Python framework for building AI agents that can use tools, make decisions, and complete tasks. It makes it easy to create agents that interact with APIs, databases, files, and more.

**Key features:**
- Simple 2-line agent creation
- Functions automatically become tools
- Interactive debugging with `auto_debug()`
- Built-in behavior tracking
- Multi-model support (OpenAI, Anthropic, Google)

### Is ConnectOnion free?

Yes! ConnectOnion is open source and free to use. However, you'll need API keys from LLM providers (OpenAI, Anthropic, etc.) which have their own pricing.

**Cost breakdown:**
- ConnectOnion framework: **Free**
- OpenAI API: Pay per token ([pricing](https://openai.com/pricing))
- Anthropic API: Pay per token ([pricing](https://www.anthropic.com/pricing))
- Google Gemini: Has free tier ([pricing](https://ai.google.dev/pricing))

### How is ConnectOnion different from LangChain?

**ConnectOnion:**
- Simpler API - create agents in 2 lines
- Built-in interactive debugging
- Focus on simplicity over features
- Smaller, easier to understand codebase

**LangChain:**
- More features and integrations
- Larger ecosystem
- Steeper learning curve
- More complex abstractions

**Use ConnectOnion if:** You want simplicity and fast development
**Use LangChain if:** You need extensive pre-built integrations

### What Python version do I need?

**Python 3.9 or higher** is required.

Check your version:
```bash
python --version
```

Upgrade if needed:
```bash
# Mac/Linux
brew install python@3.9

# Windows
# Download from python.org
```

### Can I use ConnectOnion for commercial projects?

Yes! ConnectOnion is MIT licensed - use it for anything, including commercial projects.

## Getting Started

### How do I install ConnectOnion?

```bash
pip install connectonion
```

That's it! See the [Quick Start Guide](Quick-Start) for next steps.

### Do I need an OpenAI API key?

Yes, you need an API key from a supported LLM provider:
- **OpenAI** (recommended for beginners)
- **Anthropic** (Claude models)
- **Google** (Gemini models)

Get an OpenAI key: https://platform.openai.com/api-keys

### How do I set up my API key?

**Option 1: `.env` file (recommended)**
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**Option 2: Environment variable**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

See [Quick Start Guide](Quick-Start) for details.

### What's the simplest possible agent?

```python
from connectonion import Agent

agent = Agent("assistant")
agent.input("Hello!")
```

That's it! This creates an agent and gives it a task.

## Agent Basics

### How do I give my agent tools?

Just pass Python functions to the `tools` parameter:

```python
def search(query: str) -> str:
    """Search for information"""
    return f"Results for: {query}"

agent = Agent("assistant", tools=[search])
```

The agent will automatically know when to use `search()`.

### Why isn't my agent calling my tool?

Common reasons:

**1. Missing docstring:**
```python
# ✗ Agent doesn't know what this does
def my_tool(param):
    return result

# ✓ Clear docstring
def my_tool(param: str) -> str:
    """Description of what this tool does"""
    return result
```

**2. Unclear tool name:**
```python
# ✗ Unclear
def process(data):
    pass

# ✓ Descriptive
def search_customer_database(name: str):
    pass
```

**3. System prompt conflicts:**
```python
# ✗ Discourages tool use
system_prompt="Answer directly without tools"

# ✓ Encourages tool use
system_prompt="Use tools when helpful"
```

See [Debug Agent Errors](How-To/Debug-Agent-Errors) for more solutions.

### Can I use multiple tools?

Yes! Pass a list of functions:

```python
agent = Agent(
    "assistant",
    tools=[search, calculate, send_email, get_weather]
)
```

The agent will choose which tool(s) to use based on the task.

### How do I control agent behavior?

Use the `system_prompt` parameter:

```python
agent = Agent(
    "assistant",
    tools=[...],
    system_prompt="""You are a helpful assistant.

Rules:
- Always verify information before presenting it
- Use search tool for current information
- Be concise and accurate
"""
)
```

### Can agents remember previous conversations?

Yes! Agents maintain conversation history automatically:

```python
agent.input("What's the capital of France?")
# Agent: "Paris"

agent.input("What's the population?")
# Agent knows "it" refers to Paris
```

To start fresh:
```python
agent = Agent("assistant")  # New agent, no history
```

## Debugging

### How do I debug my agent?

Use `auto_debug()`:

```python
from connectonion.decorators import xray

@xray  # Mark tool as breakpoint
def my_tool():
    pass

agent = Agent("assistant", tools=[my_tool])
agent.auto_debug()  # Enable debugging

agent.input("Task")
# Agent pauses at my_tool(), lets you inspect and modify
```

See [Interactive Debugging Guide](Tutorials/Interactive-Debugging-Guide).

### What is the `@xray` decorator?

`@xray` marks tools as debugging breakpoints:

```python
from connectonion.decorators import xray

@xray  # Agent pauses here when auto_debug() is on
def critical_operation():
    pass

# Regular tool - doesn't pause
def simple_operation():
    pass
```

### Can I debug without stopping execution?

Yes! Keep `@xray` but don't call `auto_debug()`:

```python
@xray  # Enhanced logging, no pausing
def my_tool():
    pass

agent = Agent("assistant", tools=[my_tool])
# No auto_debug() call - tool runs with enhanced logging only
```

### How do I see what the agent is thinking?

Enable console output (on by default):

```python
agent = Agent("assistant", tools=[...])
agent.input("Task")

# Output shows:
# - Tool calls
# - Parameters
# - Results
# - Agent's responses
```

Or use `auto_debug()` for full control.

## Models and Performance

### Which model should I use?

**For development/testing:**
```python
model="gpt-4o-mini"  # Fast, cheap, good enough
```

**For production (quality matters):**
```python
model="gpt-4o"  # More accurate, slower, expensive
```

**For complex reasoning:**
```python
model="o1-preview"  # Best reasoning, most expensive
```

### How much does it cost to run an agent?

Depends on the model and usage. Example (rough estimates):

**gpt-4o-mini** (recommended for most use cases):
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens
- Typical task: $0.001 - $0.01

**gpt-4o** (for better quality):
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens
- Typical task: $0.01 - $0.10

Track usage at: https://platform.openai.com/usage

### How can I reduce costs?

1. **Use cheaper models:**
   ```python
   model="gpt-4o-mini"  # 60x cheaper than gpt-4
   ```

2. **Shorter system prompts:**
   ```python
   # ✗ Long (expensive)
   system_prompt="[500 words of instructions]"

   # ✓ Concise (cheap)
   system_prompt="Be helpful and use tools when needed."
   ```

3. **Cache results:**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def expensive_search(query: str):
       return results
   ```

4. **Limit conversation history:**
   ```python
   # Start new agent instead of long conversation
   agent = Agent("assistant")
   ```

### Can I use Claude or Gemini instead of GPT?

Yes! ConnectOnion supports multiple providers:

**Anthropic Claude:**
```python
# Set ANTHROPIC_API_KEY in .env
agent = Agent("assistant", model="claude-3-5-sonnet-20241022")
```

**Google Gemini:**
```python
# Set GOOGLE_API_KEY in .env
agent = Agent("assistant", model="gemini-2.0-flash-exp")
```

### Why is my agent slow?

Common causes:

1. **Using slow model:**
   ```python
   # Slow
   model="gpt-4o"

   # Fast
   model="gpt-4o-mini"
   ```

2. **Slow tools:**
   ```python
   # Add caching or optimize
   @lru_cache(maxsize=100)
   def slow_tool():
       pass
   ```

3. **Long system prompts:**
   Shorter prompts = faster responses

## Advanced Usage

### Can I build multi-agent systems?

Yes! Create multiple agents:

```python
researcher = Agent("researcher", tools=[search])
writer = Agent("writer", tools=[write_file])

# Researcher finds information
info = researcher.input("Research AI agents")

# Writer creates content from research
writer.input(f"Write an article about: {info}")
```

### Can agents call other agents?

Yes! Make an agent into a tool:

```python
researcher = Agent("researcher", tools=[search])

def research_tool(topic: str) -> str:
    """Research a topic using the research agent"""
    return researcher.input(f"Research {topic}")

writer = Agent("writer", tools=[research_tool, write_file])
```

### How do I save agent state?

Agent state is in `agent.current_session`:

```python
import json

# Save state
state = agent.current_session
with open('agent_state.json', 'w') as f:
    json.dump(state, f)

# Load state (note: you need to recreate the agent)
with open('agent_state.json', 'r') as f:
    state = json.load(f)
agent.current_session = state
```

### Can I use local models?

Not directly yet, but you can use OpenAI-compatible APIs:

```python
# Example with local model via OpenAI-compatible server
import openai
openai.api_base = "http://localhost:8000/v1"

agent = Agent("assistant", model="local-model")
```

## Deployment

### Can I deploy agents to production?

Yes! See the [Deploy to Production Guide](How-To/Deploy-To-Production).

**Quick tips:**
- Remove `auto_debug()` calls
- Use environment variables for secrets
- Add error handling
- Implement logging
- Set rate limits

### How do I deploy to Heroku/AWS/Docker?

See specific examples in [Deploy to Production](How-To/Deploy-To-Production).

### Should I keep `@xray` in production?

Optional. `@xray` without `auto_debug()` just adds enhanced logging (minimal overhead).

**Keep it if:** You want detailed logs
**Remove it if:** You want maximum performance

## Troubleshooting

### Where can I get help?

1. **Check guides:**
   - [Troubleshooting Guide](Troubleshooting)
   - [Debug Agent Errors](How-To/Debug-Agent-Errors)

2. **Community:**
   - [Discord Server](https://discord.gg/4xfD9k8AUF)
   - [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)

3. **Report bugs:**
   - [GitHub Issues](https://github.com/wu-changxing/connectonion/issues)

### My question isn't answered here

Ask in our [Discord community](https://discord.gg/4xfD9k8AUF) or [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)!

---

**More Resources:**
- [Quick Start Guide](Quick-Start)
- [Building Your First Agent](Tutorials/Building-Your-First-Agent)
- [Examples](Examples/Email-Agent-Example)
- [Official Documentation](https://docs.connectonion.com)

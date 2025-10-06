# How-To: Debug Common AI Agent Errors

Quick solutions to common errors when building and running AI agents with ConnectOnion. Find your error, get the fix.

## Table of Contents

- [API Key Errors](#api-key-errors)
- [Tool Calling Errors](#tool-calling-errors)
- [Agent Behavior Issues](#agent-behavior-issues)
- [Import and Installation Errors](#import-and-installation-errors)
- [Performance Issues](#performance-issues)

---

## API Key Errors

### Error: "No API key found"

**Full Error:**
```
Error: No OpenAI API key found. Set OPENAI_API_KEY environment variable.
```

**Cause:** Missing or incorrectly set API key

**Solutions:**

**1. Create `.env` file (Recommended):**
```bash
# Create .env in your project directory
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**2. Set environment variable:**
```bash
# Linux/Mac
export OPENAI_API_KEY=sk-your-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**3. Set in code (NOT recommended for production):**
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"
```

**Verify it works:**
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Should print your key
```

### Error: "Invalid API key"

**Full Error:**
```
AuthenticationError: Invalid API key provided
```

**Causes & Solutions:**

**1. Wrong API key format:**
```python
# ✗ Wrong
OPENAI_API_KEY=your-key-here  # Missing sk- prefix

# ✓ Correct
OPENAI_API_KEY=sk-proj-abc123...  # OpenAI project key
OPENAI_API_KEY=sk-abc123...       # OpenAI regular key
```

**2. Key from wrong provider:**
```python
# If using Anthropic:
ANTHROPIC_API_KEY=sk-ant-...  # NOT OPENAI_API_KEY

# If using Google:
GOOGLE_API_KEY=...  # NOT OPENAI_API_KEY
```

**3. Expired or revoked key:**
- Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
- Create a new key
- Update your `.env` file

### Error: "Rate limit exceeded"

**Full Error:**
```
RateLimitError: You exceeded your current quota
```

**Solutions:**

**1. You're out of credits:**
- Check [OpenAI Usage](https://platform.openai.com/usage)
- Add payment method and credits

**2. Too many requests:**
```python
import time

# Add delay between requests
agent.input("Task 1")
time.sleep(1)  # Wait 1 second
agent.input("Task 2")
```

**3. Use cheaper model:**
```python
# Instead of gpt-4
agent = Agent("assistant", model="gpt-4o-mini")  # Much cheaper
```

---

## Tool Calling Errors

### Error: Agent doesn't call any tools

**Symptom:** Agent responds but never uses your tools

**Causes & Solutions:**

**1. Missing or unclear docstring:**
```python
# ✗ Agent doesn't know what this does
def search(q):
    return results

# ✓ Clear description
def search(query: str) -> str:
    """
    Search the web for information.

    Use this when the user needs current information or facts.

    Args:
        query: What to search for

    Returns:
        Search results
    """
    return results
```

**2. Tool name too generic:**
```python
# ✗ Unclear what this does
def process(data):
    pass

# ✓ Descriptive name
def search_customer_database(customer_name: str):
    pass
```

**3. System prompt conflicts:**
```python
# ✗ Discourages tool use
system_prompt="Answer all questions directly without using any tools"

# ✓ Encourages tool use
system_prompt="Use the search tool when you need current information"
```

**4. Missing type hints:**
```python
# ✗ Agent doesn't know parameter types
def calculate(a, b):
    return a + b

# ✓ Clear types
def calculate(a: float, b: float) -> float:
    return a + b
```

### Error: Agent calls wrong tool

**Symptom:** Agent uses tool A when it should use tool B

**Solutions:**

**1. Improve docstrings to clarify when to use each tool:**
```python
def search_web(query: str) -> str:
    """
    Search the INTERNET for current information, news, facts.

    Use this for:
    - Current events
    - General knowledge
    - External information

    Do NOT use for:
    - Internal company data (use search_database instead)
    """
    pass

def search_database(query: str) -> str:
    """
    Search the INTERNAL company database.

    Use this for:
    - Employee information
    - Customer data
    - Company records

    Do NOT use for:
    - External information (use search_web instead)
    """
    pass
```

**2. Update system prompt with examples:**
```python
system_prompt="""
Use search_web for: "What's the weather?" "Latest news about AI"
Use search_database for: "Find employee John" "Customer records"
"""
```

**3. Use better model:**
```python
# gpt-4 is better at tool selection
agent = Agent("assistant", model="gpt-4o", tools=[...])
```

### Error: Tool called with wrong parameters

**Symptom:** Tool gets incorrect or missing parameters

**Solutions:**

**1. Add clear parameter descriptions:**
```python
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email.

    Args:
        to: Recipient email address (e.g., "user@example.com")
        subject: Email subject line (e.g., "Meeting Reminder")
        body: Full email message content

    Returns:
        Success or error message
    """
    pass
```

**2. Add parameter validation with helpful errors:**
```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""

    if "@" not in to:
        return f"Error: '{to}' is not a valid email address. Format: user@example.com"

    if not subject:
        return "Error: Email must have a subject line"

    if len(body) < 10:
        return "Error: Email body too short. Please provide a complete message."

    # Send email...
```

**3. Provide examples in docstring:**
```python
def schedule_meeting(date: str, time: str, attendees: str) -> str:
    """
    Schedule a meeting.

    Args:
        date: Date in YYYY-MM-DD format (e.g., "2024-03-15")
        time: Time in HH:MM format (e.g., "14:30")
        attendees: Comma-separated emails (e.g., "john@email.com, jane@email.com")

    Example:
        schedule_meeting("2024-03-15", "14:30", "john@email.com, jane@email.com")
    """
    pass
```

---

## Agent Behavior Issues

### Issue: Agent gives wrong answers

**Causes & Solutions:**

**1. Tool returns unclear information:**
```python
# ✗ Unclear result
def search(query):
    return data  # Raw data dump

# ✓ Formatted result
def search(query):
    results = api.search(query)
    return f"""
Found {len(results)} results for '{query}':

1. {results[0].title}
   {results[0].summary}

2. {results[1].title}
   {results[1].summary}
"""
```

**2. Need better system prompt:**
```python
system_prompt="""
You are a research assistant. Follow these rules:

1. Always cite sources when presenting information
2. If unsure, say "I'm not certain" instead of guessing
3. Use the search tool for current information
4. Verify facts before presenting them
"""
```

**3. Use better model:**
```python
# gpt-4 is more accurate than gpt-4o-mini
agent = Agent("assistant", model="gpt-4o")
```

### Issue: Agent enters infinite loop

**Symptom:** Agent keeps calling the same tool repeatedly

**Causes & Solutions:**

**1. Tool returns unclear success/failure:**
```python
# ✗ Unclear result
def send_email(to: str) -> str:
    smtp.send(to)
    return "Done"  # Agent can't tell if it succeeded

# ✓ Clear result
def send_email(to: str) -> str:
    try:
        smtp.send(to)
        return f"✓ SUCCESS: Email sent to {to}"
    except Exception as e:
        return f"✗ FAILED: Could not send email to {to}. Error: {str(e)}"
```

**2. Add iteration limit:**
```python
# Default is 10, but you can change it
agent = Agent(
    "assistant",
    tools=[...],
    max_iterations=5  # Stop after 5 tool calls
)
```

**3. Debug with auto_debug():**
```python
from connectonion.decorators import xray

@xray
def problematic_tool():
    pass

agent.auto_debug()
agent.input("Task that causes loop")

# See what's happening at each iteration
```

### Issue: Agent too slow

**Solutions:**

**1. Use faster model:**
```python
# gpt-4o-mini is much faster than gpt-4
agent = Agent("assistant", model="gpt-4o-mini")
```

**2. Reduce tool complexity:**
```python
# ✗ Slow - processes everything
def search(query):
    results = api.search(query)
    for r in results:
        r.analyze()  # Slow!
    return results

# ✓ Fast - only return what's needed
def search(query):
    results = api.search(query, limit=5)  # Limit results
    return format_top_results(results)  # Simple formatting
```

**3. Cache expensive operations:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_search(query: str):
    # Results cached for identical queries
    time.sleep(2)  # Slow operation
    return results
```

**4. Reduce system prompt length:**
```python
# ✗ Very long prompt (slow)
system_prompt = """[5000 words of instructions]"""

# ✓ Concise prompt (fast)
system_prompt = """Be helpful and use tools when needed."""
```

---

## Import and Installation Errors

### Error: "No module named 'connectonion'"

**Solutions:**

**1. Install ConnectOnion:**
```bash
pip install connectonion
```

**2. Verify installation:**
```bash
pip list | grep connectonion
```

**3. Check Python version:**
```bash
python --version  # Must be 3.9+
```

**4. Use correct Python:**
```bash
# If multiple Python versions:
python3.9 -m pip install connectonion
python3.9 your_script.py
```

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Cause:** Optional dependency not installed

**Solution:**
```bash
pip install python-dotenv
```

### Error: Import works but functions not found

**Symptom:**
```python
from connectonion import Agent  # Works
from connectonion import auto_debug  # Error
```

**Solution:**
```python
# Correct imports:
from connectonion import Agent
from connectonion.decorators import xray

# Then use:
agent = Agent("name")
agent.auto_debug()  # Method, not function
```

---

## Performance Issues

### Issue: High token usage / costs

**Solutions:**

**1. Use cheaper model:**
```python
agent = Agent("assistant", model="gpt-4o-mini")  # 60x cheaper than gpt-4
```

**2. Shorter system prompts:**
```python
# ✗ Expensive - long prompt sent every time
system_prompt = """[Very long instructions]"""

# ✓ Cheaper - concise prompt
system_prompt = """Be helpful. Use tools when needed."""
```

**3. Limit tool descriptions:**
```python
# ✗ Very long docstring
def tool():
    """
    [500 words explaining every detail]
    """
    pass

# ✓ Concise but clear
def tool():
    """
    Search the web for information.

    Args:
        query: Search query
    """
    pass
```

**4. Monitor usage:**
```python
# Check token usage
response = agent.input("Task")
print(f"Tokens used: {agent.last_usage}")  # If available
```

### Issue: Memory usage too high

**Solutions:**

**1. Clear conversation history:**
```python
# Agent keeps full conversation history
# Clear it periodically:
agent.current_session["messages"] = []
```

**2. Limit conversation turns:**
```python
# Start fresh agent for each task instead of long conversation:
for task in tasks:
    agent = Agent("assistant", tools=[...])
    agent.input(task)
```

---

## Debugging Checklist

When something goes wrong:

1. **Check API key**
   - `echo $OPENAI_API_KEY` or check `.env` file
   - Try key in a simple test: `import openai; openai.api_key="your-key"`

2. **Check tool docstrings**
   - Is the description clear?
   - Are parameters documented?
   - Are examples provided?

3. **Enable auto_debug()**
   ```python
   agent.auto_debug()
   # See exactly what's happening
   ```

4. **Check model**
   - Try a better model: `model="gpt-4o"`
   - Check if model is available in your region

5. **Simplify**
   - Remove tools one by one
   - Use minimal system prompt
   - Test with simple task first

6. **Check logs**
   - Look at console output
   - Check `.co/logs/` directory for agent logs

---

## Getting More Help

**Still stuck?**

1. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check examples:**
   - [Email Agent Example](Examples-Email-Agent-Example)
   - [Web Scraping Agent](Examples-Web-Scraping-Agent)

3. **Community help:**
   - [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)
   - [Discord Server](https://discord.gg/4xfD9k8AUF)
   - [Open an issue](https://github.com/wu-changxing/connectonion/issues)

4. **Documentation:**
   - [Official Docs](https://docs.connectonion.com)
   - [API Reference](https://docs.connectonion.com/api)
   - [Troubleshooting Guide](Troubleshooting)

---

**Related Guides:**
- [Use Auto-Debug](Use-Auto-Debug) - Debug interactively
- [Creating Custom Tools](Tutorials-Creating-Custom-Tools) - Tool best practices
- [FAQ](FAQ) - Common questions

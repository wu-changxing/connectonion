# Troubleshooting Guide

Quick fixes for common errors and issues with ConnectOnion. Find your error message, get the solution.

## Quick Navigation

- [Installation Errors](#installation-errors)
- [API Key Issues](#api-key-issues)
- [Agent Not Working](#agent-not-working)
- [Tool Problems](#tool-problems)
- [Performance Issues](#performance-issues)
- [Import Errors](#import-errors)

---

## Installation Errors

### "pip: command not found"

**Cause:** Python/pip not installed or not in PATH

**Solutions:**

**Mac:**
```bash
# Install Homebrew first if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Windows:**
1. Download Python from [python.org](https://python.org)
2. **Important:** Check "Add Python to PATH" during installation
3. Restart terminal

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### "Could not find a version that satisfies the requirement connectonion"

**Cause:** Python version too old or typo in package name

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version  # Must be 3.9+
   ```

2. **Upgrade Python:**
   ```bash
   # Mac
   brew install python@3.9

   # Linux
   sudo apt install python3.9
   ```

3. **Use correct package name:**
   ```bash
   pip install connectonion  # Not "connect-onion" or "ConnectOnion"
   ```

### "Permission denied" when installing

**Cause:** Trying to install system-wide without permissions

**Solutions:**

**Option 1: Use --user flag:**
```bash
pip install --user connectonion
```

**Option 2: Use virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

pip install connectonion
```

---

## API Key Issues

### "No API key found"

**Full Error:**
```
Error: No OpenAI API key found. Set OPENAI_API_KEY environment variable.
```

**Solutions:**

**1. Create `.env` file:**
```bash
# In your project directory
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**2. Set environment variable:**
```bash
# Mac/Linux
export OPENAI_API_KEY=sk-your-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Windows CMD
set OPENAI_API_KEY=sk-your-key-here
```

**3. Verify it's set:**
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Should print your key
```

### "Invalid API key"

**Full Error:**
```
AuthenticationError: Incorrect API key provided
```

**Solutions:**

1. **Check key format:**
   - OpenAI keys start with `sk-`
   - Must be complete (usually 48-51 characters)

2. **Get new key:**
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create new secret key
   - Copy entire key
   - Update `.env` file

3. **Check for extra spaces:**
   ```bash
   # ✗ Wrong (has space)
   OPENAI_API_KEY= sk-abc123

   # ✓ Correct
   OPENAI_API_KEY=sk-abc123
   ```

### "You exceeded your current quota"

**Full Error:**
```
RateLimitError: You exceeded your current quota, please check your plan and billing details
```

**Cause:** No credits in OpenAI account

**Solutions:**

1. **Add payment method:**
   - Go to [OpenAI Billing](https://platform.openai.com/account/billing)
   - Add credit card
   - Add credits

2. **Check usage:**
   - Visit [Usage Dashboard](https://platform.openai.com/usage)
   - See how much you've used

3. **Use cheaper model:**
   ```python
   agent = Agent("assistant", model="gpt-4o-mini")  # Much cheaper
   ```

---

## Agent Not Working

### Agent responds but never calls tools

**Symptom:** Agent gives text responses but doesn't use your tools

**Causes & Solutions:**

**1. Missing or bad docstring:**
```python
# ✗ Bad - no description
def my_tool(param):
    return result

# ✓ Good - clear description
def my_tool(param: str) -> str:
    """
    Clear description of what this tool does.

    Use this when: [explain when to use it]

    Args:
        param: What this parameter is for

    Returns:
        What this returns
    """
    return result
```

**2. Tool name too vague:**
```python
# ✗ Unclear
def process(data):
    pass

# ✓ Clear and descriptive
def search_customer_database(name: str):
    pass
```

**3. System prompt discourages tool use:**
```python
# ✗ Discourages tools
system_prompt="Answer all questions directly"

# ✓ Encourages tools
system_prompt="Use available tools to help answer questions"
```

**4. Missing type hints:**
```python
# ✗ No type information
def calculate(a, b):
    return a + b

# ✓ Clear types
def calculate(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b
```

### Agent calls wrong tool

**Symptom:** Agent uses tool A when it should use tool B

**Solution: Improve tool descriptions:**

```python
def search_web(query: str) -> str:
    """
    Search the INTERNET for current information.

    Use this for:
    - Current events and news
    - General knowledge from the web
    - External information

    Do NOT use for:
    - Company internal data (use search_database)
    - Historical company records
    """
    pass

def search_database(query: str) -> str:
    """
    Search INTERNAL company database.

    Use this for:
    - Employee information
    - Customer records
    - Company documents

    Do NOT use for:
    - External information (use search_web)
    - Current news or events
    """
    pass
```

### Agent gives wrong/inaccurate answers

**Solutions:**

**1. Improve system prompt:**
```python
system_prompt="""You are a helpful assistant.

Rules:
- Always cite sources for factual claims
- If unsure, say "I don't know" instead of guessing
- Use search tool for current information
- Verify facts before presenting them
"""
```

**2. Use better model:**
```python
# More accurate but slower/expensive
agent = Agent("assistant", model="gpt-4o")
```

**3. Improve tool output:**
```python
# ✗ Unclear result
def search(query):
    return data  # Raw dump

# ✓ Formatted result
def search(query):
    results = api.search(query)
    return f"""
Search Results for '{query}':

1. {results[0].title}
   {results[0].summary}

2. {results[1].title}
   {results[1].summary}

Source: {results[0].url}
"""
```

---

## Tool Problems

### "Tool not found" error

**Cause:** Tool not added to agent's tools list

**Solution:**

```python
# Make sure tool is in the list
agent = Agent(
    "assistant",
    tools=[my_tool_1, my_tool_2, my_tool_3]  # Include all tools
)
```

### Tool called with wrong parameters

**Symptom:** Tool receives incorrect or unexpected parameters

**Solutions:**

**1. Add parameter documentation:**
```python
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email.

    Args:
        to: Recipient email (e.g., "user@example.com")
        subject: Email subject (e.g., "Meeting Reminder")
        body: Complete email message

    Example:
        send_email("user@example.com", "Hello", "This is a test")
    """
    pass
```

**2. Add validation with helpful errors:**
```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""

    if "@" not in to:
        return f"Error: '{to}' is not a valid email. Format: user@example.com"

    if not subject:
        return "Error: Subject cannot be empty"

    if len(body) < 10:
        return "Error: Email body too short (minimum 10 characters)"

    # Send email...
```

### Tool raises exception and crashes agent

**Cause:** Unhandled exception in tool

**Solution: Add try/except:**

```python
def my_tool(param: str) -> str:
    """My tool description"""
    try:
        # Your code here
        result = some_operation(param)
        return f"Success: {result}"

    except ValueError as e:
        return f"Error: Invalid input - {str(e)}"

    except Exception as e:
        # Log the error
        logging.error(f"Tool error: {e}", exc_info=True)
        return f"Error: Operation failed - {str(e)}"
```

---

## Performance Issues

### Agent is very slow

**Causes & Solutions:**

**1. Using slow model:**
```python
# ✗ Slow
model="gpt-4o"

# ✓ Fast
model="gpt-4o-mini"  # 2-3x faster
```

**2. Long system prompt:**
```python
# ✗ Slow (long prompt sent every time)
system_prompt="""[5000 words of instructions]"""

# ✓ Fast (concise)
system_prompt="Be helpful. Use tools when needed."
```

**3. Slow tools:**
```python
# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def slow_api_call(query: str) -> str:
    # Results cached for repeated queries
    time.sleep(2)  # Slow operation
    return results
```

**4. Too many tool calls:**
```python
# Limit iterations
agent = Agent(
    "assistant",
    tools=[...],
    max_iterations=5  # Stop after 5 tool calls
)
```

### High token usage / expensive

**Solutions:**

**1. Use cheaper model:**
```python
agent = Agent("assistant", model="gpt-4o-mini")  # 60x cheaper
```

**2. Shorter prompts:**
```python
# Reduce system prompt length
# Reduce tool docstring length
# Keep conversation history short
```

**3. Monitor usage:**
```python
# Check OpenAI usage dashboard
# Set spending limits
```

---

## Import Errors

### "No module named 'connectonion'"

**Cause:** ConnectOnion not installed

**Solutions:**

```bash
# Install
pip install connectonion

# Verify
pip list | grep connectonion
```

### "No module named 'dotenv'"

**Cause:** Optional dependency not installed

**Solution:**
```bash
pip install python-dotenv
```

### "Cannot import name 'xray'"

**Cause:** Wrong import path

**Solution:**
```python
# ✗ Wrong
from connectonion import xray

# ✓ Correct
from connectonion.decorators import xray
```

### "No module named 'openai'"

**Cause:** OpenAI library not installed (should be automatic)

**Solution:**
```bash
pip install openai
```

---

## Debug Mode Issues

### auto_debug() doesn't pause

**Causes:**

**1. Missing @xray decorator:**
```python
# ✗ Won't pause
def my_tool():
    pass

# ✓ Will pause
from connectonion.decorators import xray

@xray
def my_tool():
    pass
```

**2. Forgot to call auto_debug():**
```python
agent = Agent("assistant", tools=[my_tool])
agent.auto_debug()  # Don't forget this!
```

**3. Tool not being called:**
- Agent might not think it needs the tool
- Improve tool docstring

### Can't modify variables in Python Edit mode

**Solution:**

```python
# After modifying variables:
>>> result = "new value"
>>> /continue  # Required to apply changes!
```

---

## Getting More Help

### Still having issues?

1. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use auto_debug():**
   ```python
   agent.auto_debug()
   # See exactly what's happening
   ```

3. **Check examples:**
   - [Email Agent Example](Examples-Email-Agent-Example)
   - [Web Scraping Agent](Examples-Web-Scraping-Agent)

4. **Ask the community:**
   - [Discord Server](https://discord.gg/4xfD9k8AUF)
   - [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)
   - [Open an Issue](https://github.com/wu-changxing/connectonion/issues)

### Error not listed here?

Please [open an issue](https://github.com/wu-changxing/connectonion/issues) or ask in [Discord](https://discord.gg/4xfD9k8AUF) so we can add it to this guide!

---

**Related Guides:**
- [Debug Agent Errors](How-To-Debug-Agent-Errors) - Detailed debugging guide
- [FAQ](FAQ) - Common questions
- [Interactive Debugging](Tutorials-Interactive-Debugging-Guide) - Learn auto_debug()

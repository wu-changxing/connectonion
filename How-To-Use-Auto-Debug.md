# How-To: Use auto_debug() to Debug AI Agents

**Quick reference guide for debugging AI agents interactively.** Learn keyboard shortcuts, Python REPL editing, AI help mode, and real-world debugging workflows for Python AI agents. Perfect for developers debugging LLM function calling, tool execution, and agent behavior.

**Keywords:** debug ai agent python, interactive debugging python, llm debugging tools, python agent debugger, ai tool execution debug, breakpoint debugging ai

## Quick Reference

### Enable Debugging

```python
from connectonion import Agent
from connectonion.decorators import xray

@xray  # Mark tool as breakpoint
def my_tool(param: str) -> str:
    return f"Result: {param}"

agent = Agent("assistant", tools=[my_tool])
agent.auto_debug()  # Enable interactive debugging
```

### What You See at Breakpoints

When execution pauses, the debugger shows:
- **User Prompt:** Your original task
- **Tool Called:** Which function was executed (e.g., `search()`)
- **Arguments:** Parameters passed to the tool
- **Result:** What the tool returned
- **Next LLM Action:** ✨ **Preview of what the agent plans to do next** (if available)
- **Progress:** Current iteration (e.g., "Iteration 2/10")
- **Previous Tools:** What the agent did before this

### Debug Menu Commands

When paused at a breakpoint, use **arrow keys** to navigate and **Enter** to select:

| Command | Shortcut | Description |
|---------|----------|-------------|
| Continue execution | `c` or `Enter` | Resume agent execution |
| Ask AI for help | `a` | Get debugging assistance from AI |
| Edit variables (Python) | `e` | Open Python REPL to modify state |
| View execution trace | `v` | See full execution history |
| Toggle step mode | `s` | Pause at every tool call |
| Stop debugging | `q` | Exit debug session |

**Navigation:** Use ↑/↓ arrow keys to select, then press Enter. Or type the shortcut letter directly.

### Universal Commands

Work from anywhere in debug mode:

| Command | Description |
|---------|-------------|
| `/menu` | Return to main menu |
| `/continue` | Resume execution |
| `?` | Show help |

## Complete Real-World Example

Here's what a full debugging session looks like from start to finish:

```python
# research_agent.py
from connectonion import Agent
from connectonion.decorators import xray

@xray  # We want to debug web searches
def web_search(query: str) -> str:
    """Search the web and return results."""
    # Simulated search
    if "python" in query.lower():
        return "Found: Python is a programming language..."
    return "No results found"

@xray  # We want to debug analysis
def analyze_content(text: str) -> str:
    """Analyze text and extract insights."""
    return f"Analysis: {text[:50]}... [key insights extracted]"

# Create agent with debugging enabled
agent = Agent(
    name="researcher",
    model="co/gpt-4o-mini",
    tools=[web_search, analyze_content],
    system_prompt="You help with research tasks."
)

# Start debugging session
agent.auto_debug()

# Run a research task
agent.input("Research Python programming and analyze the results")
```

**What happens:**

```
🐛 Debug Session Started for 'researcher'
═══════════════════════════════════════════

User Prompt: Research Python programming and analyze the results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Breakpoint Hit: web_search()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tool: web_search
Arguments: {"query": "Python programming"}
Result: "Found: Python is a programming language..."

💡 Next LLM Action:
  → analyze_content(text="Found: Python is...")

Progress: Iteration 1/10
Previous Tools: [none]

┌─────────────────────────────────────────┐
│ What would you like to do?              │
├─────────────────────────────────────────┤
│ ▸ Continue execution                    │  ← Use arrow keys
│   Ask AI for help                       │
│   Edit variables (Python REPL)          │
│   View execution trace                  │
│   Toggle step mode                      │
│   Stop debugging                        │
└─────────────────────────────────────────┘

> c  ← Type 'c' or press Enter

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Breakpoint Hit: analyze_content()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tool: analyze_content
Arguments: {"text": "Found: Python is a programming language..."}
Result: "Analysis: Found: Python is a programming language... [key insights extracted]"

💡 Next LLM Action:
  → [No more tools] Task complete!

Progress: Iteration 2/10

> c

✅ Task Completed Successfully!
```

This shows the complete flow: breakpoints trigger, you see what's happening, preview next actions, and control execution.

## Common Workflows

### Workflow 1: Quick Inspection

**Use case:** Just want to see what's happening

```python
agent.auto_debug()
agent.input("Your task")

# At breakpoint:
> c  # Just press Enter to continue

# See tool calls and results, then continue
```

### Workflow 2: Debug a Problem

**Use case:** Something's wrong, need to investigate

```python
agent.auto_debug()
agent.input("Task that's failing")

# At breakpoint:
> a  # Ask AI for help

ai> Why did this tool get called with the wrong parameter?
AI: [Explains the issue and suggests fixes]

ai> /menu

> e  # Fix the parameter in Python mode

>>> parameter = "correct_value"
>>> /continue
```

### Workflow 3: Test "What If" Scenarios

**Use case:** Want to see alternative outcomes

```python
agent.auto_debug()
agent.input("Your task")

# At first breakpoint:
> e

>>> # Try different result
>>> result = "alternative_outcome"
>>> /continue

# Agent continues with your modified result
```

### Workflow 4: Step Through Everything

**Use case:** Debug complex multi-step workflow

```python
agent.auto_debug()
agent.input("Complex multi-step task")

# At first breakpoint:
> s  # Enable step mode

# Now agent pauses at EVERY tool call
# Step through each one with 'c'
```

## Understanding the LLM Preview

The "Next LLM Action" preview is a powerful feature that shows what the agent plans to do next:

### How It Works

After each tool execution, the debugger:
1. Simulates the next LLM call with the current tool result
2. Shows what tools the agent plans to call next
3. **Does NOT execute** the tools - just previews the plan

### Example Preview Displays

```
💡 Next LLM Action:
  → analyze_content(text="Found: Python is...")
  → write_summary(content="Analysis complete")
```

This shows the agent plans to call **two tools** in sequence.

```
💡 Next LLM Action:
  → [No more tools] Task complete!
```

This shows the agent is done and will respond with text instead of calling more tools.

```
💡 Next LLM Action:
  → [Preview unavailable]
```

Preview temporarily unavailable (network issue, etc.). Not critical - just continue.

### Why Preview Is Useful

**See the future:** Know what's coming before it happens
- "The agent is about to call the wrong tool - I should edit the result"
- "Perfect, next step is exactly what I expected"
- "Why is it calling search() again? Let me check with AI help"

**Catch errors early:** Fix problems before they compound
- See the agent is stuck in a loop before wasting iterations
- Notice incorrect parameters before the tool fails
- Identify missing tools the agent is trying to call

**Learn agent behavior:** Understand how your agent thinks
- See the decision-making process in action
- Discover when tools should be combined vs. separate
- Identify opportunities to improve system prompts

## AI Help Mode Examples

### Ask Why Something Happened

```
ai> Why did the agent call search() instead of calculate()?

AI: The agent called search() because the user's query "What is 2+2"
contains the word "what", which the LLM interpreted as an information
request rather than a calculation. The calculate() tool would be more
appropriate here.

Suggestion: Update the system prompt to clarify when to use calculate()
for mathematical expressions.
```

### Ask What to Do Next

```
ai> The search returned no results. What should I do?

AI: You have several options:
1. Continue execution (c) - let the agent handle the empty result
2. Edit the result (e) - provide sample data to test error handling
3. Modify the query (e) - try a broader search term

I recommend option 1 to see how the agent handles this edge case.
```

### Ask for Debugging Suggestions

```
ai> The agent keeps calling the same tool repeatedly. How do I fix this?

AI: This is likely an infinite loop. Common causes:
1. Tool returns unclear results - LLM can't tell if task is complete
2. System prompt doesn't specify success criteria
3. Tool error message isn't clear enough

Quick fix: Press 'q' to stop, then update the tool's return message
to be more explicit about success/failure.
```

## Python Edit Mode Examples

### Fix a Parameter

```python
>>> # See current parameters
>>> query
'Johhn'  # Typo!

>>> # Fix it
>>> query = 'John'

>>> # Re-run tool with fixed parameter
>>> result = search(query)

>>> # Continue with corrected result
>>> /continue
```

### Modify Tool Result

```python
>>> # Current result
>>> result
'Error: Not found'

>>> # Provide fallback data for testing
>>> result = 'Found: john@example.com'

>>> # Agent continues with modified result
>>> /continue
```

### Test Edge Cases

```python
>>> # Try empty result
>>> result = ''
>>> /continue

# See how agent handles it

# Try again with different data
>>> result = 'Too many results (1000+)'
>>> /continue
```

### Inspect Variables

```python
>>> # See all available variables
>>> dir()
['query', 'result', 'tool_args', 'agent', ...]

>>> # Inspect complex objects
>>> tool_args
{'query': 'Python', 'limit': 10}

>>> # Check agent state
>>> agent.current_session['trace']
[...]  # Full execution history
```

## Breakpoint Strategies

### Strategy 1: Mark Critical Tools Only

```python
@xray  # Debug this - database writes are critical
def save_to_database(data: dict):
    db.save(data)
    return "Saved"

# No @xray - simple tool, unlikely to fail
def get_current_time():
    return datetime.now().isoformat()
```

### Strategy 2: Debug Integration Points

```python
@xray  # External API - might fail
def call_external_api(endpoint: str):
    return requests.get(endpoint).text

@xray  # User input - validate before processing
def process_user_data(data: str):
    validated = validate(data)
    return process(validated)
```

### Strategy 3: Temporary Debugging

```python
# Add @xray temporarily for debugging
@xray
def problematic_tool():
    # ... having issues with this
    pass

# Remove @xray after fixing
def problematic_tool():
    # ... now working correctly
    pass
```

## Step Mode Use Cases

### When to Use Step Mode

**✓ Use step mode when:**
- Debugging complex multi-step workflows
- Need to see every tool call in sequence
- Looking for where things go wrong
- Learning how agent makes decisions

**✗ Don't use step mode when:**
- Agent works correctly (too much overhead)
- Only interested in specific tools (use @xray instead)
- Quick testing (slows down execution)

### Step Mode Example

```python
agent.auto_debug()
agent.input("Search for Python, analyze the results, and write a summary")

# At first breakpoint:
> s  # Enable step mode

# Pause 1: search() tool
> c

# Pause 2: analyze() tool
> c

# Pause 3: write_summary() tool
> s  # Disable step mode (toggle)
> c  # Continue without stepping
```

## Troubleshooting auto_debug()

### Issue: Breakpoints Not Triggering

**Problem:** Agent runs without pausing

**Solutions:**
```python
# ✓ Make sure @xray is applied
from connectonion.decorators import xray

@xray  # This is required!
def my_tool():
    pass

# ✓ Verify auto_debug() is called
agent.auto_debug()  # Don't forget this!

# ✓ Check tool is actually being used
# Add logging to confirm:
def my_tool():
    print("Tool was called!")  # Should see this
    return "result"
```

### Issue: Can't Modify Variables

**Problem:** Changes in Python mode don't apply

**Solutions:**
```python
# ✓ Make sure to use /continue after changes
>>> result = "new value"
>>> /continue  # Required!

# ✓ Check variable exists in scope
>>> dir()  # List all available variables

# ✓ Modify the right variable
>>> tool_args  # Read-only - shows parameters
>>> result  # This is what you modify
```

### Issue: AI Help Not Useful

**Problem:** AI gives generic responses

**Solutions:**
```
# ✗ Vague question
ai> help

# ✓ Specific question
ai> Why did search() return an empty string instead of results?

# ✓ Provide context
ai> The agent called calculate() but I expected search(). Why?

# ✓ Ask for actionable advice
ai> What should I change to fix this error?
```

## Production Considerations

### Disable Debugging in Production

```python
import os

agent = Agent("assistant", tools=[...])

# Only debug in development
if os.getenv("ENV") == "development":
    agent.auto_debug()

agent.input(task)
```

### Remove @xray Decorators

```python
# Development - with debugging
@xray
def my_tool():
    pass

# Production - remove @xray
def my_tool():
    pass
```

### Keep @xray for Monitoring

```python
# You can keep @xray in production for visibility
# Just don't call auto_debug()
@xray
def critical_operation():
    # @xray shows enhanced logging even without debugging
    pass
```

## Tips and Tricks

### Tip 1: Use Shortcuts

```
# Instead of arrow keys + Enter:
> c  # Continue
> a  # AI help
> e  # Python edit
> v  # View trace
> s  # Step mode
> q  # Quit
```

### Tip 2: Combine with Print Debugging

```python
@xray
def my_tool(param):
    print(f"DEBUG: param={param}")  # Still useful!
    result = process(param)
    print(f"DEBUG: result={result}")
    return result
```

### Tip 3: Save Execution Traces

```python
# In Python edit mode:
>>> import json
>>> with open('debug_trace.json', 'w') as f:
...     json.dump(agent.current_session['trace'], f, indent=2)
>>> /continue

# Now you have a trace file to analyze later
```

### Tip 4: Test Error Scenarios

```python
# At breakpoint, inject errors to test handling:
>>> result = "Error: Database connection failed"
>>> /continue

# See how agent handles the error
```

## Next Steps

- **Learn Agents:** [How AI Agents Work](Tutorials-Agent-Core-Concepts) - Complete tutorial on AI agents
- **Fix Issues:** [Debug Agent Errors](Debug-Agent-Errors) - Troubleshooting guide
- **Examples:** [Email Agent with Debugging](Examples-Email-Agent-Example) - Real-world example

## Summary

**Remember:**
- Add `@xray` to tools you want to debug
- Call `agent.auto_debug()` to enable
- Press `c` or Enter to continue (most common)
- Use `a` for AI help when confused
- Use `e` to modify variables and test scenarios
- Use `s` for step-by-step debugging
- Use `q` to exit when done

**Most important:** You don't need to learn everything - just start with `c` to continue, and discover other features as needed!

---

**Related:** [Debug Agent Errors](Debug-Agent-Errors) | [Deploy to Production](Deploy-To-Production)

# Tutorial: Interactive Debugging for AI Agents with auto_debug()

Learn how to debug AI agents interactively - pause execution, inspect variables, ask AI for help, and modify behavior in real-time. This is like using a debugger for traditional code, but designed specifically for AI agents.

## What You'll Learn

- How to enable interactive debugging with `auto_debug()`
- How to set breakpoints using the `@xray` decorator
- How to navigate the debug menu with arrow keys
- How to ask AI for debugging help
- How to edit variables with Python REPL
- How to use step mode to pause at every tool call

**Time**: 10 minutes
**Level**: Beginner to Intermediate
**Prerequisites**: Basic ConnectOnion knowledge ([Quick Start](../Quick-Start))

## Why Debug AI Agents?

AI agents make decisions you can't see. When something goes wrong, you need to:
- **See what's happening** - Which tools are being called?
- **Understand why** - Why did the agent make that choice?
- **Fix issues** - Change behavior without rewriting code
- **Explore alternatives** - What if the agent tried something different?

Interactive debugging solves all of these!

## Quick Start Example

### Step 1: Add `@xray` to Tools

```python
from connectonion import Agent
from connectonion.decorators import xray

@xray  # This tool becomes a breakpoint
def search_emails(query: str):
    """Search for emails matching a query"""
    # Your search logic
    return f"Found emails for: {query}"

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    return f"Sent email to {to}"

agent = Agent(
    name="email-assistant",
    tools=[search_emails, send_email]
)
```

**The `@xray` decorator marks tools as debugging breakpoints** - the agent will pause when it calls them.

### Step 2: Enable Debugging

```python
# Enable interactive debugging
agent.auto_debug()

# Now give it a task
agent.input("Send email to John about the meeting")
```

### Step 3: Interact with the Debug Menu

When the agent calls `search_emails()`, you'll see:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@xray BREAKPOINT: search_emails

Local Variables:
  query = "John"
  result = "Found emails for: John"

Context:
  User: "Send email to John about the meeting"
  Iteration: 1/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What do you want to do?
  → Continue execution       [Enter or c]
    Ask AI for help          [a]
    Edit variables (Python)  [e]
    View execution trace     [v]
    Toggle step mode         [s]
    Stop debugging           [q]

💡 Use ↑↓ arrows and Enter, or shortcuts
>
```

**Press `c` or Enter** to continue execution!

## Debug Menu Options

### Option 1: Continue Execution (Default)

**Shortcut**: `c` or `Enter`

```
> c

Resuming execution...
→ Tool: send_email(to="john@company.com", subject="Meeting", body="...")
← Result (187ms): Sent email to john@company.com

✓ Task complete
```

**When to use**: You've inspected what you need, let the agent continue.

### Option 2: Ask AI for Help

**Shortcut**: `a`

```
> a

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI HELP MODE
Ask questions about the current execution state.

Type /menu to return to the main menu.
Type /continue to resume execution.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ai> Why did the agent search for "John" instead of "John Smith"?

AI: The agent searched for "John" because that's what appeared in the
user's message. The LLM extracted the first name only. To fix this,
you could:
1. Modify the query variable to "John Smith"
2. Update the system prompt to extract full names
3. Add a tool to clarify ambiguous names

ai> What should I do next?

AI: I recommend continuing execution to see if the email gets sent
correctly. If the wrong email is selected, you can use Python Edit
mode (e) to modify the result before the agent proceeds.

ai> /menu
```

**When to use**:
- You don't understand why something happened
- You want suggestions for fixing issues
- You need help understanding the agent's state

### Option 3: Edit Variables (Python REPL)

**Shortcut**: `e`

```
> e

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PYTHON EDIT MODE
Full Python REPL at the breakpoint.

Available variables:
  - query = "John"
  - result = "Found emails for: John"
  - tool_args = {"query": "John"}

Type /menu to return to the main menu.
Type /continue to resume with your changes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

>>> query
'John'

>>> # Change the query to be more specific
>>> query = "John Smith"

>>> # Re-run the search with the new query
>>> result = search_emails(query)

>>> result
'Found emails for: John Smith'

>>> # Continue with the modified result
>>> /continue

Resuming with your changes...
✓ Using modified variables: query, result
```

**When to use**:
- Fix incorrect tool parameters
- Modify tool results before the agent sees them
- Test different scenarios ("what if?")
- Explore the execution state

### Option 4: View Execution Trace

**Shortcut**: `v`

```
> v

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION TRACE

Iteration 1:
  User: "Send email to John about the meeting"

  LLM Response:
    Tool calls: 1
    - search_emails(query="John")

  Tool Executions:
    ✓ search_emails → "Found emails for: John"

  Status: ⏸️  Paused at search_emails
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Press Enter to return to menu
>
```

**When to use**:
- See the full history of what happened
- Understand the sequence of tool calls
- Debug multi-step workflows

### Option 5: Toggle Step Mode

**Shortcut**: `s`

```
> s

🔍 STEP MODE: ON
Agent will now pause at EVERY tool call (not just @xray tools)

> c

Resuming...
→ Tool: send_email(to="john@company.com", ...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP MODE BREAKPOINT: send_email

Local Variables:
  to = "john@company.com"
  subject = "Meeting"
  body = "Hi John, ..."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What do you want to do?
  → Continue (step)
    Exit step mode
    ...
>
```

**When to use**:
- Debug complex flows with many tool calls
- Find exactly where something goes wrong
- Understand the complete execution path

### Option 6: Stop Debugging

**Shortcut**: `q`

```
> q

Stopping debug session...
✓ Debug session ended

Type your message to the agent:
>
```

**When to use**: You're done debugging and want to exit.

## Real-World Example: Debug an Email Agent

Let's debug a real scenario where things go wrong:

```python
from connectonion import Agent
from connectonion.decorators import xray
import smtplib

@xray
def search_contacts(name: str):
    """Find contact email by name"""
    contacts = {
        "John": "john.doe@company.com",
        "Jane": "jane.smith@company.com"
    }
    return contacts.get(name, "Not found")

@xray
def send_email(to: str, subject: str, body: str):
    """Send an email"""
    # Simulated - replace with real SMTP
    if "@" not in to:
        return f"Error: Invalid email '{to}'"
    return f"✓ Sent email to {to}"

agent = Agent(
    name="email-bot",
    tools=[search_contacts, send_email],
    system_prompt="You are an email assistant. Always verify emails before sending."
)

# Enable debugging
agent.auto_debug()

# Give it a task (this will hit an error!)
agent.input("Send an email to Jon about the project update")
```

### Debugging Session:

**1. Agent pauses at `search_contacts`:**
```
@xray BREAKPOINT: search_contacts

Local Variables:
  name = "Jon"
  result = "Not found"

What do you want to do?
> a

ai> Why was the contact not found?

AI: The contact wasn't found because "Jon" (user's spelling) doesn't
match "John" (database spelling). The agent searched for the exact
string "Jon" which doesn't exist in contacts.

ai> /menu

> e

>>> name
'Jon'

>>> # Fix the typo
>>> name = "John"
>>> result = search_contacts(name)
>>> result
'john.doe@company.com'

>>> /continue
```

**2. Agent continues and pauses at `send_email`:**
```
@xray BREAKPOINT: send_email

Local Variables:
  to = "john.doe@company.com"  # ✓ Corrected!
  subject = "Project Update"
  body = "Hi John, ..."

What do you want to do?
> c

Resuming...
✓ Sent email to john.doe@company.com
```

**Success!** We caught and fixed the typo during debugging.

## Advanced: Step Mode for Complex Workflows

When you have many tool calls, use step mode:

```python
@xray
def search(query: str):
    return f"Results for {query}"

@xray
def analyze(text: str):
    return f"Analysis: {text}"

@xray
def summarize(text: str):
    return f"Summary: {text}"

agent = Agent(
    "researcher",
    tools=[search, analyze, summarize]
)

agent.auto_debug()

# This will call multiple tools - step through each one
agent.input("Search for Python tutorials, analyze the results, and summarize")
```

Press `s` at the first breakpoint to enable step mode, then you'll pause at every tool:

```
1. Pause at search()
2. Pause at analyze()
3. Pause at summarize()
```

## Tips and Best Practices

### Tip 1: Use `@xray` on Critical Tools

```python
@xray  # Debug this
def database_query(sql: str):
    """Critical - might fail"""
    pass

# Don't debug this (simple, unlikely to fail)
def get_current_time():
    return datetime.now().isoformat()
```

### Tip 2: Ask AI for Debugging Suggestions

```
ai> The agent is calling the wrong function. What should I do?

AI: Based on the context, it seems the system prompt isn't clear
about when to use each tool. Try updating the prompt to specify:
"Use search_web() for general queries, and search_database() for
internal company information."
```

### Tip 3: Use Python Edit for "What If" Scenarios

```python
>>> # Original result
>>> result
'Found 5 results'

>>> # What if there were more results?
>>> result = 'Found 100 results'
>>> /continue

# Agent now processes the "what if" scenario
```

### Tip 4: Combine with Regular Debugging

```python
@xray
def process_data(data: str):
    import pdb; pdb.set_trace()  # Traditional debugger
    # Process data
    return result

# Now you have BOTH:
# 1. ConnectOnion's interactive menu (agent-level)
# 2. PDB debugger (code-level)
```

## Troubleshooting

**Issue: Breakpoints not triggering**
- ✓ Make sure `@xray` decorator is applied
- ✓ Verify `agent.auto_debug()` was called
- ✓ Check tool is actually being called by agent

**Issue: Can't edit variables**
- ✓ Enter Python Edit mode with `e`
- ✓ Variables must exist in current scope
- ✓ Use `/continue` to apply changes

**Issue: AI help not useful**
- ✓ Provide more context in your question
- ✓ Ask specific questions
- ✓ Try viewing the trace first (`v`)

More help: [Debug Agent Errors Guide](../How-To/Debug-Agent-Errors)

## Next Steps

**Master Debugging:**
- [How to Use Auto-Debug](../How-To/Use-Auto-Debug) - Feature reference
- [Debug Agent Errors](../How-To/Debug-Agent-Errors) - Common issues

**Build More:**
- [Creating Custom Tools](Creating-Custom-Tools) - Advanced tool patterns
- [Email Agent Example](../Examples/Email-Agent-Example) - Real example with debugging

**Deploy:**
- [Deploy to Production](../How-To/Deploy-To-Production) - Remove debug code for prod

## Summary

Interactive debugging with `auto_debug()` gives you:
- **Visibility** - See what the agent is doing
- **Control** - Pause and inspect at breakpoints
- **AI Assistance** - Get debugging help from AI
- **Modification** - Change behavior without restarting
- **Exploration** - Test "what if" scenarios

Just add `@xray` to tools and call `agent.auto_debug()` - that's it!

---

**Next:** [Creating Custom Tools Tutorial](Creating-Custom-Tools)

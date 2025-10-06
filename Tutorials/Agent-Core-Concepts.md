# How AI Agents Work - Python Agent Tutorial | ConnectOnion

**Learn how AI agents combine language models with tools to complete tasks autonomously. Step-by-step tutorial with working code examples for building intelligent Python agents.**

## What You'll Learn

- How AI agents decide when to use tools
- The agent execution loop explained from first principles
- Building your first tool-using agent with real examples
- Common patterns and best practices for agent development

## Quick Links

- [Jump to code examples](#simple-example-calculator-agent)
- [Jump to how it works](#how-agents-work-the-execution-loop)
- [Jump to common issues](#common-issues)

---

## What is an AI Agent?

AI agents are like smart assistants that can **use tools** to complete tasks. Instead of just answering questions with text, they can take actions: search databases, send emails, call APIs, run code, browse the web.

### The Key Difference

**Regular LLM (ChatGPT-style):**
```
You: "Find blue shirts in our database"
LLM: "I don't have access to your database, but you could search for..."
```

**AI Agent:**
```
You: "Find blue shirts in our database"
Agent: [Calls search_database("blue shirts")]
Agent: "I found 10 blue shirts in stock. Here they are: ..."
```

The magic: **The AI decides WHEN to use tools based on your request.**

---

## Simple Example: Calculator Agent

Let's build the simplest possible agent - one that can do math:

```python
from connectonion import Agent

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)  # Use carefully!
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Create agent with the calculator tool
agent = Agent("math_bot", tools=[calculate])

# Give it a task
agent.input("What is 42 * 17?")
```

**Output:**
```
INPUT: What is 42 * 17?

  Iteration 1/10
  → LLM Request (o4-mini)
  ← LLM Response (234ms): 1 tool call
  → Tool: calculate({"expression": "42 * 17"})
  ← Result (1ms): 714

  Iteration 2/10
  → LLM Request (o4-mini)
  ← LLM Response (189ms)

✓ Complete (0.4s)

To calculate 42 * 17, I'll use the calculator.
The result is 714.
```

### What Just Happened?

1. **User asks**: "What is 42 * 17?"
2. **Agent thinks**: "I need to use the calculate tool"
3. **Agent calls**: `calculate("42 * 17")`
4. **Tool returns**: `"714"`
5. **Agent responds**: "The result is 714"

The agent automatically decided to use the tool - you didn't have to tell it!

---

## How Agents Work: The Execution Loop

Under the hood, agents run a simple but powerful loop:

```
1. User gives task
   ↓
2. LLM decides what to do
   ↓
3. Call tools (if needed)
   ↓
4. LLM sees results
   ↓
5. Repeat until done
```

### Detailed Example with Multiple Tools

Let's see this in action with an agent that can search AND calculate:

```python
from connectonion import Agent

def search_products(query: str) -> str:
    """Search our product database."""
    # Simulated search - in real app, query a database
    return f"Found 10 products matching '{query}'"

def calculate_discount(price: float, percent: float) -> str:
    """Calculate discount price."""
    discounted = price * (1 - percent/100)
    return f"${discounted:.2f}"

agent = Agent(
    "shop_assistant",
    tools=[search_products, calculate_discount]
)

agent.input("Find laptops and calculate 20% off $1200")
```

**What happens (step by step):**

```
Iteration 1:
User: "Find laptops and calculate 20% off $1200"
↓
LLM thinks: "I need to search for laptops AND calculate discount"
↓
LLM decides: Call BOTH tools!
↓
Tool 1: search_products("laptops") → "Found 10 products..."
Tool 2: calculate_discount(1200, 20) → "$960.00"
↓
Iteration 2:
LLM sees both results
↓
LLM responds: "I found 10 laptops. With 20% off, $1200 becomes $960."
```

Notice: The agent called **both tools in one iteration** because it understood it needed both!

---

## The Three Core Components

Every agent has three essential parts:

### 1. **Name** (required)
Simple identifier for your agent:
```python
agent = Agent("shop_assistant")
```

### 2. **Tools** (optional but useful)
Functions the agent can call:
```python
def search(query: str) -> str:
    """Search for products."""
    return results

agent = Agent("bot", tools=[search])
```

### 3. **System Prompt** (optional)
Personality and behavior instructions:
```python
agent = Agent(
    "bot",
    system_prompt="You are a helpful shopping assistant. Always be friendly."
)
```

---

## Real-World Example: Email Agent

Let's build something practical - an agent that can search and send emails:

```python
from connectonion import Agent
import smtplib
from email.mime.text import MIMEText

def search_emails(query: str) -> str:
    """Search inbox for emails matching query."""
    # In real app, connect to email API
    return f"Found 3 emails about '{query}': email1@ex.com, email2@ex.com, email3@ex.com"

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to someone."""
    # In real app, actually send email
    return f"Email sent to {to} with subject: {subject}"

agent = Agent(
    "email_assistant",
    tools=[search_emails, send_email],
    system_prompt="You are an email assistant. Be concise and professional."
)

# Multi-step task - agent figures out the sequence!
agent.input("Find emails from John and send him a reply thanking him")
```

**What the agent does:**

1. **Iteration 1**: Calls `search_emails("John")` → gets results
2. **Iteration 2**: Calls `send_email("john@ex.com", "Thank you", "...")` → sends email
3. **Final response**: "I found John's emails and sent him a thank you reply."

The agent **automatically chained the tools** - search first, then send!

---

## Key Concepts Explained

### Concept 1: Tools are Just Functions

You don't need special classes or inheritance. Any Python function can be a tool:

```python
# ✅ Simple function = tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

agent = Agent("bot", tools=[get_time])
```

The only requirements:
- **Docstring** - Agent reads this to understand what the tool does
- **Type hints** - Helps agent use the tool correctly
- **Returns something** - Agent needs a result to work with

### Concept 2: The Agent Decides

You don't write "if user asks X, call tool Y". The LLM figures it out:

```python
agent = Agent("bot", tools=[search, calculate, get_time])

# Agent automatically picks the right tool for each question:
agent.input("What time is it?")          # → Uses get_time
agent.input("Search for Python")         # → Uses search
agent.input("What's 10 + 5?")            # → Uses calculate
```

### Concept 3: Iteration Limits

Agents can call tools multiple times. Set a limit to prevent infinite loops:

```python
agent = Agent(
    "bot",
    tools=[search, calculate],
    max_iterations=5  # Stop after 5 tool calls
)
```

**When to use different limits:**

| Task Complexity | Recommended Limit | Example |
|----------------|-------------------|---------|
| Simple (1-2 tools) | 3-5 | "Calculate 2+2" |
| Standard | 8-10 | "Search and summarize" |
| Complex | 15-25 | Browser automation, data analysis |

---

## Common Patterns

### Pattern 1: Search → Process → Respond

```python
def search_docs(query: str) -> str:
    """Search documentation."""
    return f"Found docs about {query}"

def summarize(text: str) -> str:
    """Summarize text."""
    return f"Summary: {text[:100]}..."

agent = Agent("helper", tools=[search_docs, summarize])
agent.input("Find docs about agents and summarize them")

# Agent automatically:
# 1. Searches docs
# 2. Summarizes results
# 3. Returns summary
```

### Pattern 2: Validate → Act → Confirm

```python
def check_balance(account: str) -> str:
    """Check if account has funds."""
    return "Balance: $500"

def transfer_money(from_account: str, to_account: str, amount: float) -> str:
    """Transfer money between accounts."""
    return f"Transferred ${amount}"

agent = Agent("banking", tools=[check_balance, transfer_money])
agent.input("Transfer $100 from checking to savings")

# Agent flow:
# 1. Checks balance first
# 2. Performs transfer
# 3. Confirms completion
```

### Pattern 3: Multi-Step Research

```python
def search_web(query: str) -> str:
    """Search the internet."""
    return "Search results..."

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text."""
    return "Positive"

def save_report(content: str) -> str:
    """Save report to file."""
    return "Saved to report.txt"

agent = Agent("researcher", tools=[search_web, analyze_sentiment, save_report])
agent.input("Research Python AI frameworks, analyze sentiment, and save a report")

# Agent chains all three tools automatically!
```

---

## Common Issues

### Issue 1: Agent Not Using Tools

**Symptoms:** Agent just talks instead of calling tools

**Cause 1: Missing or unclear docstrings**

❌ **Bad:**
```python
def search(q):
    return results
```

✅ **Good:**
```python
def search(query: str) -> str:
    """Search our product database for items matching the query."""
    return results
```

**Cause 2: Tool doesn't match the task**

If you ask "What's the weather?" but only have a `calculate` tool, the agent can't help. Add relevant tools!

### Issue 2: Too Many Iterations

**Symptoms:** "Maximum iterations reached" error

**Solution:** Increase `max_iterations`:
```python
agent = Agent("bot", tools=[...], max_iterations=20)  # Was 10
```

### Issue 3: Tool Errors

**Symptoms:** Agent gets stuck or returns "Error"

**Cause:** Tool crashed or returned invalid data

**Solution:** Add error handling in tools:
```python
def search(query: str) -> str:
    """Search for items."""
    try:
        results = api.search(query)
        return results
    except Exception as e:
        return f"Search failed: {e}"
```

Good news: Agent sees error messages and can retry with different inputs!

### Issue 4: Agent Gives Up Too Early

**Symptoms:** Agent stops before completing task

**Cause:** System prompt might be too restrictive

**Solution:** Improve system prompt:
```python
agent = Agent(
    "bot",
    tools=[search],
    system_prompt="You are persistent. If a tool fails, try again with different inputs. Complete the task!"
)
```

---

## Advanced: How Tools Get Their Info

Ever wonder how tools know what the user asked?

You can access the full agent context inside tools using the `@xray` decorator:

```python
from connectonion.decorators import xray

@xray
def search(query: str) -> str:
    """Search for items."""

    # Access the original user request!
    print(f"User asked: {xray.task}")
    print(f"Current iteration: {xray.iteration}")
    print(f"Previous tools called: {xray.previous_tools}")

    return f"Results for {query}"

agent = Agent("bot", tools=[search])
agent.input("Find blue shirts and calculate 20% off")
```

This is super useful for debugging and understanding agent behavior!

---

## Next Steps

Now that you understand how agents work, explore more:

**Core Skills:**
- [Creating Custom Tools](Creating-Custom-Tools) - Build powerful, reusable tools
- [Interactive Debugging Guide](Interactive-Debugging-Guide) - Master `agent.auto_debug()`
- [Debug Agent Errors](How-To-Debug-Agent-Errors) - Fix common problems

**Real Examples:**
- [Email Agent Example](Examples-Email-Agent-Example) - Complete email automation
- [Web Scraping Agent](Examples-Web-Scraping-Agent) - Extract data from websites

**Production:**
- [Deploy to Production](How-To-Deploy-To-Production) - Best practices for production agents

**Reference:**
- [Official Agent Documentation](https://docs.connectonion.com/agent) - Complete API reference

---

## Summary: The Five Things to Remember

1. **Agents = LLM + Tools** - They think (LLM) and act (tools)
2. **Tools are functions** - Any Python function with a docstring works
3. **Agents decide** - You don't program the logic, the LLM figures it out
4. **Iteration loop** - Agents call tools multiple times until the task is done
5. **Error handling** - Tools should handle errors gracefully

---

## FAQ

**Q: How does the agent know when to stop?**
A: When the LLM decides the task is complete (no more tool calls needed) or max_iterations is reached.

**Q: Can I use async tools?**
A: Not yet, but it's on the roadmap! For now, tools run synchronously.

**Q: What if I don't want the agent to use a tool?**
A: Don't add it to the `tools` list! Only include tools the agent should access.

**Q: How much does running an agent cost?**
A: Cost = LLM API calls. Each iteration is one API call. Simple tasks (3-5 iterations) cost pennies. Use cheaper models like `o4-mini` for development.

**Q: Can tools call other tools?**
A: Tools run independently. If you need tool chaining, let the agent do it across iterations, or create a composite tool that calls multiple functions internally.

**Q: What's the difference between `Agent` and `llm_do`?**
A: `Agent` is for multi-step tasks with tools. `llm_do` is for single LLM calls without tools. Use `Agent` when you need the agent to take actions.

---

**Ready to build complex agents?** → Continue to [Creating Custom Tools](Creating-Custom-Tools)

---

*Keywords: python ai agent, ai agent tutorial, how ai agents work, llm agent python, autonomous agents python, python ai framework*

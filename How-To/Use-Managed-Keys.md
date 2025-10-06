# How to Use Managed AI Model Keys (No API Setup Required) | ConnectOnion

**Skip API key management completely. Authenticate once with `co auth`, then use any AI model from OpenAI, Google, or Anthropic with zero configuration. Perfect for getting started, prototyping, and small projects.**

## What You'll Learn

- How to authenticate and start using managed keys in 2 minutes
- Which models are available with managed keys
- When to use managed keys vs. your own API keys
- How to switch models and manage usage
- Troubleshooting common issues

## Quick Links

- [Jump to setup (2 minutes)](#2-minute-setup)
- [Jump to available models](#available-models)
- [Jump to code examples](#code-examples)
- [Jump to troubleshooting](#troubleshooting)

---

## What Are Managed Keys?

ConnectOnion can proxy your AI model requests through secure managed keys, so you don't need to:
- Sign up for OpenAI, Google, or Anthropic accounts
- Generate and manage multiple API keys
- Set environment variables
- Handle billing for each provider

**Instead:** Authenticate once with ConnectOnion, then use any model instantly.

---

## 2-Minute Setup

### Step 1: Authenticate

Run this command in your terminal:

```bash
co auth
```

**What happens:**
```
Opening browser for authentication...
✅ Authenticated successfully! Token saved to ~/.co/auth.json
📧 Your email: 0x1234abcd@mail.openonion.ai (activated)
🎁 Free tokens: 100,000 tokens to get started
```

### Step 2: Use Any Model

Add `co/` prefix to any model name:

```python
from connectonion import Agent

# ✅ Using managed keys (no API key needed!)
agent = Agent("assistant", model="co/gpt-5")
response = agent.input("Hello!")
print(response)
```

**Output:**
```
INPUT: Hello!

  Iteration 1/10
  → LLM Request (gpt-5)
  ← LLM Response (189ms)

✓ Complete (0.2s)

Hello! How can I help you today?
```

**That's it!** You're now using GPT-5 without an OpenAI API key.

---

##⭐ Bonus: Free Tokens

Star our GitHub repo for an extra 100K tokens:

👉 **[Star ConnectOnion on GitHub](https://github.com/wu-changxing/connectonion)** 👈

After starring, your token balance automatically increases by +100K tokens!

---

## Available Models

All these models work with `co/` prefix after authentication:

### OpenAI Models

```python
from connectonion import Agent

# GPT-5 series (recommended)
agent = Agent("bot", model="co/gpt-5")           # Best for coding & agents
agent = Agent("bot", model="co/gpt-5-mini")      # Faster, cost-efficient
agent = Agent("bot", model="co/gpt-5-nano")      # Fastest, cheapest

# GPT-4.1
agent = Agent("bot", model="co/gpt-4.1")         # Smartest non-reasoning model

# GPT-4o series (previous generation)
agent = Agent("bot", model="co/gpt-4o")          # Multimodal with vision
agent = Agent("bot", model="co/gpt-4o-mini")     # Affordable, fast

# o1 reasoning models
agent = Agent("bot", model="co/o1")              # Advanced reasoning
agent = Agent("bot", model="co/o1-mini")         # Fast reasoning
```

### Google Gemini Models

```python
# Gemini 2.5 (newest)
agent = Agent("bot", model="co/gemini-2.5-pro")  # Best for long context (2M tokens)

# Gemini 2.0
agent = Agent("bot", model="co/gemini-2.0-flash-exp")         # Experimental, fast
agent = Agent("bot", model="co/gemini-2.0-flash-thinking-exp") # With reasoning

# Gemini 1.5
agent = Agent("bot", model="co/gemini-1.5-pro")     # 2M token context
agent = Agent("bot", model="co/gemini-1.5-flash")   # Fast, 1M context
agent = Agent("bot", model="co/gemini-1.5-flash-8b") # High-volume, low cost
```

### Anthropic Claude Models

```python
# Claude Opus 4 series (newest)
agent = Agent("bot", model="co/claude-opus-4.1")  # Latest, most capable
agent = Agent("bot", model="co/claude-opus-4")    # Previous version

# Claude Sonnet 4
agent = Agent("bot", model="co/claude-sonnet-4")  # Balanced performance

# Claude 3.5 series (previous generation)
agent = Agent("bot", model="co/claude-3-5-sonnet") # Excellent at coding
agent = Agent("bot", model="co/claude-3-5-haiku")  # Fast, cost-effective
```

**Total: 16+ models across 3 providers** - all with zero setup!

---

## Managed Keys vs Your Own Keys

### When to Use Managed Keys (`co/` prefix)

✅ **Perfect for:**
- **Getting started** - No API key setup, just `co auth`
- **Prototyping** - Try different models quickly
- **Learning** - Focus on building, not configuration
- **Small projects** - Free tier covers experimentation
- **Model comparison** - Switch models with one line

**Example:**
```python
# Try different models instantly
for model in ["co/gpt-5", "co/claude-opus-4.1", "co/gemini-2.5-pro"]:
    agent = Agent("tester", model=model)
    print(f"{model}: {agent.input('Hello!')}")
```

### When to Use Your Own Keys (no prefix)

✅ **Perfect for:**
- **Production apps** - Direct billing with providers
- **High volume** - Lower cost at scale
- **Enterprise** - Existing API key infrastructure
- **Privacy** - Requests go directly to providers

**Example:**
```python
# Using your own OpenAI key
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

agent = Agent("bot", model="gpt-5")  # No co/ prefix
```

### Side-by-Side Comparison

| Feature | Managed Keys (`co/`) | Your Own Keys |
|---------|---------------------|---------------|
| **Setup** | `co auth` (2 minutes) | Get keys from 3 providers |
| **Models** | All providers instantly | Limited to your keys |
| **Cost** | Usage-based | Direct provider billing |
| **Best for** | Getting started, prototyping | Production, high-volume |
| **Free tier** | 100K tokens | No |

---

## Code Examples

### Example 1: Simple Agent

```python
from connectonion import Agent

# No API key setup needed!
agent = Agent(
    "assistant",
    model="co/gpt-5-mini"  # Fast and free to start
)

response = agent.input("Explain quantum computing in simple terms")
print(response)
```

**Expected Output:**
```
Quantum computing uses quantum bits (qubits) that can be both 0 and 1
simultaneously, allowing quantum computers to solve certain problems much
faster than classical computers...
```

### Example 2: Tool-Using Agent

```python
from connectonion import Agent

def search_web(query: str) -> str:
    """Search for information."""
    return f"Results for '{query}': ..."

agent = Agent(
    "researcher",
    model="co/gpt-5",  # Using managed keys
    tools=[search_web]
)

agent.input("Search for Python AI frameworks and summarize the top 3")
```

**What happens:**
1. Agent calls `search_web("Python AI frameworks")`
2. Agent summarizes results
3. Returns concise answer

### Example 3: Model Comparison

Compare responses from different providers:

```python
from connectonion import Agent

prompt = "Write a Python function to find prime numbers"

models = [
    "co/gpt-5",              # OpenAI
    "co/claude-opus-4.1",    # Anthropic
    "co/gemini-2.5-pro"      # Google
]

for model in models:
    agent = Agent("compare", model=model)
    print(f"\n{model}:")
    print(agent.input(prompt))
```

### Example 4: Switching Models Based on Task

```python
from connectonion import Agent

def get_agent_for_task(task_type: str):
    """Choose the best model for each task."""
    models = {
        "code": "co/gpt-5",                # Best for coding
        "analysis": "co/claude-opus-4.1",  # Strong reasoning
        "research": "co/gemini-2.5-pro"    # Long context
    }
    return Agent("helper", model=models.get(task_type, "co/gpt-5-mini"))

# Use different models for different tasks
code_agent = get_agent_for_task("code")
code_agent.input("Write a binary search function")

analysis_agent = get_agent_for_task("analysis")
analysis_agent.input("Analyze this data trend...")

research_agent = get_agent_for_task("research")
research_agent.input("Research the history of AI...")
```

---

## How It Works (Behind the Scenes)

Understanding the flow helps debug issues:

```
1. You run: co auth
   ↓
2. Browser opens to https://openonion.ai/auth
   ↓
3. You log in (GitHub/Google/Email)
   ↓
4. Token saved to ~/.co/auth.json
   ↓
5. You use co/ prefix in code
   ↓
6. ConnectOnion reads token from ~/.co/auth.json
   ↓
7. Request proxied through OpenOnion.ai
   ↓
8. Response returned to your code
```

**Security:**
- Token encrypted at rest
- Token expires after 30 days (auto-refreshes)
- No prompts/responses stored by default

---

## Common Use Cases

### Use Case 1: Learning AI Development

```python
# Day 1: Start with managed keys
agent = Agent("learner", model="co/gpt-5-mini")
agent.input("Hello!")

# Day 30: Switch to your own keys for production
agent = Agent("production", model="gpt-5")  # Uses OPENAI_API_KEY
```

### Use Case 2: Rapid Prototyping

```python
# Test idea quickly without API setup
agent = Agent("prototype", model="co/gpt-5")

def analyze(data: str) -> str:
    """Analyze data."""
    return f"Analysis: {data}"

agent.tools = [analyze]
agent.input("Analyze this dataset: ...")

# Works immediately - no keys, no config!
```

### Use Case 3: Teaching & Workshops

```python
# Students run co auth once, then:

def workshop_agent(student_name: str):
    """Each student gets a working agent instantly."""
    return Agent(
        student_name,
        model="co/gpt-5-mini",  # Free tier is enough
        tools=[search, calculate]
    )

# 30 students, zero API key management!
```

---

## Troubleshooting

### Issue 1: "Not authenticated" Error

**Symptoms:**
```
Error: Not authenticated. Please run 'co auth' first.
```

**Solutions:**
```bash
# Solution 1: Authenticate
co auth

# Solution 2: Check auth file exists
ls -la ~/.co/auth.json

# Solution 3: Re-authenticate if token expired
co auth
```

### Issue 2: "Token expired" Error

**Symptoms:**
```
Error: Authentication token has expired
```

**Solution:**
```bash
# Simply re-authenticate (takes 30 seconds)
co auth
```

Tokens expire after 30 days for security. Re-auth renews it.

### Issue 3: "Model not found" Error

**Symptoms:**
```
Error: Model 'co/gpt-6' not found
```

**Cause:** Typo in model name or unsupported model

**Solution:** Check [Available Models](#available-models) section for exact names:
```python
# ❌ Wrong
agent = Agent("bot", model="co/gpt-6")  # Doesn't exist

# ✅ Correct
agent = Agent("bot", model="co/gpt-5")
```

### Issue 4: Slow Responses

**Symptoms:** Requests take longer than expected

**Cause:** Proxying adds ~50-100ms latency

**Solutions:**
- **For development**: Managed keys are fine
- **For production**: Use your own keys for direct connection:
  ```python
  agent = Agent("bot", model="gpt-5")  # Direct to OpenAI
  ```

### Issue 5: Browser Doesn't Open

**Symptoms:** `co auth` doesn't open browser

**Solutions:**
```bash
# Get manual URL
co auth --no-browser

# Output:
# Visit: https://openonion.ai/auth?token=abc123...
# Then paste this URL in your browser
```

---

## Advanced Topics

### Fallback Strategy

Start with managed keys, fall back to own keys:

```python
import os
from connectonion import Agent

def create_agent(name: str):
    """Try managed keys, fall back to own."""
    try:
        # Try managed keys first
        return Agent(name, model="co/gpt-5")
    except Exception as e:
        if "not authenticated" in str(e):
            # Fall back to own key
            if os.getenv("OPENAI_API_KEY"):
                print("Using your own OpenAI key")
                return Agent(name, model="gpt-5")
            else:
                raise Exception("No keys available. Run 'co auth' or set OPENAI_API_KEY")
        raise

agent = create_agent("helper")
```

### Cost Tracking (Coming Soon)

```bash
# Check usage (feature coming soon)
co status

# Output:
# ✅ Authenticated as: user@example.com
# 📊 Usage today: 15,234 tokens ($0.31)
# 💳 Plan: Free tier (84,766 tokens remaining)
```

### Team Collaboration (Coming Soon)

Share managed keys across a team:

```bash
# Each team member authenticates once
co auth

# Everyone uses the same code
# Different users, but seamless collaboration
```

---

## Comparison with Other Frameworks

### ConnectOnion Managed Keys

```python
# 1. Authenticate once
co auth

# 2. Use any model
agent = Agent("bot", model="co/gpt-5")
agent.input("Hello!")
```

### LangChain (Traditional approach)

```python
# 1. Install
pip install langchain openai anthropic google-generativeai

# 2. Set multiple keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...

# 3. Create agent
from langchain import agents
agent = agents.initialize_agent(...)
```

**ConnectOnion advantage:** One command (`co auth`) vs managing 3+ API keys!

---

## Next Steps

Now that you know how to use managed keys:

**Explore Models:**
- [Models Documentation](https://docs.connectonion.com/models) - Complete model list
- Try different models with [Model Comparison Example](#example-3-model-comparison)

**Build Agents:**
- [Agent Core Concepts](../Tutorials/Agent-Core-Concepts) - How agents work
- [Creating Custom Tools](../Tutorials/Creating-Custom-Tools) - Add capabilities

**Production:**
- Learn when to switch to your own keys
- [Deploy to Production](Deploy-To-Production) - Production best practices

---

## Summary

**Managed Keys in 3 Points:**

1. **One-time setup**: `co auth` (2 minutes)
2. **Any model**: Add `co/` prefix → `model="co/gpt-5"`
3. **Zero configuration**: No API keys, no environment variables

**Perfect for:** Getting started, prototyping, learning, small projects

**When to switch to own keys:** Production, high-volume, direct billing preferred

---

## FAQ

**Q: Is this free?**
A: Yes! Free tier includes 100,000 tokens. ⭐ Star our repo for +100K bonus tokens.

**Q: Do I need accounts with OpenAI/Google/Anthropic?**
A: No! That's the whole point - manage keys manages everything.

**Q: Can I use managed keys AND my own keys in the same project?**
A: Yes! Mix and match:
```python
dev_agent = Agent("dev", model="co/gpt-5-mini")  # Managed
prod_agent = Agent("prod", model="gpt-5")        # Your key
```

**Q: What happens to my prompts?**
A: Proxied through OpenOnion servers but **not stored** by default. Privacy-focused.

**Q: Can my team share one account?**
A: Team features coming soon. For now, each developer needs their own `co auth`.

**Q: How do I check my token usage?**
A: `co status` command is coming soon. For now, check [dashboard.openonion.ai](https://dashboard.openonion.ai)

**Q: Can I use this in production?**
A: Yes, but for high-volume production, consider using your own API keys for direct billing and lower latency.

---

**Ready to start?** → Run `co auth` now and build your first agent!

---

*Keywords: ai model api keys, llm api management, openai api key setup, claude api authentication, managed api keys, ai development setup*

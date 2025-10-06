# ConnectOnion Wiki - Python AI Agent Framework

**Build powerful AI agents in Python with minimal code**

ConnectOnion is a lightweight Python framework for creating AI agents that can use tools, make decisions, and interact with the world. This wiki provides tutorials, examples, and guides to help you build amazing AI-powered applications.

## 🚀 Quick Links

### Getting Started
- **[Quick Start Guide](Quick-Start)** - Build your first agent in 5 minutes
- **[Building Your First Agent](Tutorials/Building-Your-First-Agent)** - Complete step-by-step tutorial
- **[Creating Custom Tools](Tutorials/Creating-Custom-Tools)** - Add capabilities to your agents

### Features & Guides
- **[Interactive Debugging Guide](Tutorials/Interactive-Debugging-Guide)** - Debug agents with `agent.auto_debug()`
- **[How to Use Auto-Debug](How-To/Use-Auto-Debug)** - Feature guide and examples
- **[Debug Agent Errors](How-To/Debug-Agent-Errors)** - Troubleshooting common issues

### Examples
- **[Email Agent Example](Examples/Email-Agent-Example)** - Search and send emails with AI
- **[Web Scraping Agent](Examples/Web-Scraping-Agent)** - Extract data from websites

### Reference
- **[FAQ](FAQ)** - Frequently asked questions
- **[Troubleshooting](Troubleshooting)** - Common errors and solutions

## 📖 What is ConnectOnion?

ConnectOnion helps you build AI agents that can:
- **Use tools** - Search, send emails, browse the web, run code
- **Make decisions** - Plan multi-step tasks and adapt to results
- **Debug easily** - Interactive debugging with `auto_debug()`
- **Scale simply** - From prototypes to production

### Simple Example

```python
from connectonion import Agent

def search_web(query: str) -> str:
    """Search the web and return results"""
    return f"Found information about {query}"

agent = Agent(
    name="assistant",
    tools=[search_web]
)

agent.input("Find information about Python AI frameworks")
```

That's it! The agent will use the LLM to decide when to call `search_web()` and process the results.

## 🎯 Why ConnectOnion?

**Keep Simple Things Simple**
- 2-line agent creation: `Agent("name").input("task")`
- Functions become tools automatically
- No complex configuration files

**Make Complicated Things Possible**
- Interactive debugging with `auto_debug()`
- Behavior tracking and logging
- Trust policies for security
- Multi-agent coordination (coming soon)

## 📚 Learning Path

**1. Beginner** (Start here!)
1. [Quick Start Guide](Quick-Start) - 5 minutes
2. [Building Your First Agent](Tutorials/Building-Your-First-Agent) - 15 minutes
3. [Email Agent Example](Examples/Email-Agent-Example) - Working code to study

**2. Intermediate**
1. [Creating Custom Tools](Tutorials/Creating-Custom-Tools)
2. [Interactive Debugging Guide](Tutorials/Interactive-Debugging-Guide)
3. [Debug Agent Errors](How-To/Debug-Agent-Errors)

**3. Advanced**
1. [Deploy to Production](How-To/Deploy-To-Production)
2. [Web Scraping Agent](Examples/Web-Scraping-Agent)
3. [Official Documentation](https://connectonion.com/docs) - Full API reference

## 🔗 Official Resources

- **Documentation**: [connectonion.com/docs](https://connectonion.com/docs)
- **GitHub**: [github.com/wu-changxing/connectonion](https://github.com/wu-changxing/connectonion)
- **PyPI**: [pypi.org/project/connectonion](https://pypi.org/project/connectonion)
- **Discord**: [Join our community](https://discord.gg/4xfD9k8AUF)

## 🆘 Need Help?

- Check the [FAQ](FAQ) for common questions
- Browse [Troubleshooting](Troubleshooting) for error solutions
- Ask in [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)
- Join our [Discord community](https://discord.gg/4xfD9k8AUF)

## 📝 Contributing

Found an error? Want to add a tutorial?
- Edit pages on [GitHub](https://github.com/wu-changxing/connectonion/tree/main/wiki)
- Open an [issue](https://github.com/wu-changxing/connectonion/issues)
- Join the discussion on [Discord](https://discord.gg/4xfD9k8AUF)

---

**Ready to build your first AI agent?** → Start with the [Quick Start Guide](Quick-Start)

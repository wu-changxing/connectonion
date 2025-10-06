# Tutorial: Creating Custom Tools for AI Agents

Learn how to create powerful custom tools for your AI agents. This tutorial covers everything from simple functions to advanced patterns with error handling, validation, and real API integrations.

## What You'll Learn

- How to turn any Python function into an agent tool
- Best practices for tool design and documentation
- Error handling and validation patterns
- Real-world API integrations
- Advanced tool patterns (caching, retries, etc.)

**Time**: 15 minutes
**Level**: Intermediate
**Prerequisites**: [Building Your First Agent](Building-Your-First-Agent)

## The Basics: Functions as Tools

In ConnectOnion, **tools are just Python functions**. The agent uses your function's signature and docstring to understand how to use it.

### Simple Tool Example

```python
from connectonion import Agent

def get_weather(city: str) -> str:
    """
    Get current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Weather information as a string
    """
    # Your weather API logic here
    return f"Weather in {city}: 72°F, Sunny"

agent = Agent("weather-bot", tools=[get_weather])
agent.input("What's the weather in Tokyo?")
```

**That's it!** The agent now knows:
- Function name: `get_weather`
- What it does: from the docstring
- Parameters: `city` (string)
- What it returns: string

## Tool Design Best Practices

### 1. Write Clear Docstrings

**Bad:**
```python
def search(q):
    """Searches"""
    return results
```

**Good:**
```python
def search_web(query: str) -> str:
    """
    Search the web for information on a topic.

    Use this when the user asks for current information, facts,
    or needs to find something online.

    Args:
        query: The search query (e.g., "Python tutorials")

    Returns:
        Search results as formatted text
    """
    return results
```

**Why it matters:** The LLM reads your docstring to decide when and how to call the tool!

### 2. Use Type Hints

```python
# Bad - agent doesn't know types
def calculate(a, b):
    return a + b

# Good - clear types
def calculate(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

# Even better - with validation
def calculate(a: float, b: float, operation: str = "add") -> float:
    """
    Perform a mathematical operation.

    Args:
        a: First number
        b: Second number
        operation: One of: add, subtract, multiply, divide

    Returns:
        Result of the calculation
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    # ... etc
```

### 3. Return Strings (Usually)

Agents work best with string results:

```python
# Good - returns string
def get_user(user_id: int) -> str:
    user = database.get(user_id)
    return f"User: {user.name}, Email: {user.email}, Role: {user.role}"

# Also fine - will be converted to string
def get_user_count() -> int:
    return database.count()

# Avoid - hard for LLM to interpret
def get_user(user_id: int) -> dict:
    return {"name": "John", "email": "john@example.com", "roles": [...]}
```

If you must return structured data, format it clearly:

```python
def get_user(user_id: int) -> str:
    user = database.get(user_id)
    return f"""
User Information:
- Name: {user.name}
- Email: {user.email}
- Roles: {', '.join(user.roles)}
- Last Active: {user.last_active}
"""
```

## Error Handling Patterns

### Pattern 1: Return Error Messages (Recommended)

```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    try:
        # Validate
        if "@" not in to:
            return f"Error: Invalid email address '{to}'"

        if not subject or not body:
            return "Error: Email must have subject and body"

        # Send email
        smtp.send(to, subject, body)
        return f"✓ Successfully sent email to {to}"

    except smtplib.SMTPException as e:
        return f"Error sending email: {str(e)}"
```

**Why this works:** The agent sees the error message and can:
- Try again with corrected parameters
- Ask the user for clarification
- Choose a different approach

### Pattern 2: Graceful Degradation

```python
def search_database(query: str) -> str:
    """Search the database for records"""
    try:
        results = db.search(query)
        if not results:
            return f"No results found for '{query}'. Try:\n- Broader search terms\n- Check spelling\n- Use keywords instead of full sentences"
        return format_results(results)

    except DatabaseConnectionError:
        return "Database temporarily unavailable. Please try again in a moment."

    except Exception as e:
        return f"Search failed: {str(e)}. Please rephrase your query."
```

### Pattern 3: Input Validation

```python
def calculate_percentage(value: float, total: float) -> str:
    """Calculate what percentage 'value' is of 'total'"""

    # Validate inputs
    if total == 0:
        return "Error: Cannot calculate percentage of zero"

    if value < 0 or total < 0:
        return "Error: Negative numbers not supported"

    # Calculate
    percentage = (value / total) * 100
    return f"{value} is {percentage:.2f}% of {total}"
```

## Real-World API Integrations

### Example: Weather API Tool

```python
import requests
from typing import Optional

def get_weather(
    city: str,
    country_code: Optional[str] = None,
    units: str = "metric"
) -> str:
    """
    Get current weather for a city using OpenWeatherMap API.

    Args:
        city: City name (e.g., "Tokyo", "New York")
        country_code: Optional 2-letter country code (e.g., "JP", "US")
        units: Temperature units - "metric" (Celsius) or "imperial" (Fahrenheit)

    Returns:
        Current weather information
    """
    try:
        # Build query
        location = f"{city},{country_code}" if country_code else city

        # Call API
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": api_key, "units": units}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Parse response
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        unit_symbol = "°C" if units == "metric" else "°F"

        return f"""
Weather in {city}:
- Temperature: {temp}{unit_symbol}
- Conditions: {description}
- Humidity: {humidity}%
"""

    except requests.exceptions.Timeout:
        return f"Weather service timed out for {city}. Please try again."

    except requests.exceptions.RequestException as e:
        return f"Could not get weather for {city}: {str(e)}"

    except KeyError:
        return f"City '{city}' not found. Please check the spelling or try adding a country code."
```

### Example: GitHub API Tool

```python
import requests
from typing import Optional

def search_github_repos(
    query: str,
    language: Optional[str] = None,
    sort: str = "stars",
    max_results: int = 5
) -> str:
    """
    Search GitHub repositories.

    Args:
        query: Search query (e.g., "machine learning")
        language: Filter by programming language (e.g., "python", "javascript")
        sort: Sort by "stars", "forks", or "updated"
        max_results: Maximum number of results (1-10)

    Returns:
        List of matching repositories with details
    """
    try:
        # Build search query
        q = query
        if language:
            q += f" language:{language}"

        # Call GitHub API
        url = "https://api.github.com/search/repositories"
        headers = {"Accept": "application/vnd.github.v3+json"}
        params = {"q": q, "sort": sort, "per_page": min(max_results, 10)}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        # Format results
        data = response.json()
        repos = data.get("items", [])

        if not repos:
            return f"No repositories found for '{query}'"

        results = [f"Found {len(repos)} repositories:\n"]

        for i, repo in enumerate(repos, 1):
            results.append(f"""
{i}. {repo['name']} by {repo['owner']['login']}
   ⭐ {repo['stargazers_count']} stars | 🍴 {repo['forks_count']} forks
   {repo['description'] or 'No description'}
   URL: {repo['html_url']}
""")

        return "\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"GitHub search failed: {str(e)}"
```

## Advanced Tool Patterns

### Pattern 1: Caching for Performance

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def search_expensive_api(query: str) -> str:
    """
    Search an expensive/slow API (results cached).

    Args:
        query: Search query

    Returns:
        Search results
    """
    # Simulate slow API call
    time.sleep(2)
    return f"Results for: {query}"

# First call takes 2 seconds
# Subsequent calls with same query are instant!
```

### Pattern 2: Retry with Backoff

```python
import time
from typing import Optional

def fetch_data_with_retry(
    url: str,
    max_retries: int = 3
) -> str:
    """
    Fetch data from URL with automatic retries.

    Args:
        url: URL to fetch
        max_retries: Maximum retry attempts

    Returns:
        Response data or error message
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                return f"Failed after {max_retries} attempts: {str(e)}"
```

### Pattern 3: Structured Output

```python
def analyze_text(text: str) -> str:
    """
    Analyze text and return structured insights.

    Args:
        text: Text to analyze

    Returns:
        Analysis results in structured format
    """
    word_count = len(text.split())
    char_count = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')

    return f"""
TEXT ANALYSIS
═══════════════
Statistics:
  - Words: {word_count}
  - Characters: {char_count}
  - Sentences: {sentences}
  - Avg words/sentence: {word_count / max(sentences, 1):.1f}

Readability:
  - {"Easy" if word_count / max(sentences, 1) < 15 else "Complex"}

Recommendations:
  - {get_recommendations(word_count, sentences)}
"""
```

### Pattern 4: Multi-Step Tools

```python
def research_and_summarize(topic: str) -> str:
    """
    Research a topic and provide a summary.

    This tool combines multiple steps:
    1. Search for information
    2. Analyze relevance
    3. Summarize findings

    Args:
        topic: Topic to research

    Returns:
        Research summary
    """
    # Step 1: Search
    search_results = search_web(topic)

    if "Error" in search_results:
        return search_results

    # Step 2: Extract key information
    key_points = extract_key_points(search_results)

    # Step 3: Summarize
    summary = f"""
RESEARCH: {topic}
═══════════════

Key Findings:
{format_points(key_points)}

Sources: [List of sources]

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

    return summary
```

## Testing Your Tools

### Test Tools Independently

```python
def search_web(query: str) -> str:
    """Search the web"""
    # Implementation

# Test without agent
if __name__ == "__main__":
    # Test normal case
    result = search_web("Python tutorials")
    print(result)

    # Test edge cases
    print(search_web(""))  # Empty query
    print(search_web("a" * 1000))  # Very long query
```

### Test with Agent

```python
from connectonion import Agent

# Create test agent
agent = Agent("test", tools=[search_web, get_weather])

# Test scenarios
test_queries = [
    "What's the weather in Tokyo?",
    "Search for Python tutorials",
    "Get weather for a city that doesn't exist",
]

for query in test_queries:
    print(f"\nTest: {query}")
    agent.input(query)
```

## Common Patterns Library

### File Operations

```python
def read_file(filepath: str) -> str:
    """Read contents of a file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"✓ Wrote {len(content)} characters to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"
```

### Database Operations

```python
def query_database(sql: str) -> str:
    """Execute SQL query (SELECT only)"""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries allowed"

    try:
        results = db.execute(sql)
        return format_table(results)
    except Exception as e:
        return f"Query failed: {str(e)}"
```

### Web Scraping

```python
def scrape_webpage(url: str) -> str:
    """Extract text content from a webpage"""
    try:
        from bs4 import BeautifulSoup
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text
        text = soup.get_text(separator='\n', strip=True)
        return text[:5000]  # Limit to 5000 chars

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
```

## Next Steps

**Practice with Examples:**
- [Email Agent Example](../Examples/Email-Agent-Example) - See real tools in action
- [Web Scraping Agent](../Examples/Web-Scraping-Agent) - Advanced tool patterns

**Debug Your Tools:**
- [Interactive Debugging Guide](Interactive-Debugging-Guide) - Test tools with `auto_debug()`
- [Debug Agent Errors](../How-To/Debug-Agent-Errors) - Fix common issues

**Deploy:**
- [Deploy to Production](../How-To/Deploy-To-Production) - Production considerations

## Summary

**Key Takeaways:**
1. Tools are just Python functions with good docstrings
2. Return error messages as strings - let the agent adapt
3. Validate inputs and handle errors gracefully
4. Use type hints for clear parameter types
5. Test tools independently before adding to agents

**Tool Design Checklist:**
- ✓ Clear, descriptive function name
- ✓ Comprehensive docstring with Args and Returns
- ✓ Type hints on all parameters
- ✓ Error handling with helpful messages
- ✓ Input validation
- ✓ Returns string (or easily stringified type)

---

**Next Tutorial:** [Interactive Debugging Guide](Interactive-Debugging-Guide)

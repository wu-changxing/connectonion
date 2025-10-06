# How-To: Deploy AI Agents to Production

Best practices for deploying ConnectOnion agents to production environments. Learn how to handle secrets, optimize performance, monitor agents, and ensure reliability.

## Production Checklist

Before deploying to production:

- [ ] Remove or disable `auto_debug()` calls
- [ ] Use environment variables for API keys
- [ ] Add error handling and logging
- [ ] Set appropriate timeouts
- [ ] Implement rate limiting
- [ ] Add monitoring and alerting
- [ ] Test with production data
- [ ] Document agent behavior
- [ ] Set up backup/failover
- [ ] Review security considerations

---

## Environment Configuration

### Use Environment Variables

**❌ Never in production:**
```python
# NEVER hardcode API keys!
agent = Agent("assistant")
os.environ["OPENAI_API_KEY"] = "sk-abc123..."  # DON'T DO THIS
```

**✅ Production approach:**
```python
# Load from environment
import os

# Verify key exists
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")

agent = Agent("assistant")
```

### Environment Files

**Development (`.env`):**
```bash
# .env - NOT committed to git
OPENAI_API_KEY=sk-dev-key-here
ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
```

**Production (system environment):**
```bash
# Set via deployment platform (Heroku, AWS, etc.)
OPENAI_API_KEY=sk-prod-key-here
ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

### Multi-Environment Setup

```python
import os
from dotenv import load_dotenv

# Load .env only in development
if os.getenv("ENV") != "production":
    load_dotenv()

# Configuration based on environment
class Config:
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "60"))

# Use in your code
agent = Agent(
    "assistant",
    model=os.getenv("MODEL", "gpt-4o-mini")
)
```

---

## Remove Debug Code

### Disable auto_debug()

```python
import os

agent = Agent("assistant", tools=[...])

# Only debug in development
if os.getenv("ENV") == "development":
    agent.auto_debug()

agent.input(task)
```

### Remove @xray Decorators (Optional)

```python
# Development version
from connectonion.decorators import xray

@xray  # Remove for production
def process_payment(amount: float):
    pass

# Production version
def process_payment(amount: float):
    # @xray removed - less overhead
    pass
```

**Note:** You can keep `@xray` in production for enhanced logging without `auto_debug()`.

---

## Error Handling and Resilience

### Wrap Agent Calls

```python
def run_agent_task(task: str, max_retries: int = 3):
    """
    Run agent task with retries and error handling.
    """
    for attempt in range(max_retries):
        try:
            result = agent.input(task)
            return {"success": True, "result": result}

        except openai.RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            return {"success": False, "error": "Rate limit exceeded"}

        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return {"success": False, "error": str(e)}

        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
            return {"success": False, "error": "Internal error"}

    return {"success": False, "error": "Max retries exceeded"}
```

### Tool-Level Error Handling

```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send email with comprehensive error handling"""
    try:
        # Validate inputs
        if "@" not in to:
            return f"Error: Invalid email '{to}'"

        # Attempt to send
        smtp.send(to, subject, body)

        # Log success
        logging.info(f"Email sent to {to}")
        return f"✓ Email sent to {to}"

    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed")
        return "Error: Email server authentication failed"

    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")
        return f"Error: Could not send email - {str(e)}"

    except Exception as e:
        logging.error(f"Unexpected email error: {e}", exc_info=True)
        return "Error: Email system unavailable"
```

---

## Logging and Monitoring

### Production Logging

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Log agent activities
def run_task(task: str):
    logger.info(f"Starting task: {task}")

    try:
        result = agent.input(task)
        logger.info(f"Task completed: {task[:50]}...")
        return result

    except Exception as e:
        logger.error(f"Task failed: {task}", exc_info=True)
        raise
```

### Structured Logging (JSON)

```python
import json
import logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Use JSON logging
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
```

### Monitor Agent Performance

```python
import time

def track_agent_performance(task: str):
    """Track and log agent performance metrics"""
    start_time = time.time()

    try:
        result = agent.input(task)
        duration = time.time() - start_time

        # Log metrics
        logger.info(json.dumps({
            "event": "agent_task_completed",
            "task": task[:100],
            "duration_seconds": duration,
            "success": True
        }))

        return result

    except Exception as e:
        duration = time.time() - start_time

        logger.error(json.dumps({
            "event": "agent_task_failed",
            "task": task[:100],
            "duration_seconds": duration,
            "error": str(e)
        }))

        raise
```

---

## Performance Optimization

### Use Fast Models

```python
# Production - optimize for cost and speed
agent = Agent(
    "assistant",
    model="gpt-4o-mini",  # 60x cheaper, 2x faster than gpt-4
    tools=[...]
)

# Reserve expensive models for complex tasks
def handle_complex_task(task: str):
    advanced_agent = Agent(
        "advanced",
        model="gpt-4o",  # Use when needed
        tools=[...]
    )
    return advanced_agent.input(task)
```

### Cache Results

```python
from functools import lru_cache
import hashlib

# Cache function results
@lru_cache(maxsize=1000)
def expensive_api_call(query: str) -> str:
    """Cached for 1000 unique queries"""
    result = api.search(query)
    return result

# Cache with custom TTL (using Redis, Memcached, etc.)
import redis
cache = redis.Redis(host='localhost')

def cached_search(query: str, ttl: int = 3600) -> str:
    """Cache results for 1 hour"""
    cache_key = f"search:{hashlib.md5(query.encode()).hexdigest()}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached.decode()

    # Call API and cache
    result = api.search(query)
    cache.setex(cache_key, ttl, result)
    return result
```

### Set Timeouts

```python
def run_with_timeout(task: str, timeout: int = 60):
    """Run agent with timeout"""
    import signal

    class TimeoutError(Exception):
        pass

    def timeout_handler(signum, frame):
        raise TimeoutError("Agent execution timed out")

    # Set timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        result = agent.input(task)
        signal.alarm(0)  # Cancel timeout
        return result

    except TimeoutError:
        logging.error(f"Task timed out after {timeout}s: {task}")
        raise
```

---

## Security Considerations

### Input Validation

```python
def sanitize_user_input(user_input: str) -> str:
    """Sanitize user input before passing to agent"""

    # Limit length
    if len(user_input) > 10000:
        raise ValueError("Input too long (max 10000 characters)")

    # Remove potentially dangerous content
    blocked_patterns = [
        "ignore previous instructions",
        "disregard all",
        "<script>",
        "DROP TABLE",
    ]

    for pattern in blocked_patterns:
        if pattern.lower() in user_input.lower():
            raise ValueError("Input contains blocked content")

    return user_input

# Use in production
user_task = sanitize_user_input(request.POST["task"])
result = agent.input(user_task)
```

### Tool Permissions

```python
# Restrict dangerous operations in production
def delete_file(filepath: str) -> str:
    """Delete a file (RESTRICTED IN PRODUCTION)"""

    # Production safety check
    if os.getenv("ENV") == "production":
        return "Error: File deletion disabled in production"

    # Development only
    os.remove(filepath)
    return f"Deleted {filepath}"
```

### Rate Limiting

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = {}

    def allow_request(self, user_id: str) -> bool:
        now = datetime.now()

        # Clean old requests
        if user_id in self.requests:
            self.requests[user_id] = [
                req for req in self.requests[user_id]
                if now - req < self.window
            ]

        # Check limit
        if user_id not in self.requests:
            self.requests[user_id] = []

        if len(self.requests[user_id]) >= self.max_requests:
            return False

        # Allow request
        self.requests[user_id].append(now)
        return True

# Use rate limiter
limiter = RateLimiter(max_requests=10, window_seconds=60)

def handle_request(user_id: str, task: str):
    if not limiter.allow_request(user_id):
        raise Exception("Rate limit exceeded. Try again later.")

    return agent.input(task)
```

---

## Deployment Platforms

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Set environment
ENV ENV=production
ENV PYTHONUNBUFFERED=1

# Run app
CMD ["python", "app.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  agent-service:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENV=production
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

### AWS Lambda

```python
# lambda_handler.py
import json
from connectonion import Agent

# Initialize agent outside handler (cold start optimization)
agent = Agent("assistant", tools=[...])

def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        task = event.get("task", "")
        result = agent.input(task)

        return {
            "statusCode": 200,
            "body": json.dumps({"result": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
```

### Heroku

```yaml
# Procfile
web: gunicorn app:app

# runtime.txt
python-3.9.16
```

```bash
# Deploy
heroku create my-agent-app
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

---

## Monitoring and Alerting

### Health Checks

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test agent
        test_result = agent.input("test")

        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
```

### Error Alerting

```python
import requests

def send_alert(message: str, severity: str = "error"):
    """Send alert to monitoring service (Slack, PagerDuty, etc.)"""

    # Slack webhook example
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    payload = {
        "text": f"[{severity.upper()}] Agent Error",
        "attachments": [{
            "text": message,
            "color": "danger" if severity == "error" else "warning"
        }]
    }

    requests.post(webhook_url, json=payload)

# Use in error handling
try:
    result = agent.input(task)
except Exception as e:
    send_alert(f"Agent failed: {str(e)}", severity="error")
    raise
```

---

## Best Practices Summary

**DO:**
- ✅ Use environment variables for secrets
- ✅ Add comprehensive error handling
- ✅ Implement logging and monitoring
- ✅ Set timeouts and rate limits
- ✅ Cache expensive operations
- ✅ Test with production-like data
- ✅ Use fast/cheap models when possible
- ✅ Sanitize user inputs
- ✅ Monitor performance metrics

**DON'T:**
- ❌ Hardcode API keys
- ❌ Deploy with `auto_debug()` enabled
- ❌ Skip error handling
- ❌ Ignore performance optimization
- ❌ Trust user input blindly
- ❌ Use expensive models unnecessarily
- ❌ Deploy without monitoring
- ❌ Forget to set timeouts

---

## Next Steps

- **Monitoring:** Set up dashboards (Grafana, Datadog, etc.)
- **Scaling:** Consider load balancing for high traffic
- **Security:** Regular security audits and updates
- **Documentation:** Document agent behavior and limitations

**Related Guides:**
- [Debug Agent Errors](Debug-Agent-Errors) - Fix production issues
- [Creating Custom Tools](../Tutorials/Creating-Custom-Tools) - Production-ready tools
- [Use Auto-Debug](Use-Auto-Debug) - Debug in development

---

**Need Help?**
- [Discord Community](https://discord.gg/4xfD9k8AUF)
- [GitHub Discussions](https://github.com/wu-changxing/connectonion/discussions)
- [Official Documentation](https://connectonion.com/docs)

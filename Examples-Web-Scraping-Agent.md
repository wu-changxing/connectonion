# Example: Web Scraping Agent - Extract Data from Websites with AI

A complete example of an AI agent that can scrape websites, extract structured data, and analyze content. Learn how to build intelligent web scrapers with ConnectOnion.

## What This Agent Does

The Web Scraping Agent can:
- Fetch and parse HTML from any URL
- Extract specific information (prices, titles, dates, etc.)
- Search for elements using CSS selectors or XPath
- Handle errors and rate limiting
- Analyze and summarize web content

**Technologies used:**
- ConnectOnion for the agent framework
- BeautifulSoup4 for HTML parsing
- Requests for HTTP requests
- lxml for advanced parsing

## Complete Code

```python
from connectonion import Agent
from connectonion.decorators import xray
import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
from urllib.parse import urljoin, urlparse

# Rate limiting
last_request_time = {}
MIN_REQUEST_INTERVAL = 1.0  # seconds

def rate_limit(url: str):
    """Enforce rate limiting per domain"""
    domain = urlparse(url).netloc
    current_time = time.time()

    if domain in last_request_time:
        elapsed = current_time - last_request_time[domain]
        if elapsed < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    last_request_time[domain] = time.time()

@xray  # Debug scraping issues
def fetch_webpage(url: str) -> str:
    """
    Fetch HTML content from a URL.

    Args:
        url: Web page URL (e.g., "https://example.com")

    Returns:
        HTML content as text or error message
    """
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return f"Error: URL must start with http:// or https://"

        # Rate limiting
        rate_limit(url)

        # Fetch page
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; ConnectOnion/1.0)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Return HTML
        return response.text

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out"

    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {str(e)}"

@xray
def extract_text(html: str, css_selector: Optional[str] = None) -> str:
    """
    Extract text content from HTML.

    Args:
        html: HTML content
        css_selector: Optional CSS selector to target specific elements
                     (e.g., "h1", ".article-title", "#main-content")

    Returns:
        Extracted text content
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Extract from specific elements if selector provided
        if css_selector:
            elements = soup.select(css_selector)
            if not elements:
                return f"No elements found matching '{css_selector}'"

            texts = [elem.get_text(strip=True) for elem in elements]
            return "\n\n".join(texts)

        # Otherwise, extract all text
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)

        # Limit length
        if len(text) > 5000:
            text = text[:5000] + "\n... (truncated)"

        return text

    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_links(html: str, base_url: str) -> str:
    """
    Extract all links from HTML.

    Args:
        html: HTML content
        base_url: Base URL to resolve relative links

    Returns:
        List of links found
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative to absolute URL
            absolute_url = urljoin(base_url, href)
            link_text = link.get_text(strip=True)

            links.append(f"- {link_text or '(no text)'}: {absolute_url}")

        if not links:
            return "No links found"

        # Limit to first 20 links
        result = "\n".join(links[:20])
        if len(links) > 20:
            result += f"\n... and {len(links) - 20} more links"

        return result

    except Exception as e:
        return f"Error extracting links: {str(e)}"

def find_elements(
    html: str,
    element_type: str,
    limit: int = 10
) -> str:
    """
    Find specific elements in HTML.

    Args:
        html: HTML content
        element_type: Element to find (e.g., "h1", "img", "table")
        limit: Maximum number of elements to return

    Returns:
        List of found elements with their content/attributes
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all(element_type, limit=limit)

        if not elements:
            return f"No <{element_type}> elements found"

        results = []
        for i, elem in enumerate(elements, 1):
            # Format based on element type
            if element_type == 'img':
                src = elem.get('src', 'no src')
                alt = elem.get('alt', 'no alt text')
                results.append(f"{i}. {alt}: {src}")

            elif element_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = elem.get_text(strip=True)
                results.append(f"{i}. {text}")

            elif element_type == 'table':
                # Extract table summary
                rows = elem.find_all('tr')
                results.append(f"{i}. Table with {len(rows)} rows")

            else:
                text = elem.get_text(strip=True)[:100]
                results.append(f"{i}. {text}...")

        return "\n".join(results)

    except Exception as e:
        return f"Error finding elements: {str(e)}"

def extract_structured_data(html: str, data_type: str) -> str:
    """
    Extract structured data from HTML.

    Args:
        html: HTML content
        data_type: Type of data to extract ("prices", "dates", "emails", "phones")

    Returns:
        Extracted structured data
    """
    import re

    try:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        if data_type == "prices":
            # Find price patterns
            prices = re.findall(r'\$[\d,]+\.?\d*', text)
            return "Prices found:\n" + "\n".join(set(prices)) if prices else "No prices found"

        elif data_type == "emails":
            # Find email patterns
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            return "Emails found:\n" + "\n".join(set(emails)) if emails else "No emails found"

        elif data_type == "phones":
            # Find phone patterns
            phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text)
            formatted = ['-'.join(filter(None, p)) for p in phones]
            return "Phone numbers found:\n" + "\n".join(set(formatted)) if formatted else "No phone numbers found"

        elif data_type == "dates":
            # Find date patterns
            dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
            return "Dates found:\n" + "\n".join(set(dates)) if dates else "No dates found"

        else:
            return f"Unknown data type: {data_type}. Use: prices, emails, phones, dates"

    except Exception as e:
        return f"Error extracting {data_type}: {str(e)}"

# Create the Web Scraping Agent
scraper_agent = Agent(
    name="web-scraper",
    tools=[
        fetch_webpage,
        extract_text,
        extract_links,
        find_elements,
        extract_structured_data
    ],
    system_prompt="""You are a web scraping assistant that helps extract information from websites.

Your capabilities:
- Fetch web pages and extract content
- Find specific elements using CSS selectors
- Extract structured data (prices, emails, dates, etc.)
- Extract all links from a page
- Search for specific HTML elements

Best practices:
- Always fetch the page first before extracting data
- Use CSS selectors for precise extraction
- Respect rate limits (1 request per second per domain)
- Provide clear summaries of extracted data

When asked to scrape:
1. Fetch the webpage
2. Extract relevant information using appropriate tools
3. Format the results clearly

Be helpful and accurate with web scraping tasks.""",
    model="gpt-4o-mini"
)

# Example usage
if __name__ == "__main__":
    # Example 1: Simple page scraping
    print("=== Example 1: Fetch and extract text ===")
    scraper_agent.input("Fetch https://example.com and extract all text")

    # Example 2: Find specific elements
    print("\n=== Example 2: Find specific elements ===")
    scraper_agent.input("Go to https://news.ycombinator.com and find all headlines")

    # Example 3: Extract structured data
    print("\n=== Example 3: Extract structured data ===")
    scraper_agent.input("Scrape https://example-shop.com and find all prices")
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install connectonion beautifulsoup4 requests lxml
```

### 2. Set OpenAI API Key

```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 3. Run the Agent

```bash
python web_scraper.py
```

## Usage Examples

### Example 1: Extract All Text

```python
scraper_agent.input("Fetch the content from https://example.com and extract all text")
```

**What happens:**
1. Agent calls `fetch_webpage("https://example.com")`
2. Agent calls `extract_text(html)`
3. Returns clean text content

### Example 2: Find Specific Elements

```python
scraper_agent.input("Go to https://news.ycombinator.com and extract all article titles")
```

**What happens:**
1. Fetches the page
2. Uses `find_elements(html, "a")` or CSS selector
3. Returns list of titles

### Example 3: Extract Prices

```python
scraper_agent.input("Scrape https://amazon.com/product/B123 and find the price")
```

**What happens:**
1. Fetches product page
2. Uses `extract_structured_data(html, "prices")`
3. Returns extracted prices

### Example 4: Get All Links

```python
scraper_agent.input("Get all links from https://python.org")
```

**What happens:**
1. Fetches page
2. Uses `extract_links(html, base_url)`
3. Returns list of absolute URLs

### Example 5: Advanced CSS Selectors

```python
scraper_agent.input("Fetch GitHub trending page and extract repository names using CSS selector '.repo-list .h3'")
```

## Advanced Features

### Custom Parsing Logic

```python
def extract_product_info(html: str) -> str:
    """Extract product information from e-commerce pages"""
    soup = BeautifulSoup(html, 'html.parser')

    try:
        title = soup.select_one('.product-title').text.strip()
        price = soup.select_one('.product-price').text.strip()
        description = soup.select_one('.product-description').text.strip()
        rating = soup.select_one('.star-rating')['data-rating']

        return f"""
Product Information:
  Title: {title}
  Price: {price}
  Rating: {rating}/5
  Description: {description[:200]}...
"""
    except Exception as e:
        return f"Error extracting product info: {e}"
```

### Handle JavaScript-Rendered Sites

For sites that use JavaScript, use Selenium:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def fetch_dynamic_page(url: str) -> str:
    """Fetch page rendered with JavaScript"""
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(2)  # Wait for JS to load
        html = driver.page_source
        return html
    finally:
        driver.quit()
```

### Add Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_fetch(url: str) -> str:
    """Cache fetched pages"""
    return fetch_webpage(url)
```

### Export to CSV/JSON

```python
import csv
import json

def export_to_csv(data: list, filename: str) -> str:
    """Export scraped data to CSV"""
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        return f"✓ Data exported to {filename}"
    except Exception as e:
        return f"Error exporting: {e}"

def export_to_json(data: dict, filename: str) -> str:
    """Export scraped data to JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return f"✓ Data exported to {filename}"
    except Exception as e:
        return f"Error exporting: {e}"
```

## Debugging

Enable interactive debugging to troubleshoot scraping:

```python
scraper_agent.auto_debug()
scraper_agent.input("Scrape prices from https://example.com")

# When agent pauses:
# > Press 'v' to view trace
# > Press 'e' to inspect HTML content
# > Press 'a' to ask AI why extraction failed
```

## Best Practices

### 1. Respect robots.txt

```python
from urllib.robotparser import RobotFileParser

def check_robots_txt(url: str) -> bool:
    """Check if scraping is allowed"""
    rp = RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))
    rp.read()
    return rp.can_fetch('*', url)
```

### 2. Add User-Agent

```python
headers = {
    'User-Agent': 'MyBot/1.0 (+https://mywebsite.com/bot-info)'
}
```

### 3. Handle Errors Gracefully

```python
def fetch_webpage(url: str) -> str:
    try:
        # Attempt to fetch
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "Error: Page not found (404)"
        elif e.response.status_code == 403:
            return "Error: Access forbidden (403)"
        else:
            return f"Error: HTTP {e.response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 4. Rate Limiting

Always implement rate limiting to avoid overwhelming servers:

```python
time.sleep(1)  # Wait 1 second between requests
```

### 5. CSS Selector Reference

Common patterns:
- `h1` - All h1 elements
- `.class-name` - Elements with class
- `#id-name` - Element with ID
- `div.article` - Div with class article
- `ul > li` - Direct children
- `a[href*="github"]` - Links containing "github"

## Legal and Ethical Considerations

### Always Check:
- ✅ Website's Terms of Service
- ✅ robots.txt file
- ✅ Rate limiting policies
- ✅ Copyright restrictions

### Don't:
- ❌ Scrape copyrighted content without permission
- ❌ Overwhelm servers with requests
- ❌ Ignore robots.txt
- ❌ Scrape personal data without consent

### Do:
- ✓ Respect rate limits
- ✓ Add proper User-Agent
- ✓ Cache responses
- ✓ Only scrape public data

## Common Issues

### Issue: "403 Forbidden"

**Solutions:**
- Add proper User-Agent header
- Check robots.txt
- Respect rate limits
- Some sites block bots entirely

### Issue: "Empty results"

**Solutions:**
- Page might use JavaScript (use Selenium)
- Wrong CSS selector
- Content inside iframe
- Enable debug mode to inspect HTML

### Issue: "Timeout errors"

**Solutions:**
- Increase timeout: `requests.get(url, timeout=30)`
- Check internet connection
- Site might be slow

## Next Steps

**Enhance This Example:**
- Add Selenium for JavaScript sites
- Implement data persistence (database)
- Add scheduling (scrape periodically)
- Create data visualization

**Learn More:**
- [Creating Custom Tools](Tutorials-Creating-Custom-Tools)
- [Deploy to Production](How-To-Deploy-To-Production)
- [Debug Agent Errors](How-To-Debug-Agent-Errors)

**More Examples:**
- [Email Agent](Email-Agent-Example)

---

**Complete code:** [Download web_scraper.py](https://github.com/wu-changxing/connectonion/tree/main/examples/web_scraper.py)

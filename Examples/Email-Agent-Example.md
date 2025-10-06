# Example: Email Agent - Search and Send Emails with AI

A complete, working example of an AI agent that can search for emails and send messages. This example demonstrates tool creation, error handling, and real-world API integration.

## What This Agent Does

The Email Agent can:
- Search your Gmail inbox by query
- Send emails to specific recipients
- Handle multiple requests in conversation
- Provide clear error messages

**Technologies used:**
- ConnectOnion for the agent framework
- Gmail API for email operations
- OAuth 2.0 for authentication

## Complete Code

```python
from connectonion import Agent
from connectonion.decorators import xray
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
import os.path

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None

    # Load saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

@xray  # Debug this tool if needed
def search_emails(query: str, max_results: int = 5) -> str:
    """
    Search Gmail inbox for emails matching a query.

    Args:
        query: Search query (e.g., "from:john", "subject:meeting", "after:2024/01/01")
        max_results: Maximum number of results to return (1-10)

    Returns:
        List of matching emails with sender, subject, and snippet
    """
    try:
        service = get_gmail_service()

        # Search emails
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=min(max_results, 10)
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return f"No emails found matching '{query}'"

        # Get details for each email
        email_list = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

            # Get snippet
            snippet = msg_data.get('snippet', '')

            email_list.append(f"""
Email #{len(email_list) + 1}:
  From: {sender}
  Date: {date}
  Subject: {subject}
  Preview: {snippet[:100]}...
""")

        result = f"Found {len(email_list)} emails:\n" + "\n".join(email_list)
        return result

    except HttpError as error:
        return f"Gmail API error: {error}"

    except Exception as e:
        return f"Error searching emails: {str(e)}"

@xray  # Debug this tool if needed
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email via Gmail.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email message content

    Returns:
        Success confirmation or error message
    """
    try:
        # Validate inputs
        if "@" not in to:
            return f"Error: '{to}' is not a valid email address"

        if not subject or len(subject) < 2:
            return "Error: Email must have a subject line"

        if not body or len(body) < 10:
            return "Error: Email body too short (minimum 10 characters)"

        # Create message
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send via Gmail API
        service = get_gmail_service()
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return f"✓ Email sent successfully to {to} (Message ID: {sent_message['id']})"

    except HttpError as error:
        return f"Gmail API error: {error}"

    except Exception as e:
        return f"Error sending email: {str(e)}"

# Create the Email Agent
email_agent = Agent(
    name="email-assistant",
    tools=[search_emails, send_email],
    system_prompt="""You are an email assistant that helps manage Gmail.

Your capabilities:
- Search emails using Gmail search syntax (from:, to:, subject:, after:, before:, etc.)
- Send emails to specific recipients

Best practices:
- When searching, use specific queries to find relevant emails
- Before sending, confirm recipient and content
- Provide clear confirmations for actions taken
- If unsure about email addresses, search for them first

Always be helpful and accurate with email operations.""",
    model="gpt-4o-mini"  # Fast and cost-effective
)

# Example usage
if __name__ == "__main__":
    # Enable debugging (optional)
    # email_agent.auto_debug()

    # Example 1: Search for emails
    print("=== Example 1: Search emails ===")
    email_agent.input("Find emails from john in the last week")

    # Example 2: Send an email
    print("\n=== Example 2: Send email ===")
    email_agent.input("Send an email to jane@example.com with subject 'Meeting Reminder' and body 'Don't forget our meeting tomorrow at 2 PM'")

    # Example 3: Multi-step task
    print("\n=== Example 3: Search and reply ===")
    email_agent.input("Search for emails about 'project update' and tell me who sent them")
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install connectonion google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Set Up Gmail API

**a. Enable Gmail API:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API for the project
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`

**b. Place credentials:**
```bash
# Put credentials.json in your project directory
mv ~/Downloads/credentials.json ./credentials.json
```

### 3. First Run (Authentication)

```bash
python email_agent.py
```

On first run:
1. Browser opens for Google sign-in
2. Grant permissions to your app
3. `token.json` is created (stores credentials)
4. Agent is ready to use!

### 4. Set OpenAI API Key

```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

## Usage Examples

### Example 1: Simple Search

```python
email_agent.input("Find emails from Sarah")
```

**Output:**
```
Found 3 emails:

Email #1:
  From: Sarah Johnson <sarah@company.com>
  Date: Mon, 15 Jan 2024 14:30:00
  Subject: Project Update
  Preview: Hi team, I wanted to share our progress...

Email #2:
  From: Sarah Johnson <sarah@company.com>
  Date: Wed, 10 Jan 2024 09:15:00
  Subject: Meeting Notes
  Preview: Thanks for attending today's meeting...

Email #3:
  From: Sarah Johnson <sarah@company.com>
  Date: Fri, 05 Jan 2024 16:45:00
  Subject: Quick Question
  Preview: Do you have a moment to discuss...
```

### Example 2: Advanced Search

```python
# Gmail search syntax
email_agent.input("Find unread emails with attachments from last month")

# Equivalent Gmail query: is:unread has:attachment after:2024/01/01
```

### Example 3: Send Email

```python
email_agent.input("Send an email to john@example.com thanking him for the project update")
```

**Output:**
```
✓ Email sent successfully to john@example.com (Message ID: abc123...)
```

### Example 4: Multi-Turn Conversation

```python
# Turn 1
email_agent.input("Search for emails about the quarterly review")

# Turn 2 (agent remembers context)
email_agent.input("Who sent the most recent one?")

# Turn 3
email_agent.input("Send them a reply saying I'll have the report ready by Friday")
```

## Debugging the Agent

Enable interactive debugging to see what's happening:

```python
email_agent.auto_debug()
email_agent.input("Find emails from John and send him a reply")

# When agent pauses at breakpoint:
# > Press 'c' to continue
# > Press 'a' to ask AI why it made certain choices
# > Press 'e' to modify search results or email content
# > Press 'v' to see execution trace
```

## Customization Ideas

### Add More Email Operations

```python
def mark_as_read(email_ids: str) -> str:
    """Mark emails as read"""
    # Implementation
    pass

def archive_emails(query: str) -> str:
    """Archive emails matching query"""
    # Implementation
    pass

def get_labels() -> str:
    """List all Gmail labels"""
    # Implementation
    pass
```

### Add Filters and Sorting

```python
def search_emails(
    query: str,
    max_results: int = 5,
    sort_by: str = "date"  # date, from, subject
) -> str:
    """Search with sorting options"""
    # Implementation
    pass
```

### Add Attachments

```python
def send_email_with_attachment(
    to: str,
    subject: str,
    body: str,
    attachment_path: str
) -> str:
    """Send email with file attachment"""
    # Implementation
    pass
```

## Common Issues

### Issue: "credentials.json not found"

**Solution:** Download OAuth credentials from Google Cloud Console

### Issue: "Insufficient permissions"

**Solution:**
1. Delete `token.json`
2. Re-run the script
3. Grant all requested permissions

### Issue: "Daily sending limit exceeded"

**Solution:** Gmail has sending limits:
- New accounts: ~100-500 emails/day
- Established accounts: ~2000 emails/day

## Best Practices

### 1. Error Handling

```python
# Tools return error messages as strings
# Agent sees them and can adapt

if error:
    return f"Error: {error_message}"
else:
    return f"Success: {result}"
```

### 2. Input Validation

```python
# Validate before API calls
if "@" not in to:
    return "Error: Invalid email address"
```

### 3. Clear Return Messages

```python
# Bad - unclear
return "Done"

# Good - specific
return f"✓ Email sent to {to}"
```

### 4. Use @xray on Critical Tools

```python
@xray  # Debug email sending
def send_email(...):
    pass

# Don't need @xray for simple searches
def search_emails(...):
    pass
```

## Next Steps

**Enhance This Example:**
- Add calendar integration
- Implement email templates
- Add bulk operations
- Create email summaries

**Learn More:**
- [Creating Custom Tools](Tutorials-Creating-Custom-Tools)
- [Interactive Debugging](Tutorials-Interactive-Debugging-Guide)
- [Deploy to Production](How-To-Deploy-To-Production)

**More Examples:**
- [Web Scraping Agent](Web-Scraping-Agent)

---

**Complete code:** [Download email_agent.py](https://github.com/wu-changxing/connectonion/tree/main/examples/email_agent.py)

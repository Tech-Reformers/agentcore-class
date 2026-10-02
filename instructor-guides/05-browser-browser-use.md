# Browser Tool with Browser-Use (Data Extraction Demo)

**Official Sample**: `awslabs/amazon-bedrock-agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/02-browser-use/`  
**Working Demo**: Use the official sample directly (it works!)

## What This Shows

Unlike Nova Act, **Browser-Use returns actual extracted data** from web pages. Perfect for showing real data extraction in class.

## Setup

First time only:
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser
pip install -r requirements.txt
cd 02-browser-use
python3 patch_browser_use.py
```

## Run Demo (copy-paste this)

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/02-browser-use && python3 getting_started.py --task "Go to example.com and extract all the text content"
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/02-browser-use && python getting_started.py --task "Go to example.com and extract all the text content"
```

Takes ~30-60 sec. **Returns actual extracted data** unlike Nova Act.

**Alternative Tasks:**
```bash
# Wikipedia extract
python3 getting_started.py --task "Go to wikipedia.org/wiki/Amazon_Web_Services and extract the first paragraph"

# AWS pricing
python3 getting_started.py --task "Go to aws.amazon.com/bedrock/pricing and list the main pricing sections"
```

## Expected Output

- Browser session starts
- Claude Haiku agent navigates and extracts data
- **Actual structured data returned** ✅
- Session closes

## Key Differences from Nova Act

| Feature | Nova Act | Browser-Use |
|---------|----------|-------------|
| Data extraction | ❌ No structured output | ✅ Returns extracted data |
| Model | Nova Act API | Claude Haiku (Bedrock) |
| Best for | Task automation | Data extraction |
| Output | Task confirmation | Structured results |

## Summary

Browser-Use with Claude Haiku provides **actual data extraction** from web pages. Use this when you need to show students real data being returned from browser automation.


---

## Teaching Notes

### Where AgentCore is Used

**Key code (lines 80-93):**
```python
from bedrock_agentcore.tools.browser_client import BrowserClient

# AgentCore part: Start managed browser
client = BrowserClient(region)      # ← AgentCore SDK
client.start()                       # ← AWS API call to start browser
ws_url, headers = client.generate_ws_headers()  # ← Get connection info

# browser-use part: Connect to the AgentCore browser
browser_session = Browser(
    cdp_url=ws_url,                  # ← Connect to AWS-managed browser
    browser_profile=BrowserProfile(headers=headers),
)
```

### What Each Component Does

**AgentCore Browser Tool** (AWS service):
- Provides the **managed, secure Chromium sandbox** running in AWS
- Handles browser infrastructure, scaling, security
- Accessed via Chrome DevTools Protocol (CDP)
- API: `StartBrowserSession`, `StopBrowserSession`, `ConnectBrowserAutomationStream`

**browser-use** (open-source library):
- **Client framework** that controls the browser
- Uses Claude (or other LLMs) to decide what actions to take
- Connects to any CDP-compatible browser (including AgentCore's)
- Returns structured data from web pages

**Analogy**: AgentCore = AWS-managed browser infrastructure, browser-use = the driver/controller

### Common Student Questions

**Q: Do we need AgentCore Runtime for this?**  
A: **No!** This uses **AgentCore Browser Tool** only. Runtime is for deploying agents; Browser is for web automation. They're separate services.

**Q: Why use browser-use instead of Nova Act?**  
A: browser-use returns structured data better. Nova Act is great for task automation but doesn't return extracted data. Both work with AgentCore Browser.

**Q: Could we use Playwright directly?**  
A: Yes! Any CDP-compatible tool works. browser-use just makes it easier by adding LLM-based decision making.

### The AgentCore Value Proposition

**Without AgentCore:**
- Set up your own browser infrastructure (Selenium Grid, Docker containers)
- Manage scaling, security, updates
- Handle authentication and network isolation

**With AgentCore Browser Tool:**
- Call `client.start()` → AWS provisions secure browser
- No infrastructure to manage
- Built-in security, scaling, observability
- Just connect and use

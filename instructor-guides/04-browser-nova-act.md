# Browser Tool with Nova Act

**Official Sample**: `awslabs/amazon-bedrock-agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act/`  
**Working Demo**: `instructor-guides/demos/04-browser-nova-act/` *(use this for class)*

## Setup

Ensure Nova Act API key is set:
```bash
export NOVA_ACT_API_KEY=<from nova.amazon.com/act>
```

## Run Demo (Using Fixed Version)

**Mac (copy-paste this):**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/instructor-guides/demos/04-browser-nova-act && python3 getting_started.py --prompt "Navigate to the pricing section and confirm you can see the pricing information" --starting-page "https://aws.amazon.com/bedrock/pricing/" --nova-act-key $NOVA_ACT_API_KEY
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/instructor-guides/demos/04-browser-nova-act && python getting_started.py --prompt "Navigate to the pricing section and confirm you can see the pricing information" --starting-page "https://aws.amazon.com/bedrock/pricing/" --nova-act-key $NOVA_ACT_API_KEY
```

**Expected Output:**
- Status: SUCCEEDED
- Steps executed: 1-3
- No structured data returned (this is normal for Nova Act)

**What This Demonstrates:**
- ✅ AgentCore Browser sessions work
- ✅ Nova Act can connect and control the browser
- ✅ Natural language commands drive browser actions
- ℹ️ Data extraction requires additional integration (e.g., with Strands agents)

Takes ~10-20 sec. Shows execution summary and confirms browser automation worked.

**Key Teaching Point:** This demo shows the **browser infrastructure** working (session creation, Nova Act connection, task execution). Nova Act confirms tasks but doesn't return structured data.

**For data extraction demo, use:** `05-browser-browser-use.md` - Browser-Use with Claude returns actual extracted data.

**Summary**: AgentCore provides managed Chromium sandbox. Nova Act drives browser remotely via Chrome DevTools Protocol. No local browser or webdriver needed.

---

## About the Fixed Version

**Why we created a fixed version:**
- Official AWS sample has bugs (`result.response` doesn't exist, wrong attribute names)
- Fixed version provides better error messages and user guidance
- See `instructor-guides/demos/04-browser-nova-act/README.md` for details

**Upstream issue:** The bugs exist in the official repo at https://github.com/awslabs/amazon-bedrock-agentcore-samples

# Browser Tool with Nova Act

**Sample**: `01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act/`

## Setup

Ensure Nova Act API key is set:
```bash
export NOVA_ACT_API_KEY=<from nova.amazon.com/act>
```

## Run Demo

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act
python3 getting_started.py \
  --prompt "Search for macbooks and extract the details of the first one" \
  --starting-page "https://www.amazon.com/" \
  --nova-act-key $NOVA_ACT_API_KEY
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act
python getting_started.py \
  --prompt "Search for macbooks and extract the details of the first one" \
  --starting-page "https://www.amazon.com/" \
  --nova-act-key $NOVA_ACT_API_KEY
```

Takes ~30-60 sec. Prints extracted macbook details.

**Summary**: AgentCore provides managed Chromium sandbox. Nova Act drives browser remotely via Chrome DevTools Protocol. No local browser or webdriver needed.

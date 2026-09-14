# Lab (Module 4) — Browser Tool with Nova Act

**Sample**: `01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act/`

Nova Act = Amazon's native browser automation. AgentCore provides a managed Chromium sandbox. Nova Act drives the sandbox over Chrome DevTools Protocol.

## Run it

Set the API key (if not already):
```bash
export NOVA_ACT_API_KEY=<from nova.amazon.com/act>
```

Run the headless demo:

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act
python getting_started.py \
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

Takes ~30 sec to a minute. Prints the extracted result.

## Point at in the code (`getting_started.py`)

Three things:

1. **`with browser_session("us-west-2") as client:`** — the AgentCore-managed Chromium session; auto-provisioned on enter, torn down on exit
2. **`ws_url, headers = client.generate_ws_headers()`** — a `wss://` CDP endpoint and SigV4-signed auth headers
3. **`NovaAct(cdp_endpoint_url=ws_url, cdp_headers=headers, ...)`** — Nova Act connects to the remote browser via CDP

Say: "No Playwright driver on your laptop. No `webdriver`. The browser lives in an AWS sandbox, Nova Act drives it remotely."

## Point at in the console output

- `Region:` / `Starting URL:` / `Prompt:` header
- The extracted result — a natural-language answer built from the page

For a live-view flair (real-time DCV streaming), the `live_view.py` script does the same thing but with a viewer. Skip unless the classroom setup makes DCV worth it.

## Cleanup

None — the browser session tears itself down when the `with` block exits. No AWS resources left over.

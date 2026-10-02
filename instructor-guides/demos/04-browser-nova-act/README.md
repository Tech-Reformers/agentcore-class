# Browser Nova Act Demo - Working Version

This is a **fixed version** of the Nova Act browser automation demo from the official AWS samples.

## What Was Fixed

The original sample at `awslabs/amazon-bedrock-agentcore-samples` has bugs:
1. ~~`result.response` doesn't exist~~ → Fixed: Now accesses correct attributes
2. ~~`time_worked` should be `time_worked_s`~~ → Fixed: Uses correct attribute name
3. Added better error messages and guidance for users

**Upstream issue:** https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-features/03-connect-your-agent-to-anything/02-browser/01-nova-act/getting_started.py

## Prerequisites

```bash
pip install boto3 nova-act rich bedrock-agentcore
export NOVA_ACT_API_KEY=<your-key-from-nova.amazon.com/act>
```

## Usage

```bash
python getting_started.py \
  --prompt "Find the pricing information on this page" \
  --starting-page "https://aws.amazon.com/bedrock/pricing/" \
  --nova-act-key $NOVA_ACT_API_KEY
```

## Recommended Prompts

These work reliably:

**Option 1: AWS Documentation**
```bash
python getting_started.py \
  --prompt "Extract and return the key features listed on this page" \
  --starting-page "https://aws.amazon.com/bedrock/pricing/" \
  --nova-act-key $NOVA_ACT_API_KEY
```

**Option 2: Wikipedia (very stable)**
```bash
python getting_started.py \
  --prompt "Extract and return the first paragraph of the article" \
  --starting-page "https://en.wikipedia.org/wiki/Amazon_Web_Services" \
  --nova-act-key $NOVA_ACT_API_KEY
```

**Option 3: Simple page**
```bash
python getting_started.py \
  --prompt "Extract all text from this page" \
  --starting-page "https://example.com/" \
  --nova-act-key $NOVA_ACT_API_KEY
```

## Why Amazon.com Doesn't Work

The original demo used `amazon.com` which often fails due to:
- Anti-bot protection (Cloudflare, captchas)
- Rate limiting
- Dynamic content loading slowly
- Complex page structure

## Teaching Notes

- **Browser sessions** are created by AgentCore and managed in AWS
- **Nova Act** connects to the session via Chrome DevTools Protocol (CDP)
- **Prompts** should explicitly ask to "return" or "extract" data for structured output
- **Sessions auto-expire** after idle timeout (default 15 minutes)

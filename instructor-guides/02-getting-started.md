# Lab (Module 2) — Getting Started with AgentCore CLI

**Project**: `/Users/johnkrull/Projects/agentcore-samples/CustomerSupport/`
**Sample source**: `agentcore-samples/00-getting-started/`

No reset needed between classes. `agentcore deploy` updates the existing stack in place.

## Run it locally

```bash
cd /Users/johnkrull/Projects/agentcore-samples/CustomerSupport
agentcore dev
```

`agentcore dev` starts a local server. Try:
- `Tell me about the Wireless Headphones`
- `What's the return policy for electronics?`
- `I bought PROD-002 and want to return it — what's the policy?` (multi-tool)

Press `Esc` to exit.

## Deploy to AWS

```bash
agentcore deploy
```

Takes ~5 min. Walk the code while it runs.

## Point at in the code (`app/CustomerSupport/main.py`)

Four things, in order:

1. **`app = BedrockAgentCoreApp()`** — wraps the whole agent for AgentCore Runtime
2. **`@tool` decorators on `get_return_policy` / `get_product_info`** — docstring becomes the tool description the model reads
3. **`Agent(model=load_model(), tools=[...], system_prompt=...)`** — a Strands agent, one line to compose
4. **`@app.entrypoint invoke(payload, context)`** — how AgentCore invokes the agent; streams via `stream_async`

Say: "Two tools, one Strands agent, one entrypoint decorator. That's the whole thing."

## Invoke the deployed agent

```bash
agentcore status
agentcore invoke "What's the return policy for audio products?" --stream
agentcore invoke "Tell me about product PROD-004" --stream
```

## Bonus tour (if time)

```bash
agentcore logs                  # live CloudWatch tail
agentcore traces list --limit 5 # OpenTelemetry traces
```

Point out: same agent code, works locally *and* in the cloud. No AWS setup happened in your code — the CLI provisioned IAM/CDK/runtime for you.

## Cleanup

No between-class cleanup needed. The stack costs almost nothing when idle.

If you want a full teardown (e.g. changing accounts, done teaching):
```bash
agentcore remove all
agentcore deploy      # syncs empty state — CDK tears down the stack

# Next class, re-register before dev/deploy:
agentcore add agent --name CustomerSupport --type byo --language Python \
  --framework Strands --model-provider Bedrock \
  --code-location app/CustomerSupport --entrypoint main.py
```

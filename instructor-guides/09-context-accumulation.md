# Lab (Module 9) — Watching Context Fill Up

**Project**: `CustomerSupport/` (the M2 agent, reused)
  - Mac: `/Users/johnkrull/Projects/agentcore-samples/CustomerSupport/`
  - Windows (Git Bash, class PC): `/d/Projects/agentcore-class/CustomerSupport/`

Show attendees that an agent "remembers" the conversation within a session — and prove it by watching the model's input grow between turns. No memory service, no new code. Just visible proof of what Strands is doing behind the scenes.

## Run it

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/CustomerSupport
agentcore dev
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/CustomerSupport
agentcore dev
```

Opens the chat UI + inspector in the browser.

## Multi-turn conversation (in the chat UI)

Ask two related questions. The second must depend on the first, so students see the agent using context:

- Turn 1: `Tell me about PROD-002`
- Turn 2: `What's its return policy?`

The agent should correctly answer turn 2 about the Smart Watch (electronics — 30 day window) even though "it" is never named. That's the payoff.

## Point at in the inspector

After turn 2 completes:

1. Click **Turn 1's trace** in the traces panel
2. Expand `invoke_agent` → find the model call span (`bedrock.converse` or similar)
3. Look at the span's input attribute (e.g. `gen_ai.input.messages`). Note the message array length.
4. Now click **Turn 2's trace**
5. Same span, same attribute — the message array is roughly **doubled**. It contains turn 1's user question, turn 1's assistant response, tool call results, and turn 2's user question.

Say: "Every turn, Strands rebuilds the full conversation and sends it to the model. That's why the agent 'remembers' — it's re-reading the transcript from the top every time."

## Point at in the code (`app/CustomerSupport/main.py`)

Two lines are all it takes:

```python
_agent = None

def get_or_create_agent():
    global _agent
    if _agent is None:
        _agent = Agent(model=..., tools=..., system_prompt=...)
    return _agent
```

Say: "The agent is cached in module-level state. Every invocation reuses the same `Agent` instance, which keeps its `messages` array between calls. That's session memory — free, but ephemeral."

## Why this matters (setup for memory lab)

- **Free, works out of the box**: no code, no service.
- **But it dies** the moment the container recycles, or when you use a different session ID, or when you restart the process.
- **And it doesn't cross conversations**: user comes back tomorrow, agent has no clue who they are.

That's the exact problem AgentCore Memory (M5) solves. This demo is the perfect setup for it.

## Cleanup

Ctrl+C to stop `agentcore dev`. Nothing deployed, nothing to remove.

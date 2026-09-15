# Watching Context Accumulation

**Project**: `CustomerSupport/` (reusing M2 agent)
- Mac: `/Users/johnkrull/Projects/agentcore-samples/CustomerSupport/`
- Windows: `/d/Projects/agentcore-class/CustomerSupport/`

## Run Demo

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

Opens chat UI + inspector in browser.

## Test Multi-Turn Conversation

In the chat UI:
```
Turn 1: Tell me about PROD-002
Turn 2: What's its return policy?
```

Agent answers turn 2 correctly about Smart Watch even though "it" isn't named.

## View in Inspector

1. Click Turn 1's trace → expand `invoke_agent` → check model call input messages (note array length)
2. Click Turn 2's trace → same span → messages array roughly doubled (contains full conversation history)

**Summary**: Strands rebuilds full conversation each turn. Agent "remembers" by re-reading transcript. This is ephemeral session memory — works out of the box but dies when container recycles.

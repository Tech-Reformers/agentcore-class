# Short-Term Memory

**Sample**: `01-features/04-manage-context-of-your-agent/memory/01-short-term-memory/`

## Run Demo

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/04-manage-context-of-your-agent/memory/01-short-term-memory
python3 standard-usage.py sdk
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/04-manage-context-of-your-agent/memory/01-short-term-memory
python standard-usage.py sdk
```

Takes 30 sec - 2 min (waiting for memory resource to become ACTIVE). Shows conversation turns being stored and retrieved.

## Cleanup

**Mac:**
```bash
python3 standard-usage.py sdk --cleanup
```

**Windows (Git Bash):**
```bash
python standard-usage.py sdk --cleanup
```

**Summary**: Short-term memory stores raw conversation turns scoped by actorId + sessionId. Agent reloads context from memory on each invocation.

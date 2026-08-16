# Lab (Module 5) — Short-Term Memory

**Sample**: `01-features/04-manage-context-of-your-agent/memory/01-short-term-memory/standard-usage.py`

Short-term memory = raw conversation turns scoped to `actorId` + `sessionId`. No embeddings, no extraction — just an ordered log for the agent to reload context from.

## Run it

```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/04-manage-context-of-your-agent/memory/01-short-term-memory
python standard-usage.py sdk
```

`sdk` uses the AgentCore Python SDK (recommended). `boto3` shows the raw API for contrast — run it too if you want to compare surfaces.

Takes ~30 sec (memory resource has to become ACTIVE).

## Point at in the code (`standard-usage.py`, `run_with_sdk` function)

Four things:

1. **`MemoryClient` (control plane)** — creates the memory resource, waits for `ACTIVE`
2. **`MemorySessionManager` (data plane)** — binds to a memory, scoped per `actorId` + `sessionId`
3. **`session.add_turns([...])`** — write three conversation turns in one batched call
4. **`session.get_last_k_turns(k=5)`** — reload the last N turns; this is what the agent does at the start of every new invocation

Say: "One memory resource can serve many actors and sessions. The agent hydrates context on invoke, appends the new turn on response, moves on."

## Point at in the console output

- `[sdk] Created memory <id>` — the resource id (copy it if you want to poke around later)
- Turns printed back with roles — proves the round-trip works
- `Keeping memory ... (pass --cleanup to delete)` — resource persists by default

## Cleanup

```bash
python standard-usage.py sdk --cleanup
```

Deletes the memory resource. Or leave it — costs nothing meaningful, and you can inspect it in the console.

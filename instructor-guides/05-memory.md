# Memory Demo (Short-Term Memory)

**Sample**: `instructor-guides/demos/05-memory/` (uses pre-provisioned Memory resource)

✅ **Memory Resource Already Provisioned**: `ClassroomDemo_1790910798-ImR0cmGbmO`

## IN CLASS: Run Demo (Fast!)

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/instructor-guides/demos/05-memory && python3 classroom-demo.py sdk --demo
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/instructor-guides/demos/05-memory && python classroom-demo.py sdk --demo
```

Shows:
1. Adding conversation turns to memory
2. Retrieving conversation turns back from memory

Runs in seconds - just writes and reads conversation data!

## AFTER ALL CLASSES: Cleanup (Optional)

⚠️ **Only run this when you're completely done teaching** - deletes the Memory resource to avoid ongoing charges.

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/instructor-guides/demos/05-memory && python3 classroom-demo.py sdk --cleanup
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/instructor-guides/demos/05-memory && python classroom-demo.py sdk --cleanup
```

**Note**: You can keep this resource running for weeks/months for multiple classes. Only cleanup when you're done teaching this course entirely.

**Summary**: Short-term memory stores raw conversation turns scoped by actorId + sessionId. Agent can reload conversation context from memory on each invocation.


---

## What This Demo Shows

This demonstrates **AgentCore Memory** - managed storage for conversation context.

### The Flow (classroom-demo.py)

**--setup (Already Done)**
   ```python
   memory = client.create_memory_and_wait(
       name="ClassroomDemo_...",
       strategies=[],  # Empty = short-term memory only
       event_expiry_days=30
   )
   ```
   - Creates a Memory resource
   - No strategies = just stores raw conversation turns
   - Waits for status = ACTIVE (~30 sec - 2 min)
   - **Already done** - you can use it for all classes

**--demo (In Class)**
1. **Store Conversation Turns**
   ```python
   session.add_turns([
       ConversationalMessage("Hi, I'm Alex. I prefer Python over Java.", MessageRole.USER),
       ConversationalMessage("Got it, Alex — I'll lean toward Python in examples.", MessageRole.ASSISTANT),
       ConversationalMessage("What did I tell you about my language preference?", MessageRole.USER),
   ])
   ```
   - Each turn is stored as an **event** in AgentCore Memory
   - Scoped by: `memory_id` + `actor_id` + `session_id`

2. **Retrieve Conversation**
   ```python
   turns = session.get_last_k_turns(k=5)
   for turn in turns:
       for msg in turn:
           print(f"{msg['role']}: {msg['content']['text']}")
   ```
   - Gets the last 5 turns from memory
   - Agent can reload conversation context
   - Runs instantly - no AI processing needed

**--cleanup (After All Classes)**
   - Deletes the Memory resource to avoid charges

## Key Concepts

**Memory Resource**
- AWS-managed storage for conversation data
- Multiple actors and sessions per resource
- Events auto-expire after configured days

**Actor** (`actor_id`)
- Represents WHO is having the conversation
- Example: `"user-42"`, `"customer-abc"`, `"agent-1"`

**Session** (`session_id`)
- Represents a single conversation thread
- Example: `"sess-123456"`, `"chat-2024-10-01"`
- Multiple sessions per actor

**Event**
- A single conversation turn (user message or assistant response)
- Stored with timestamp, payload, metadata
- Can be retrieved individually or in bulk

## Two API Styles Shown

**boto3 (raw AWS API)**
```python
control.create_memory(...)
data.create_event(...)
data.list_events(...)
```
- Low-level AWS API calls
- Shows exactly what's on the wire
- More verbose

**SDK (MemorySessionManager)**
```python
session = manager.create_memory_session(...)
session.add_turns([...])
turns = session.get_last_k_turns(k=5)
```
- High-level ergonomic API
- Recommended for production
- Less boilerplate

## Teaching Points

**Without AgentCore Memory:**
- Store conversations in DynamoDB/S3 yourself
- Build retrieval logic
- Handle expiration, cleanup
- Manage scaling

**With AgentCore Memory:**
- Fully managed conversation storage
- Built-in event expiration
- Optimized retrieval APIs
- Automatic scaling

**Use Cases:**
- Multi-turn conversations (chatbots)
- Resume conversations later
- Multiple users/sessions
- Audit trail of interactions

## Common Student Questions

**Q: Is this like RAG or vector search?**  
A: No, this is **short-term memory** - it just stores and retrieves raw conversation turns. No AI processing, no semantic search. For AI-extracted facts and semantic search, you'd add memory **strategies** (see the long-term memory sample).

**Q: Does the agent automatically use this?**  
A: No, your agent code must explicitly retrieve and pass context. The Memory service just stores/retrieves - your agent decides when/what to load.

**Q: What's the difference from just keeping conversation in memory?**  
A: AgentCore Memory persists across agent invocations/restarts, supports multiple sessions, auto-expires old data, and works with agents deployed on Runtime. If your agent crashes or redeploys, conversation history is preserved.

**Q: Why do we need actor_id and session_id?**  
A: One Memory resource can serve many users and conversations. `actor_id` = which user, `session_id` = which conversation thread. This lets you have multiple concurrent chats per user.

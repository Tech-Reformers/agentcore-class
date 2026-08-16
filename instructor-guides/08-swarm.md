# Lab (Module 8) — Strands Swarm (Multi-Agent Orchestration)

Swarm = multiple specialized Strands agents in **one process** that hand off to each other based on the task. Not AgentCore-hosted, not A2A. Pure Strands orchestration primitive.

Different from A2A: A2A is a *wire protocol* between separate services. Swarm is an *in-process* coordination pattern.

## Save the script

Save as `swarm_demo.py` anywhere in the workspace:

```python
import logging
from strands import Agent
from strands.models import BedrockModel
from strands.multiagent import Swarm

logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

model = BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0")

researcher = Agent(name="researcher", model=model, system_prompt="You are a research specialist...")
coder      = Agent(name="coder",      model=model, system_prompt="You are a coding specialist...")
reviewer   = Agent(name="reviewer",   model=model, system_prompt="You are a code review specialist...")
architect  = Agent(name="architect",  model=model, system_prompt="You are a system architecture specialist...")

swarm = Swarm(
    [coder, researcher, reviewer, architect],
    entry_point=researcher,
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,
    node_timeout=300.0,
    repetitive_handoff_detection_window=8,
    repetitive_handoff_min_unique_agents=3,
)

result = swarm("Sketch a REST API for a todo app — endpoints, data model, one code sample")

print(f"\nStatus: {result.status}")
print(f"Node history: {[node.node_id for node in result.node_history]}")
```

## Run it

```bash
export AWS_PROFILE=jkdemo
source /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv/bin/activate
python swarm_demo.py
```

Runs for 30 sec to a few minutes depending on how many handoffs the agents decide they need.

## Point at in the code

Four things:

1. **`from strands.multiagent import Swarm`** — the orchestration primitive
2. **Four named `Agent(...)` instances** — each with a different `system_prompt` defining its specialty
3. **`Swarm([...], entry_point=..., max_handoffs=..., repetitive_handoff_detection_window=...)`** — the swarm config; agents decide when to hand off, safeguards prevent loops
4. **`swarm(task)` returns a `result` with `status` + `node_history`** — the sequence of agents that participated

Say: "You didn't tell them who goes next. Each agent decides — based on its system prompt and the task state — whether to hand off, and to whom. The framework prevents infinite loops with `repetitive_handoff_detection_window`."

## Point at in the console

- **Debug logs** — `strands.multiagent` handoff decisions in real time. Show them the agent-to-agent transitions.
- **Final output** — the last agent's response
- **`Node history`** at the end — the actual sequence, e.g. `['researcher', 'architect', 'coder', 'reviewer']`

That handoff sequence *is* the interesting artifact. Compare across runs — with the same task, agents may pick different paths.

## Cleanup

None. Nothing deployed, no AWS resources beyond the Bedrock calls that already happened.

## Where this fits in the multi-agent story

- **Swarm** — many agents, one process, one shared context
- **A2A** — many agents, separate services, wire protocol between them
- **AgentCore Gateway** — many *tools* served through one MCP endpoint (not multi-agent, but adjacent)

Different problems, different primitives. Swarm is the fastest to demo because there's no infrastructure to stand up.

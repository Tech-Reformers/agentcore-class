# Strands Swarm (Multi-Agent Orchestration)

## Setup

Save as `swarm_demo.py`:

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

## Run Demo

**Mac:**
```bash
export AWS_PROFILE=jkdemo
source /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv/bin/activate
python3 swarm_demo.py
```

**Windows (Git Bash):**
```bash
export AWS_PROFILE=jkdemo
source /d/Projects/agentcore-class/agentcore-samples/.venv/Scripts/activate
python swarm_demo.py
```

Takes 30 sec - few minutes. Watch debug logs showing agent handoffs in real time.

**Summary**: Swarm orchestrates multiple specialized agents in one process. Agents decide when to hand off based on task state. Different from A2A (separate services) — this is in-process coordination.

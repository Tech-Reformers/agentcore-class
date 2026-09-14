# Lab (Module 6) — Observability + Evaluation

Three parts: **built-in traces** (free, no code) + **custom spans** (enrich the picture) + **evaluation** (score the agent).

**Prereq**: CloudWatch Transaction Search must be enabled in the account. Console → CloudWatch → X-Ray settings → Transaction Search. One-time.

## Part 1 — Built-in traces on the CustomerSupport agent

The Module 2 agent is already emitting traces. Show them.

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/CustomerSupport
agentcore invoke "Tell me about product PROD-002" --stream
agentcore invoke "What's the return policy for electronics?" --stream
agentcore traces list --limit 5
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/CustomerSupport
agentcore invoke "Tell me about product PROD-002" --stream
agentcore invoke "What's the return policy for electronics?" --stream
agentcore traces list --limit 5
```

Then open **CloudWatch console → GenAI observability → Bedrock AgentCore**. Filter by the runtime, click a trace, walk:

- The span hierarchy (`invoke_agent` → `model_call` → `tool_call`)
- Timing per span
- Input/output attributes on the model call
- Tool arguments and return values

Say: "You wrote zero telemetry code. ADOT auto-instrumented every Bedrock call and every Strands tool."

## Part 2 — Custom spans

**Sample**: `01-features/06-observe-evaluate-optimize-your-agent/01-observe/custom_span_creation.py`

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/06-observe-evaluate-optimize-your-agent/01-observe
cp .env.example .env
# edit .env if needed
opentelemetry-instrument python custom_span_creation.py --session-id "class-demo"
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/06-observe-evaluate-optimize-your-agent/01-observe
cp .env.example .env
# edit .env if needed
opentelemetry-instrument python custom_span_creation.py --session-id "class-demo"
```

Runs locally, sends spans to CloudWatch. Wait ~30 sec, then look in the same GenAI observability view.

## Point at in the code (`custom_span_creation.py`)

Three things:

1. **`tracer = trace.get_tracer("web_search", "1.0.0")`** — one line, gets you a tracer
2. **`with tracer.start_as_current_span("web_search") as span:`** — creates a span, auto-closes on exit
3. **`span.set_attribute(...)` and `span.add_event(...)`** — attach business metadata and timeline markers

Say: "Custom spans are three lines of OpenTelemetry. You add them where you want visibility that ADOT can't auto-discover — business logic, custom decisions, external calls."

## Point at in the console

Compare two traces side by side in CloudWatch:

- **Auto-only** (Module 2 CustomerSupport) — you see model + tool calls
- **With custom spans** — you also see `web_search` with `search.query`, `search.results_count` attributes and `search_started` / `search_completed` events

## Part 3 — Evaluation on the CustomerSupport agent

AgentCore ships 13 built-in evaluators (Correctness, Helpfulness, ToolSelectionAccuracy, GoalSuccessRate, Refusal, Harmfulness, etc.). Score any trace with one CLI command — no code, no separate deploy.

**Get a recent session ID** (from your Part 1 invocations):

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/CustomerSupport
agentcore traces list --limit 5
# copy a session-id from the output
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/CustomerSupport
agentcore traces list --limit 5
# copy a session-id from the output
```

**Run an on-demand evaluation** against that session:
```bash
agentcore run eval \
  --runtime CustomerSupport \
  --evaluator Builtin.ToolSelectionAccuracy \
  --session-id <paste-session-id>
```

`Builtin.ToolSelectionAccuracy` fits CustomerSupport perfectly — the agent chose between `get_return_policy` and `get_product_info`, evaluator scores whether it picked right.

**Try a few more** — same session, different evaluator:
```bash
agentcore run eval --runtime CustomerSupport --evaluator Builtin.Helpfulness       --session-id <id>
agentcore run eval --runtime CustomerSupport --evaluator Builtin.ResponseRelevance --session-id <id>
```

Each returns a **score**, an **explanation**, and **token usage**. Show the explanations — that's the "why" behind the number.

Say: "You didn't write any evaluation code. Built-in LLM-as-a-judge, one command. In production you'd wire this into a CI/CD pipeline or turn on `online-eval` for continuous sampling."

## Bonus (only if time permits)

Enable continuous online evaluation on CustomerSupport:
```bash
agentcore add online-eval \
  --name CustomerSupportQuality \
  --runtime CustomerSupport \
  --evaluator Builtin.GoalSuccessRate Builtin.Helpfulness \
  --sampling-rate 100 \
  --enable-on-create
agentcore deploy
```

Now every invocation gets scored and results roll up in CloudWatch. Skip unless you have time — it re-deploys the stack.

## Cleanup

Nothing to clean for observability or on-demand evaluation.

If you enabled `online-eval`, remove it before signing off:
```bash
agentcore remove online-eval --name CustomerSupportQuality
agentcore deploy
```

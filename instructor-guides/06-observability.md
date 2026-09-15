# Observability + Evaluation

**Prereq**: Enable CloudWatch Transaction Search in Console → CloudWatch → X-Ray settings.

## Part 1 — Built-in Traces

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

Open **CloudWatch console → GenAI observability → Bedrock AgentCore**. View trace hierarchy, timing, and tool calls.

## Part 2 — Custom Spans

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/06-observe-evaluate-optimize-your-agent/01-observe
cp .env.example .env
opentelemetry-instrument python3 custom_span_creation.py --session-id "class-demo"
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/06-observe-evaluate-optimize-your-agent/01-observe
cp .env.example .env
opentelemetry-instrument python custom_span_creation.py --session-id "class-demo"
```

Wait ~30 sec, then check CloudWatch for custom `web_search` span with attributes and events.

## Part 3 — Evaluation

Get recent session ID:
```bash
cd <CustomerSupport directory>
agentcore traces list --limit 5
```

Run evaluation on a session:
```bash
agentcore run eval \
  --runtime CustomerSupport \
  --evaluator Builtin.ToolSelectionAccuracy \
  --session-id <paste-session-id>

agentcore run eval --runtime CustomerSupport --evaluator Builtin.Helpfulness --session-id <session-id>
agentcore run eval --runtime CustomerSupport --evaluator Builtin.ResponseRelevance --session-id <session-id>
```

Each returns score, explanation, and token usage.

**Summary**: Zero-code observability via ADOT auto-instrumentation. Custom spans add business context. Built-in evaluators score traces on-demand.

# Lab (Module 3) — Inbound Auth with Amazon Cognito

**Sample**: `01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito/`

## Run it

```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito
python inbound_auth_runtime.py
```

Deploy takes ~3 min.

## Point at in the code (while it deploys)

`inbound_auth_runtime.py` — three things, in order:

1. **`AGENT_CODE` string (~line 50)** — the agent itself, runs *inside* the runtime container
   - `@app.entrypoint` → what AgentCore calls
   - Model = inference profile ID
2. **`authorizerConfiguration` block (~line 375)** — the two-value auth config
   - `discoveryUrl` + `allowedClients`
3. **`before-send` hook in `invoke_runtime` (~line 428)** — client side, swaps SigV4 for `Authorization: Bearer <jwt>`

## Point at in the console output

- **Step 5** — no token → `AccessDeniedException`. Rejected *before* the agent runs.
- **Step 6** — JWT obtained, first 30 chars shown.
- **Step 7** — with token → agent returns "sunny".

## Cleanup

```bash
python inbound_auth_runtime.py --cleanup
```

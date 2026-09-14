# Lab (Module 3) — Inbound Auth with Amazon Cognito

**Sample**: `01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito/`

The one concept: **runtimes can require a JWT bearer token instead of AWS SigV4.** Everything else in the script is provisioning plumbing.

## Run it

Prereqs: venv activated, `AWS_PROFILE` set, SSO logged in (see `00-instructor-prep.md`).

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito
python3 inbound_auth_runtime.py
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples/01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito
python inbound_auth_runtime.py
```

Deploy takes ~3 min. The narrative is in the console output — watch Steps 5, 6, 7.

## The one config that matters

Everything else — Cognito pool creation, IAM role setup, S3 zip upload — is boilerplate you can skim. **This** is inbound auth:

```python
# When creating the runtime:
authorizerConfiguration={
    "customJWTAuthorizer": {
        "discoveryUrl": cognito_config["discovery_url"],
        "allowedClients": [cognito_config["client_id"]],
    }
}
```

Two fields. Discovery URL tells AgentCore where to fetch signing keys (JWKS). Allowed clients whitelists which OAuth clients' tokens are accepted. Skip this block entirely and you get default IAM (SigV4) auth.

## The client side — how to pass the token

boto3 signs with SigV4 by default. For a JWT-authed runtime, hook the request pipeline to send a bearer token instead:

```python
def _inject_bearer(request, **_):
    request.headers["Authorization"] = f"Bearer {bearer_token}"

data_plane.meta.events.register(
    "before-send.bedrock-agentcore.InvokeAgentRuntime",
    _inject_bearer,
)
```

That's it — same `invoke_agent_runtime` call, different auth on the wire.

## What to narrate while the script runs

The console prints seven steps. Focus your commentary on three moments:

**Step 5 — "Invoke WITHOUT authorization" → AccessDeniedException**
> "Watch this. No token → the runtime rejects it *before* the agent code runs. This is the security boundary."

**Step 6 — "Access token obtained: eyJraWQ..."**
> "Cognito issues a JWT. We could paste this into jwt.io and see the claims — user id, expiration, audience. AgentCore validates all of that."

**Step 7 — "Agent response: The weather is currently sunny!"**
> "Same request as Step 5. Same runtime. Only difference: the bearer token. That's inbound auth."

## Cleanup

```bash
python3 inbound_auth_runtime.py --cleanup
```

Removes the runtime, IAM role, and Cognito pool. S3 code artifacts stay in the `agentcore-code-*` bucket — delete manually if you care.

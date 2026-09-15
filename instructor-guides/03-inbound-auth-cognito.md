# Inbound Auth with Amazon Cognito

**Sample**: `01-features/05-authenticate-and-authorize/01-inbound-auth/01-inbound-auth-cognito/`

## Setup & Run

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

Takes ~3 min. Watch the console output for three key moments:

## What Happens

1. **Call without token** → AccessDeniedException (runtime blocks before agent runs)
2. **Cognito issues JWT** → Access token obtained
3. **Call with bearer token** → Success ("The weather is currently sunny!")

## Cleanup

**Mac:**
```bash
python3 inbound_auth_runtime.py --cleanup
```

**Windows (Git Bash):**
```bash
python inbound_auth_runtime.py --cleanup
```

**Summary**: Runtimes can require JWT bearer tokens instead of AWS SigV4. AgentCore validates tokens before invoking agent code.

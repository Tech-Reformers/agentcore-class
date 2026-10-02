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

---

## Teaching Notes

### Step 1: Cognito Setup
- **Creates caller identity** (not agent identity) - testuser = the client calling the agent
- Uses **direct password authentication** (username + password → JWT access token)
- Real-world: Use **Cognito for customers**, **corporate SSO** (Okta/Azure AD) for employees
- This is **not OAuth** - it's JWT authentication with an OIDC-compatible provider
- Production would use proper OAuth flows (authorization code + PKCE) or SSO integration

### Step 2: IAM Execution Role
- Role **AgentCore assumes** to run the agent
- Permissions: CloudWatch Logs, X-Ray, Bedrock model invocation

### Step 3: Build & Upload
- Agent code embedded as string for **single-file demo**
- Real projects: actual `strands_agent.py` file in project directory
- `uv` downloads **ARM64 dependencies** (AgentCore runs on Graviton)
- Zip uploaded to S3, temp directory cleaned up

### Step 4: Create Runtime
- `customJWTAuthorizer` config points to Cognito discovery URL
- AgentCore fetches JWKS and validates tokens automatically
- `allowedClients` restricts which app client IDs are accepted

### Steps 5-7: Test Auth Flow
- Without token → `AccessDeniedException` (auth enforced)
- Get token via Cognito **USER_PASSWORD_AUTH** (direct password exchange, not OAuth)
- With token → Success (JWT validated, agent runs)

### Key Concepts
- **JWT in header**: `Authorization: Bearer <jwt>` replaces AWS SigV4
- **Discovery URL**: OIDC `/.well-known/openid-configuration` endpoint
- **Inbound auth**: Controls **who can call** the agent (not agent-to-agent)

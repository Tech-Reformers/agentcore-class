# Getting Started with AgentCore CLI

**Project**: `CustomerSupport/`
- Mac: `/Users/johnkrull/Projects/agentcore-samples/CustomerSupport/`
- Windows: `/d/Projects/agentcore-class/CustomerSupport/`

## Run Locally

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/CustomerSupport
agentcore dev
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/CustomerSupport
agentcore dev
```

**Test prompts:**
```
Tell me about the Wireless Headphones
What's the return policy for electronics?
I bought PROD-002 and want to return it — what's the policy?
```

Press `Esc` to exit.

## Deploy to AWS

```bash
agentcore deploy
```

Takes ~5 min. Shows CustomerSupport agent with two tools (`get_return_policy`, `get_product_info`) deployed to AWS.

## Invoke Deployed Agent

```bash
agentcore status
agentcore invoke "What's the return policy for audio products?" --stream
agentcore invoke "Tell me about product PROD-004" --stream
```

**Summary**: Same agent code runs locally and in AWS. AgentCore CLI handles all infrastructure provisioning.

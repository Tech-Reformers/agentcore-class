# Instructor Prep — Before Every Class

## Pre-Class Setup (2 min)

**Mac:**
```bash
aws sso login --profile jkdemo
export AWS_PROFILE=jkdemo
aws sts get-caller-identity
source /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv/bin/activate
```

**Windows (Git Bash):**
```bash
aws sso login --profile jkdemo
export AWS_PROFILE=jkdemo
aws sts get-caller-identity
source /d/Projects/agentcore-class/agentcore-samples/.venv/Scripts/activate
```

Verify: `(.venv)` shows in prompt and `get-caller-identity` prints your account.

## One-Time Setup (if needed)

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples
python3 -m venv .venv
source .venv/bin/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit
```

**Windows (Git Bash):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples
python -m venv .venv
source .venv/Scripts/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit
```

## Nova Act API Key

**Mac** — add to `~/.zshrc`:
```bash
export NOVA_ACT_API_KEY="<your-key-from-nova.amazon.com/act>"
```

**Windows (Git Bash)** — add to `~/.bashrc`:
```bash
export NOVA_ACT_API_KEY="<your-key-from-nova.amazon.com/act>"
```

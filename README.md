# AgentCore Class

Teaching materials and demo project for the "Building Agentic AI with Amazon Bedrock AgentCore" course.

## Contents

- `instructor-guides/` — Per-module lab guides for teaching the class
- `CustomerSupport/` — The AgentCore CLI-scaffolded customer support agent used in Module 2

## Bootstrap on a new machine

1. Clone this repo:
   ```bash
   git clone https://github.com/Tech-Reformers/agentcore-class.git
   cd agentcore-class
   ```

2. Clone the AWS AgentCore samples repo alongside (needed for M3–M6, M8):
   ```bash
   git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git agentcore-samples
   ```

3. Install prerequisites:
   - Python 3.10+
   - Node.js 20+
   - AWS CLI v2
   - `uv` — `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - AgentCore CLI — `npm install -g @aws/agentcore`

4. Set up the shared venv at the samples repo root:
   ```bash
   cd agentcore-samples
   python3 -m venv .venv
   source .venv/bin/activate
   find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
   pip uninstall -y bedrock-agentcore-starter-toolkit
   ```

5. Install CustomerSupport dependencies:
   ```bash
   cd ../CustomerSupport/agentcore/cdk && npm install
   cd ../.. && agentcore add agent --name CustomerSupport --type byo --language Python \
     --framework Strands --model-provider Bedrock \
     --code-location app/CustomerSupport --entrypoint main.py
   ```

6. Update paths in `instructor-guides/00-instructor-prep.md` to match your machine's home directory.

7. Sign in to AWS via SSO and set the profile before teaching each class:
   ```bash
   aws sso login --profile <your-profile>
   export AWS_PROFILE=<your-profile>
   ```

## Bootstrap on Windows

The guides use zsh/bash commands throughout. On Windows you have two options:

### Recommended: Git Bash

Install [Git for Windows](https://git-scm.com/download/win) — it includes Git Bash. In Git Bash, nearly every command in the guides works verbatim (`export`, `source`, `find`, forward-slash paths). Use it as your daily shell for this class.

### Alternative: PowerShell

Every command needs translation. Common substitutions:

| Guide command (bash) | PowerShell equivalent |
|---|---|
| `export AWS_PROFILE=jkdemo` | `$env:AWS_PROFILE = "jkdemo"` |
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| `find 01-features ... -exec pip install -r {} \;` | `Get-ChildItem 01-features -Recurse -Filter requirements.txt | %{ pip install -r $_.FullName }` |
| `/Users/you/...` | `C:\Users\you\...` |

First time only — enable script execution so `.venv\Scripts\Activate.ps1` works:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Windows-specific prereq commands

- Python 3.10+ — install from [python.org](https://www.python.org/downloads/windows/) or the Microsoft Store
- Node.js 20+ — install from [nodejs.org](https://nodejs.org/)
- AWS CLI v2 — install from [aws.amazon.com/cli](https://aws.amazon.com/cli/)
- `uv`:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- AgentCore CLI:
  ```powershell
  npm install -g @aws/agentcore
  ```

### Line endings

Configure git once so it doesn't auto-convert LF → CRLF and confuse scripts:
```bash
git config --global core.autocrlf input
```

### Update hardcoded paths

The guides reference `/Users/johnkrull/Projects/agentcore-samples/...`. On Windows, do a find/replace across `instructor-guides/*.md` to match your Windows path (e.g. `C:\Users\johnkrull\Projects\agentcore-samples\...` or the Git Bash equivalent `/c/Users/johnkrull/Projects/agentcore-samples/...`).

## Class agenda

See `instructor-guides/` — each `NN-*.md` maps to a module in the course.

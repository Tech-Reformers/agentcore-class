# AgentCore Class

Teaching materials and demo project for the "Building Agentic AI with Amazon Bedrock AgentCore" course.

## Contents

- `instructor-guides/` — Per-module lab guides for teaching the class
- `CustomerSupport/` — The AgentCore CLI-scaffolded customer support agent used in Module 2

## Bootstrap

Pick your platform below. Each recipe is self-contained.

---

### macOS / Linux (zsh or bash)

**1. Install prerequisites**
- Python 3.10+
- Node.js 20+
- AWS CLI v2
- `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- AgentCore CLI: `npm install -g @aws/agentcore`

**2. Clone both repos**
```bash
git clone https://github.com/Tech-Reformers/agentcore-class.git
cd agentcore-class
git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git agentcore-samples
```

**3. Set up the shared venv**
```bash
cd agentcore-samples
python3 -m venv .venv
source .venv/bin/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit
cd ..
```

**4. Install CustomerSupport dependencies**
```bash
cd CustomerSupport/agentcore/cdk && npm install && cd ../..
agentcore add agent --name CustomerSupport --type byo --language Python \
  --framework Strands --model-provider Bedrock \
  --code-location app/CustomerSupport --entrypoint main.py
cd ..
```

**5. Sign in to AWS (before every class session)**
```bash
aws sso login --profile <your-profile>
export AWS_PROFILE=<your-profile>
aws sts get-caller-identity   # verify
```

**6. Update paths** in `instructor-guides/00-instructor-prep.md` to match your machine's home directory.

---

### Windows

Two shell options. **Git Bash** (bundled with [Git for Windows](https://git-scm.com/download/win)) is the easiest — nearly every bash command in the guides works verbatim. **PowerShell** works too but every command needs translation.

**1. Install prerequisites**
- Python 3.10+ from [python.org](https://www.python.org/downloads/windows/)
- Node.js 20+ from [nodejs.org](https://nodejs.org/)
- AWS CLI v2 from [aws.amazon.com/cli](https://aws.amazon.com/cli/)
- Git for Windows (includes Git Bash) from [git-scm.com](https://git-scm.com/download/win)
- `uv` (in PowerShell):
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- AgentCore CLI: `npm install -g @aws/agentcore`

**2. First-time-only settings (PowerShell)**
```powershell
# Allow the venv activation script to run
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Stop git from mangling line endings
git config --global core.autocrlf input
```

**3. Clone both repos** (works in either shell)
```bash
git clone https://github.com/Tech-Reformers/agentcore-class.git
cd agentcore-class
git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git agentcore-samples
```

**4. Set up the shared venv**

Windows venv layout differs — it uses `Scripts/` instead of `bin/`.

*In Git Bash:*
```bash
cd agentcore-samples
python -m venv .venv
source .venv/Scripts/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit
cd ..
```

*In PowerShell:*
```powershell
cd agentcore-samples
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Get-ChildItem 01-features -Recurse -Filter requirements.txt | %{ pip install -r $_.FullName }
pip uninstall -y bedrock-agentcore-starter-toolkit
cd ..
```

**5. Install CustomerSupport dependencies** (either shell)
```bash
cd CustomerSupport/agentcore/cdk && npm install && cd ../..
agentcore add agent --name CustomerSupport --type byo --language Python `
  --framework Strands --model-provider Bedrock `
  --code-location app/CustomerSupport --entrypoint main.py
cd ..
```
(PowerShell uses backtick `` ` `` for line continuation; Git Bash uses backslash `\`.)

**6. Sign in to AWS (before every class session)**

*Git Bash:*
```bash
aws sso login --profile <your-profile>
export AWS_PROFILE=<your-profile>
aws sts get-caller-identity
```

*PowerShell:*
```powershell
aws sso login --profile <your-profile>
$env:AWS_PROFILE = "<your-profile>"
aws sts get-caller-identity
```

**7. Update paths** in `instructor-guides/00-instructor-prep.md` from `/Users/johnkrull/...` to your Windows path. Git Bash: use `/c/Users/<you>/...`. PowerShell: use `C:\Users\<you>\...`.

---

## Class agenda

See `instructor-guides/` — each `NN-*.md` maps to a module in the course.

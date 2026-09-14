# Instructor Prep — Before Every Class

## Right before class (2 min)

**Mac:**
```bash
aws sso login --profile jkdemo
export AWS_PROFILE=jkdemo
aws sts get-caller-identity
source /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv/bin/activate
which agentcore    # must NOT point inside the .venv
```

**Windows (Git Bash, class PC):**
```bash
aws sso login --profile jkdemo
export AWS_PROFILE=jkdemo
aws sts get-caller-identity
source /d/Projects/agentcore-class/agentcore-samples/.venv/Scripts/activate
which agentcore    # must NOT point inside the .venv
```

If `get-caller-identity` prints your account and role, your prompt has `(.venv)`, and `which agentcore` points outside the venv, you're ready. On Mac that's typically `/usr/local/bin/agentcore` (wherever npm installed it); on the Windows class PC it'll be somewhere under `%APPDATA%\npm` — as long as it's not inside `.venv/Scripts/`, you're fine.

If `which agentcore` points inside `.venv/bin/` (Mac) or `.venv/Scripts/` (Windows), run: `pip uninstall -y bedrock-agentcore-starter-toolkit` — that's the deprecated Python toolkit shadowing the npm CLI.

The `export` scopes `AWS_PROFILE=jkdemo` to this shell only — close the terminal and it's gone, so it won't affect other AWS work in other shells.

## If a lab breaks mid-class

| Error | Fix |
|---|---|
| `InvalidClientTokenId` / `security token ... expired` | `aws sso login` |
| `AccessDeniedException ... service control policy` | Region-Deny SCP hit. Change `global.` → `us.` on the model ID, or disable the SCP in Control Tower |
| `Invocation of model ID ... on-demand throughput isn't supported` | Model needs an inference profile. Prefix with `us.` |
| `You don't have access to the model` | Enable model access in Bedrock console |
| `RuntimeClientError: 500 from runtime` | Agent code failed inside runtime. Check CloudWatch: `/aws/bedrock-agentcore/runtimes/<id>-DEFAULT` |
| `agentcore invoke ... No such option: --stream` | Python starter toolkit is shadowing the npm CLI. Run: `pip uninstall -y bedrock-agentcore-starter-toolkit` |
| (Windows) `source .../.venv/bin/activate: No such file or directory` | Windows venvs have no `bin/` folder. Use `source .../.venv/Scripts/activate` instead |
| (Windows) `command not found` after `source .venv/Scripts/activate` looked fine | Confirm the prompt actually shows `(.venv)` — if not, re-check the path; the class PC repo root is `/d/Projects/agentcore-class/`, not `/Users/johnkrull/...` |

## CloudWatch query for any runtime error

```
fields @timestamp, level, message, errorType, errorMessage
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
```

## Nova Act key naming gotcha

Nova console gives `NOVA_API_KEY`, samples expect `NOVA_ACT_API_KEY`.

**Mac** — add to `~/.zshrc`:
```bash
export NOVA_ACT_API_KEY="$NOVA_API_KEY"
```

**Windows (Git Bash)** — there's no `.zshrc`. Add to `~/.bashrc` (Git Bash reads this on startup):
```bash
export NOVA_ACT_API_KEY="$NOVA_API_KEY"
```
This only persists for Git Bash sessions. If you also need it outside Git Bash (e.g. a `cmd`/PowerShell terminal), set it as a durable Windows env var instead: `setx NOVA_ACT_API_KEY "<value>"` (requires a new terminal to take effect).

## One-time setup (already done)

Venv at `agentcore-samples/agentcore-samples/.venv` under the samples repo root. Only redo if you re-clone the samples repo or upgrade Python.

If you ever rebuild the venv, follow the mass install with the toolkit uninstall so it doesn't shadow the npm CLI:

**Mac:**
```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples
python3 -m venv .venv
source .venv/bin/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit    # always after mass install
```

**Windows (Git Bash, class PC):**
```bash
cd /d/Projects/agentcore-class/agentcore-samples
python -m venv .venv
source .venv/Scripts/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit    # always after mass install
```

# Instructor Prep — Before Every Class

## Right before class (2 min)

```bash
aws sso login --profile jkdemo
export AWS_PROFILE=jkdemo
aws sts get-caller-identity
source /Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv/bin/activate
which agentcore    # must NOT point inside the .venv
```

If `get-caller-identity` prints your account and role, your prompt has `(.venv)`, and `which agentcore` points to `/usr/local/bin/agentcore` (or wherever npm installed it), you're ready.

If `which agentcore` points inside `.venv/bin/`, run: `pip uninstall -y bedrock-agentcore-starter-toolkit` — that's the deprecated Python toolkit shadowing the npm CLI.

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

## CloudWatch query for any runtime error

```
fields @timestamp, level, message, errorType, errorMessage
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
```

## Nova Act key naming gotcha

Nova console gives `NOVA_API_KEY`, samples expect `NOVA_ACT_API_KEY`. Add to `~/.zshrc`:
```bash
export NOVA_ACT_API_KEY="$NOVA_API_KEY"
```

## One-time setup (already done)

Venv at `/Users/johnkrull/Projects/agentcore-samples/agentcore-samples/.venv`. Only redo if you re-clone the samples repo or upgrade Python.

If you ever rebuild the venv, follow the mass install with the toolkit uninstall so it doesn't shadow the npm CLI:

```bash
cd /Users/johnkrull/Projects/agentcore-samples/agentcore-samples
python3 -m venv .venv
source .venv/bin/activate
find 01-features -maxdepth 4 -name requirements.txt -exec pip install -r {} \;
pip uninstall -y bedrock-agentcore-starter-toolkit    # always after mass install
```

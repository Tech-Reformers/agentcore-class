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

## Class agenda

See `instructor-guides/` — each `NN-*.md` maps to a module in the course.

"""Interactive chat with a deployed Bedrock AgentCore harness.

Usage:
    python invoke_harness.py                    # start an interactive chat loop
    python invoke_harness.py "your prompt"      # send a single prompt and exit

Notes:
    - runtimeSessionId groups turns into one conversation. The interactive loop
      reuses one session id for the whole run so the harness keeps context.
      Session IDs must be reasonably long (>= 33 chars).
    - Requires a recent boto3/botocore that includes the `invoke_harness` API.
    - Your AWS credentials must have `bedrock-agentcore:InvokeHarness` on the
      harness ARN below.
    - Type 'exit' or 'quit' (or press Ctrl-C / Ctrl-D) to leave the chat.
"""

import sys
import uuid

import boto3

REGION = "us-east-1"
HARNESS_ARN = (
    "arn:aws:bedrock-agentcore:us-east-1:352486303890:harness/"
    "my_demo_harness2-P9FC6dxjBs"
)

# Error event keys that may appear in the stream.
ERROR_KEYS = (
    "internalServerException",
    "throttlingException",
    "validationException",
    "accessDeniedException",
    "serviceQuotaExceededException",
    "conflictException",
    "resourceNotFoundException",
)


def invoke(client, prompt: str, session_id: str) -> None:
    """Send one prompt and stream the assistant's reply to stdout."""
    response = client.invoke_harness(
        harnessArn=HARNESS_ARN,
        runtimeSessionId=session_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
    )

    for event in response["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            if "text" in delta:
                print(delta["text"], end="", flush=True)
        elif any(key in event for key in ERROR_KEYS):
            print("\n[ERROR]", event)

    print()


def chat_loop(client, session_id: str) -> None:
    """Read prompts from the user and stream replies until they quit."""
    print("Connected to harness. Type 'exit' or 'quit' to leave.\n")
    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not prompt:
            continue
        if prompt.lower() in ("exit", "quit"):
            break

        print("bot> ", end="", flush=True)
        invoke(client, prompt, session_id)


def main() -> None:
    client = boto3.client("bedrock-agentcore", region_name=REGION)
    # One session id per run keeps conversation context across turns.
    session_id = f"demo-session-{uuid.uuid4()}"

    if len(sys.argv) > 1:
        # Single-shot mode: send the provided prompt and exit.
        invoke(client, sys.argv[1], session_id)
    else:
        # Interactive mode.
        chat_loop(client, session_id)


if __name__ == "__main__":
    main()

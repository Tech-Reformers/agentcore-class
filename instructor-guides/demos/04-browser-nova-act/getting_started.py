"""
Basic Browser Tool Usage with Amazon Nova Act SDK - FIXED VERSION

Demonstrates headless browser automation using the AgentCore Browser Tool
and Nova Act SDK:
  1. Start a browser session via browser_session() context manager
  2. Generate a CDP WebSocket URL and auth headers
  3. Connect Nova Act to the browser session
  4. Execute a natural language prompt on a target page
  5. Print the result and exit

Prerequisites:
    pip install boto3 nova-act rich bedrock-agentcore
    export NOVA_ACT_API_KEY=<your-nova-act-api-key>

IAM permissions required:
    bedrock-agentcore:StartBrowserSession
    bedrock-agentcore:StopBrowserSession
    bedrock-agentcore:ConnectBrowserAutomationStream

Usage:
    python getting_started.py \
        --prompt "Find the pricing information on this page" \
        --starting-page "https://aws.amazon.com/bedrock/pricing/" \
        --nova-act-key $NOVA_ACT_API_KEY
"""

import argparse
import os

from boto3.session import Session
from nova_act import NovaAct
from rich.console import Console

from bedrock_agentcore.tools.browser_client import browser_session

console = Console()


def browser_with_nova_act(
    prompt: str,
    starting_page: str,
    nova_act_key: str,
    region: str = "us-west-2",
):
    """Run a Nova Act prompt in an AgentCore Browser session."""
    result = None
    with browser_session(region) as client:
        ws_url, headers = client.generate_ws_headers()
        try:
            with NovaAct(
                cdp_endpoint_url=ws_url,
                cdp_headers=headers,
                preview={"playwright_actuation": True},
                nova_act_api_key=nova_act_key,
                starting_page=starting_page,
            ) as nova_act:
                result = nova_act.act(prompt)
        except Exception as exc:
            console.print(f"[red]NovaAct error:[/red] {exc}")
    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Headless browser demo with Nova Act and AgentCore Browser Tool")
    parser.add_argument("--prompt", required=True, help="Natural language browser instruction")
    parser.add_argument("--starting-page", required=True, help="Starting URL for the browser")
    parser.add_argument(
        "--nova-act-key",
        default=os.getenv("NOVA_ACT_API_KEY"),
        help="Nova Act API key (env: NOVA_ACT_API_KEY)",
    )
    parser.add_argument("--region", default=Session().region_name or "us-west-2")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.nova_act_key:
        console.print("[red]ERROR:[/red] --nova-act-key is required (or set NOVA_ACT_API_KEY).")
        raise SystemExit(1)

    console.print("=" * 60)
    console.print("AgentCore Browser Tool — Nova Act Getting Started (FIXED)")
    console.print("=" * 60)
    console.print(f"  Region:       {args.region}")
    console.print(f"  Starting URL: {args.starting_page}")
    console.print(f"  Prompt:       {args.prompt}")

    result = browser_with_nova_act(
        args.prompt,
        args.starting_page,
        args.nova_act_key,
        args.region,
    )

    if result:
        console.print(f"\n[bold green]✅ Nova Act Execution Summary:[/bold green]")
        console.print(f"  Status: SUCCEEDED")
        console.print(f"  Steps executed: {result.metadata.num_steps_executed}")
        console.print(f"  Time worked: {result.metadata.time_worked_s}")
        console.print(f"  Session ID: {result.metadata.session_id}")
        
        # Check for various possible data attributes
        if hasattr(result, 'return_value') and result.return_value:
            console.print(f"\n[cyan]📊 Extracted Data:[/cyan]")
            console.print(result.return_value)
        elif hasattr(result, 'data') and result.data:
            console.print(f"\n[cyan]📊 Extracted Data:[/cyan]")
            console.print(result.data)
        else:
            console.print(f"\n[yellow]ℹ️  Nova Act completed successfully.[/yellow]")
            console.print(f"[yellow]Note: No structured data was returned. The agent confirmed task completion.[/yellow]")
            console.print(f"[yellow]For data extraction, ensure your prompt explicitly asks to 'return' or 'extract' information.[/yellow]")
    else:
        console.print("\n[red]❌ No result returned.[/red]")

    console.print("\n" + "=" * 60)
    console.print("Demo complete!")
    console.print("=" * 60)


if __name__ == "__main__":
    main()

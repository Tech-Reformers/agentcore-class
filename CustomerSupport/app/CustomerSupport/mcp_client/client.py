import os
import logging
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

logger = logging.getLogger(__name__)

# An MCP server exposes tools the agent can call over HTTP. This public example needs no auth.
EXAMPLE_MCP_ENDPOINT = "https://mcp.exa.ai/mcp"

def get_streamable_http_mcp_client() -> MCPClient:
    """Connect to an MCP server and expose its tools to a Strands agent."""
    # For a server that requires auth, pass headers={"Authorization": f"Bearer {access_token}"}.
    return MCPClient(lambda: streamablehttp_client(EXAMPLE_MCP_ENDPOINT))

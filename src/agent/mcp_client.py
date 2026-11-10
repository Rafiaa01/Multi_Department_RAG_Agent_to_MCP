from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient(
    {
        "hr": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8001/mcp",
        },
        "it": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8002/mcp",
        },
        "finance": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8003/mcp",
        },
    }
)


async def get_mcp_tools():
    """Discover tools from all connected MCP servers."""

    tools = await mcp_client.get_tools()

    return tools
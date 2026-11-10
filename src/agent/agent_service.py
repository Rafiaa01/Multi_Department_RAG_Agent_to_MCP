from src.agent.mcp_client import get_mcp_tools
from src.agent.tools_agent import create_department_agent


async def initialize_agent():
    """Discover MCP tools and initialize the department agent."""

    tools = await get_mcp_tools()

    agent = create_department_agent(tools)

    return agent
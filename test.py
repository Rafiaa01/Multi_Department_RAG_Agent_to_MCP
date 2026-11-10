
import asyncio

from src.agent.mcp_client import get_mcp_tools


async def main():
    tools = await get_mcp_tools()

    for tool in tools:
        print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())

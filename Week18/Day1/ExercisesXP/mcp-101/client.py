import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Parameters to spawn the MCP server
server_params = StdioServerParameters(
    command="mcp",
    args=["run", "server.py"],
    env=None
)

def extract_content(payload):
    """Extract text content from MCP responses."""
    if hasattr(payload, "contents"):
        contents = payload.contents
        if contents:
            first = contents[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)
    if hasattr(payload, "content"):
        return payload.content
    return str(payload)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session
            await session.initialize()

            # List resources
            resources = await session.list_resources()
            print("Resources:")
            for r in resources.resources:
                print("-", r.uri)

            # List tools
            tools = await session.list_tools()
            print("\nTools:")
            for t in tools.tools:
                print("-", t.name)

            # Read resource
            greeting = await session.read_resource("greeting://hello")
            print("\nGreeting result:")
            print(extract_content(greeting))

            # Call tool
            result = await session.call_tool(
                "add",
                {"a": 1, "b": 7}
            )
            print("\nAdd tool result:")
            print(extract_content(result))

if __name__ == "__main__":
    asyncio.run(run())


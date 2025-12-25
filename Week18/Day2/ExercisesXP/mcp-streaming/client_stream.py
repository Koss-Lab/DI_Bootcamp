import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def on_message(message):
    """
    Handle MCP notifications.
    NOTE: STDIO transport does not surface notifications,
    but this handler is required for HTTP transports.
    """
    if isinstance(message, types.Notification):
        print("NOTIFICATION:", message.params)

async def run():
    """
    Client using STDIO fallback transport.
    HTTP is preferred for notifications, but STDIO is used
    here for stability in local execution.
    """

    params = StdioServerParameters(
        command="python3",
        args=["server_stream.py"]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(
            read,
            write,
            message_handler=on_message
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                "process_items",
                arguments={"total": 5}
            )

            print("FINAL RESULT:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run())

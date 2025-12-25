from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("Streaming-Demo")

@mcp.tool(description="Process items and emit progress notifications")
async def process_items(total: int = 5, ctx=None) -> str:
    """
    Long-running tool emitting structured MCP notifications.
    """
    for i in range(1, total + 1):
        await asyncio.sleep(0.3)

        if ctx is not None:
            await ctx.notify(
                "progress",
                {
                    "current": i,
                    "total": total,
                    "message": f"Processing item {i}/{total}"
                }
            )

    return f"Processed {total} items successfully."

if __name__ == "__main__":
    # Streamable HTTP enabled (notifications supported on HTTP transports)
    mcp.run(transport="streamable-http")

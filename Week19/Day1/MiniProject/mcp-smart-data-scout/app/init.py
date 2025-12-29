# app/init.py
import asyncio
from app.mcp_registry import ToolRegistry
from app.orchestrator import Orchestrator


async def demo():
    reg = ToolRegistry()
    await reg.start()
    agent = Orchestrator(reg)

    print(await agent.run_async("What time is it now?"))
    print(await agent.run_async("Fetch https://example.com and summarize it."))

    await reg.close()


if __name__ == "__main__":
    asyncio.run(demo())

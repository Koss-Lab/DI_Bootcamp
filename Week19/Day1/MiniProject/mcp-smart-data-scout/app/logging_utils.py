import json
from datetime import datetime


def log_tool_call(tool: str, args: dict, result: dict):
    """
    Logs summarized MCP tool calls for observability.
    """

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "tool": tool,
        "arguments": args,
        "result_preview": str(result)[:200],
    }

    print("[MCP TOOL]", json.dumps(log_entry))

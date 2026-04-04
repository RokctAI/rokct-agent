"""
Gateway management tools.
"""

import json
from tools.registry import registry
from tools.session_digest_tool import generate_session_digest

def session_digest_handler(args: dict) -> str:
    """Handler for session_digest tool."""
    active_threshold = args.get("active_threshold_minutes", 60)
    digest = generate_session_digest(active_threshold_minutes=active_threshold)
    return json.dumps({"success": True, "digest": digest})

registry.register(
    name="session_digest",
    toolset="gateway",
    schema={
        "name": "session_digest",
        "description": "Generate a digest of active and idle gateway sessions.",
        "parameters": {
            "type": "object",
            "properties": {
                "active_threshold_minutes": {
                    "type": "integer",
                    "description": "Threshold in minutes to consider a session active.",
                    "default": 60
                }
            }
        }
    },
    handler=session_digest_handler,
    description="Generate a digest of active and idle gateway sessions.",
    emoji="📊"
)

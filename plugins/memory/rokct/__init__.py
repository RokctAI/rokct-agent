"""
RokctMemoryProvider — Briding agent memory with the Frappe brain app and pgvector.

Philosophy: The agent's memory is the Frappe database. No duplicate storage.
Integrates with 'brain' app for semantic search and fact recording.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)

class RokctMemoryProvider(MemoryProvider):
    """
    Memory provider that uses Frappe's 'brain' app (pgvector) for storage.
    """

    def __init__(self):
        self._session_id = None
        self._user_id = None
        self._platform = None
        self._initialized = False

    @property
    def name(self) -> str:
        return "rokct"

    def is_available(self) -> bool:
        """Check if Frappe credentials are set."""
        return all([
            os.getenv("FRAPPE_BASE_URL"),
            os.getenv("FRAPPE_API_KEY"),
            os.getenv("FRAPPE_API_SECRET")
        ])

    def initialize(self, session_id: str, **kwargs) -> None:
        """Warm up connection to Frappe."""
        self._session_id = session_id
        self._user_id = kwargs.get("user_id", "guest")
        self._platform = kwargs.get("platform", "unknown")
        self._initialized = True
        logger.debug("RokctMemoryProvider initialized for user %s", self._user_id)

    def system_prompt_block(self) -> str:
        """Instructions for using Rokct memory."""
        return (
            "## Memory System: Rokct Brain\n"
            "Your long-term memory is managed by the Rokct Brain (Frappe + pgvector).\n"
            "- Important facts from this conversation are automatically saved.\n"
            "- You can explicitly search past context using the `search_engrams` tool."
        )

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """Semantic recall from Frappe brain."""
        if not self._initialized: return ""
        
        from gateway.frappe_integration import call_frappe_api
        args = {
            "query": query,
            "user": self._user_id,
            "limit": 5
        }
        
        try:
            from model_tools import _run_async
            result = _run_async(call_frappe_api("brain.api.semantic_search", args))
            
            if result.get("success") and result.get("results"):
                context = "\n".join([f"- {r['content']}" for r in result["results"]])
                return f"\n### Relevant Past Context:\n{context}\n"
        except Exception as e:
            logger.warning("Rokct prefetch failed: %s", e)
            
        return ""

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """Persist conversation turn to brain app."""
        if not self._initialized: return
        
        from gateway.frappe_integration import call_frappe_api
        args = {
            "user": self._user_id,
            "platform": self._platform,
            "session_id": session_id or self._session_id,
            "messages": [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
        }
        
        try:
            from model_tools import _run_async
            _run_async(call_frappe_api("brain.api.record_turn", args))
        except Exception as e:
            logger.warning("Rokct sync_turn failed: %s", e)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Expose brain search tool."""
        return [
            {
                "name": "search_engrams",
                "description": "Search your long-term memory for past facts and context.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search term or question."}
                    },
                    "required": ["query"]
                }
            }
        ]

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        """Handle search_engrams tool."""
        if tool_name == "search_engrams":
            from gateway.frappe_integration import call_frappe_api
            from model_tools import _run_async
            query_args = {
                "query": args["query"],
                "user": self._user_id,
                "limit": 10
            }
            result = _run_async(call_frappe_api("brain.api.semantic_search", query_args))
            return json.dumps(result)
            
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def shutdown(self) -> None:
        pass

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {"key": "base_url", "description": "Frappe Site URL", "env_var": "FRAPPE_BASE_URL", "required": True},
            {"key": "api_key", "description": "Frappe API Key", "env_var": "FRAPPE_API_KEY", "secret": True, "required": True},
            {"key": "api_secret", "description": "Frappe API Secret", "env_var": "FRAPPE_API_SECRET", "secret": True, "required": True}
        ]

def register(ctx):
    """Plugin registration entry point."""
    ctx.register_memory_provider(RokctMemoryProvider())

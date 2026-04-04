"""
Dynamic Frappe Toolset for Hermes Agent.
Loads ERP tools on-demand based on entity detection.
"""

import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any

from tools.registry import registry
from gateway.frappe_integration import call_frappe_api

logger = logging.getLogger(__name__)

# Path to baked schemas inside the tenant site
SCHEMA_PATH = Path("/home/frappe/frappe-bench/sites/currentsite/rcore/platform/schemas/ai_tools.json")

class FrappeDynamicToolset:
    """
    Manages lazy-loading of Frappe tools based on entity context.
    """
    def __init__(self):
        self._cached_schemas = {}
        self._loaded_tools = set()

    async def get_tools_for_message(self, message: str) -> List[str]:
        """
        1. Detect entities/intent from message.
        2. Fetch tool names from platform:get_entity_tools.
        3. Register/Return only those tool names.
        """
        entities = await self._detect_entities(message)
        if not entities:
            return []

        all_tool_names = set()
        for entity in entities:
            # Fetch allowed tool names for this entity
            result = await call_frappe_api("platform:get_entity_tools", {"entity": entity})
            if result.get("success") and result.get("tools"):
                all_tool_names.update(result["tools"])
                # We could also recursively fetch tools for related_entities if they aren't in 'entities'
                # but for now let's keep it simple as per requirement.

        if all_tool_names:
            await self._register_tools(list(all_tool_names))
        
        return list(all_tool_names)

    async def _detect_entities(self, text: str) -> List[str]:
        """
        Use SentenceTransformer to map text to entities.
        Returns a list of matching entities.
        """
        candidate_entities = ["invoice", "customer", "item", "lead"]
        found = []
        try:
            from sentence_transformers import SentenceTransformer, util
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            text_emb = model.encode(text, convert_to_tensor=True)
            ent_embs = model.encode(candidate_entities, convert_to_tensor=True)
            
            scores = util.cos_sim(text_emb, ent_embs)[0]
            
            for idx, score in enumerate(scores):
                if score > 0.35: # Slightly lower threshold to capture multiple
                    found.append(candidate_entities[idx])
        except Exception:
            # Fallback simple keyword check
            lowered = text.lower()
            for e in candidate_entities:
                if e in lowered: found.append(e)
        
        return found

    def _execute_remote_tool(self, cmd: str, args: dict, **kwargs) -> str:
        """Routes the tool call back to Frappe via api.tenant."""
        from model_tools import _run_async
        return _run_async(call_frappe_api(cmd, args))

    async def _register_tools(self, names: List[str]):
        """
        Loads schemas from ai_tools.json and registers them if not already done.
        """
        if not SCHEMA_PATH.exists():
            # Try a fallback path if we're in the monorepo env
            fallback = Path("/home/jules/ecosystem/monorepo_pat/rcore/rcore/platform/schemas/ai_tools.json")
            if fallback.exists():
                schema_file = fallback
            else:
                return
        else:
            schema_file = SCHEMA_PATH

        if not self._cached_schemas:
            try:
                with open(schema_file, "r") as f:
                    schemas = json.load(f)
                    self._cached_schemas = {s["name"]: s for s in schemas}
            except Exception as e:
                logger.debug(f"Failed to load ai_tools.json: {e}")
                return

        for name in names:
            if name in self._loaded_tools:
                continue
            
            schema = self._cached_schemas.get(name)
            if not schema:
                continue

            # Capture name in closure
            def make_handler(cmd_name):
                return lambda args, **kw: self._execute_remote_tool(cmd_name, args, **kw)

            registry.register(
                name=name,
                toolset="frappe",
                schema=schema,
                handler=make_handler(name),
                emoji="🚜"
            )
            self._loaded_tools.add(name)

# Global instance
frappe_dynamic = FrappeDynamicToolset()

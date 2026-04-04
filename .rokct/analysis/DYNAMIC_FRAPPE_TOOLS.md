# Technical Guide: Dynamic Frappe Tools in Hermes Agent [DONE] (done)

This guide explains how to use your `rcore` platform's "Bake" logic to dynamically inject Frappe capabilities into Hermes Agent as executable tools.

## 1. The Dynamic Tool Architecture [DONE]

Your `manager.py` already generates `ai_tools.json` (OpenAI tool schemas). Hermes Agent can consume these schemas to register tools on the fly.

**The Flow:**
1.  **Frappe:** You run `bake_assets()`. It scans `api.py` and produces `ai_tools.json`.
2.  **Hermes:** A custom `FrappeDynamicToolset` reads this JSON at startup.
3.  **LLM:** The agent sees all your Frappe methods (e.g., `erpnext:create_invoice`) as standard tools.
4.  **Execution:** When the agent calls a tool, Hermes routes the request to your Frappe `api.tenant` gateway.

## 2. Implementation: `tools/frappe_dynamic.py` [DONE]

You can implement this in Hermes with a single Python file.

```python
import json
import requests
from pathlib import Path
from tools.registry import registry

# Path to your baked schemas
SCHEMA_PATH = Path("/home/frappe/frappe-bench/sites/currentsite/rcore/platform/schemas/ai_tools.json")

def execute_frappe_tool(cmd, payload, task_id=None):
    """
    Routes Hermes tool calls to the Frappe Gateway.
    """
    # Resolve your Frappe site URL and API Key
    # In a real setup, these would come from Hermes .env or config.yaml
    FRAPPE_URL = "http://localhost:8000/api/method/rcore.platform.api.tenant"
    HEADERS = {
        "Authorization": "token <api_key>:<api_secret>",
        "Content-Type": "application/json"
    }
    
    data = {
        "cmd": cmd,
        "payload": payload
    }
    
    response = requests.post(FRAPPE_URL, json=data, headers=HEADERS)
    return response.text

def register_dynamic_tools():
    """
    Reads ai_tools.json and registers each one in the Hermes registry.
    """
    if not SCHEMA_PATH.exists():
        return

    with open(SCHEMA_PATH, "r") as f:
        tools = json.load(f)

    for tool_def in tools:
        cmd_name = tool_def["name"]
        
        registry.register(
            name=cmd_name,
            toolset="frappe",
            schema=tool_def,
            handler=lambda args, cmd=cmd_name, **kw: execute_frappe_tool(cmd, args, **kw),
            emoji="🚜" # Frappe tractor emoji
        )

# Initialize on import
register_dynamic_tools()
```

## 3. Handling Multi-Tenancy

To make this work for your different users (Tenants), you need to pass the tenant context from Hermes to Frappe.

1.  **Hermes Session:** When a message comes in from WhatsApp, Hermes knows the `user_id`.
2.  **Mapping:** You should maintain a mapping table (or use your Frappe user records) to link the WhatsApp `user_id` to a Frappe `API Key/Secret`.
3.  **Execution:** In `execute_frappe_tool`, you dynamically select the `Authorization` header based on the current session's user.

## 4. Why this is powerful

-   **Zero Code Maintenance:** If you add a new feature to Frappe (e.g., `Paas: Reboot Server`), you just run `bake`. The Agent automatically "learns" the new tool without you writing a single line of Python/Go in the agent codebase.
-   **Security & Redaction:** Hermes v0.7.0 includes enhanced **Secret Exfiltration Blocking**. You can add patterns for Frappe `sid` and API secrets to the redaction engine to ensure they never leak.
-   **Inline Diffs:** v0.7.0's **Inline Diff Previews** allow you to visually verify what the agent is "baking" or "patching" in your site config files before the action is finalized.
-   **Consistency:** The same tools used by your Flutter/Next.js apps are now available to your AI agent.

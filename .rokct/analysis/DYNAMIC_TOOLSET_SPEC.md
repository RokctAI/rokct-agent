# Technical Specification: `FrappeDynamicToolset` & ERP Integration (done)

This document defines how Rokct Agent dynamically integrates with Frappe ERP logic using the "Bake" process and Hermes v0.7.0 features.

## 1. Dynamic Tool Discovery [DONE]

*   **Source:** `/home/frappe/frappe-bench/apps/rcore/rcore/platform/schemas/ai_tools.json`
*   **Trigger:** The `FrappeDynamicToolset` (in `tools/frappe_dynamic.py`) is triggered per message in `run_agent.py`.
*   **Method:**
    - Scan the JSON for OpenAI-style tool definitions.
    - Call `registry.register()` for each tool found.
    - Use a generic handler that routes calls to the Frappe Gateway.

## 2. Tool Execution Path [DONE]

When the LLM calls a dynamic tool (e.g., `erpnext:create_invoice`):
1.  **Hermes Registry:** Matches the tool name and dispatches to the handler.
2.  **Handler Logic:**
    ```python
    def execute_frappe_tool(cmd, payload):
        # cmd = "erpnext.create_invoice"
        # payload = { "customer": "ABC Corp", "amount": 100 }
        return frappe.call("rokct.platform.api.tenant", cmd=cmd, payload=payload)
    ```
3.  **Frappe Side:** `rcore.platform.api.execute_tenant` receives the command, validates it against the `api_manifest.json`, and executes the business logic.

## 3. Visual Verification (v0.7.0 Feature)

It is important to distinguish between **ERP Tool Calls** and **File System Mutations**:

### A. ERP Tool Calls (Database)
*   **Tools:** Baked assets like `erpnext:create_invoice`, `crm:update_lead`.
*   **Behavior:** These are direct calls to the Frappe API (`frappe.call`).
*   **Verification:** These do **not** produce file diffs. Verification is handled by the agent describing its action (e.g., "I have created Invoice #123 for you").

### B. Coding & Config Tasks (File System)
*   **Tools:** `patch`, `write_file`, `skill_manage`.
*   **Behavior:** Used when the agent is tasked with modifying the tenant's site configuration (e.g., `site_config.json`) or performing development work on the tenant's custom Frappe apps.
*   **v0.7.0 Inline Diffs:** For these specific file-system actions, the agent will render a unified diff in the WhatsApp chat. This allows the user to see exactly which lines of code or configuration are being changed before they send `/approve`.

## 4. Multi-App Scope
The "Bake" process in `rcore` ensures that tools from all installed apps (`erpnext`, `crm`, `lending`, `hrms`) are aggregated into the single `ai_tools.json`. This gives the agent a unified view of the entire ERP ecosystem.

---
*End of Specification*

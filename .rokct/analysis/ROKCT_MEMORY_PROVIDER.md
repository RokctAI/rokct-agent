# Technical Specification: `RokctMemoryProvider` Plugin [DONE] (done)

This document defines the implementation of the `RokctMemoryProvider` for Hermes Agent v0.7.0, bridging the agent's memory with the Frappe `brain` app.

## 1. Provider Overview

*   **Plugin Path:** `plugins/memory/rokct/`
*   **Target Backend:** Local Frappe Site (using `brain` app and `pgvector`).
*   **Philosophy:** The agent's memory *is* the Frappe database. No duplicate storage.

## 2. Interface Mapping

| Hermes Hook | Action | brain App API Call |
| :--- | :--- | :--- |
| `initialize()` | Warm up | `frappe.connect()` to local site. |
| `prefetch(query)` | Recall | `brain.api.semantic_search(query, limit=5)` |
| `sync_turn(user, asst)`| Persist | `brain.api.record_event` (log raw turn) + `brain.api.record_chat_summary` |
| `get_tool_schemas()` | Tools | Expose `search_engrams` and `record_user_fact`. |

## 3. Detailed Logic [DONE]

### A. Semantic Recall (`prefetch`)
When the user sends a message (e.g., "What was the quote for John?"), Hermes calls `prefetch`.
1.  Provider calls `semantic_search` on the local Frappe site.
2.  `brain` app performs `pgvector` search on `tabEngram`.
3.  Top results are returned to Hermes and injected into the system prompt as "Relevant Past Context".

### B. Turning History into Engrams (`sync_turn`)
After every agent response:
1.  Hermes calls `sync_turn`.
2.  Provider sends the user's message and the agent's response to `brain.api.record_event`.
3.  The `brain` app creates/updates an `Engram` linked to the current user.
4.  **Vectorization:** The `brain` app autonomously re-calculates the embedding for the updated Engram summary, ensuring the vector store is always fresh.

### C. Tenant Isolation
Since each `rokct-agent` runs inside a tenant container:
-   The provider uses `frappe.session.user` (resolved from the Hermes session `user_id`) to scope all API calls.
-   Data never leaves the tenant's PostgreSQL database.

## 4. Multi-Provider Context
As per Hermes v0.7.0 architecture, the `RokctMemoryProvider` will be the **single external provider** active in the `MemoryManager`. It will work alongside the built-in `MEMORY.md` (which can be used for ephemeral "scratchpad" memory).

---
*End of Specification*

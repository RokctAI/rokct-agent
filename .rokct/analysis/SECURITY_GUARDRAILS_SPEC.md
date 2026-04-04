# Technical Specification: Security & Subscription Guardrails (done)

This document defines the security and subscription-aware guardrails for the Rokct Agent platform.

## 1. Secret Redaction (v0.7.0 Security Engine)

We will extend Hermes's native `SecretExfiltrationBlocker` with Frappe-specific patterns to prevent the LLM from leaking platform credentials.

| Pattern Name | Regex Pattern (Conceptual) | Action |
| :--- | :--- | :--- |
| **Frappe SID** | `sid=[a-f0-9]{32}` | Redact from URLs and Responses |
| **API Token** | `token [a-f0-9]{15}:[a-f0-9]{15}`| Redact from tool output and chat |
| **Platform Secret**| `(?i)platform_sync_secret["']?\s*[:=]\s*["']?(\w+)` | Block exfiltration |

## 2. Subscription Interceptor

The Centralized WhatsApp Bridge will implement a "Pre-Flight" check for every user message.

### A. Active Subscription
- **Status:** `Active` or `Trialing`.
- **Action:** Forward to Tenant Agent.

### B. Suspended Subscription
- **Status:** `Dropped` or `Past Due`.
- **Action:**
    - Do NOT forward to Tenant Agent (save compute/tokens).
    - Send automated reply: *"Your Rokct.ai subscription is currently suspended. Please visit https://platform.rokct.ai to resume your service."*

### C. Archived/Deleted Tenant
- **Status:** `Deleted`.
- **Action:**
    - Call `control.api.notify_deleted_tenant(tenant_id)`.
    - Send archived notification.
    - Purge local WhatsApp session from the Bridge.

## 3. Sandboxing & Workspace Isolation [DONE]

*   **Workspace Mapping:** For each tenant, Hermes will be configured with a dedicated **`MESSAGING_CWD`** (e.g., `/home/frappe/frappe-bench/sites/{site}/workspace`).
*   **Restricted Access:** The agent will only be allowed to read/write within this subdirectory. It will NOT have permission to modify core Frappe site files or config files outside this path.
*   **Role-Based Logic:** The agent will verify the `app_role` from the local `site_config.json`. If `app_role == tenant`, all mutating file tools (like `patch` or `write_file` to core paths) will be hard-disabled at the registry level. [DONE]
*   **Execute Code:** All code execution tools will run inside the tenant's isolated Docker container, restricted to the tenant's workspace.

## 4. Resource Limits

*   **Token Budget:** Each tenant Hermes process will have a `max_iterations` and `iteration_budget` configured in its `config.yaml` based on their subscription tier (e.g., Lite: 10 turns/task, Pro: 50 turns/task).

---
*End of Specification*

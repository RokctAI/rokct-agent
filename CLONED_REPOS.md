# Ecosystem Structure

Repositories are maintained across **Frappenize** and **RokctAI** organizations. **Monorepo** has only the **main** branch, while others utilize the **rokct** branch for active development.

## 1. Core Framework & Platform

### [Monorepo (RokctAI)](https://github.com/RokctAI/Monorepo)
*   **Path:** `/home/jules/ecosystem/monorepo_pat`
*   **Role:** The primary project container. Holds private code that gets merged to corresponding apps by rpanel.
*   **Tree:**
    ```text
    monorepo_pat/
    ├── control/
    ├── rcore/
    ├── IoT/
    ├── handbook/
    └── MONOREPO_WHITELISTING.md
    ```

### [rcore (RokctAI)](https://github.com/RokctAI/rcore)
*   **Path:** `/home/jules/ecosystem/monorepo_pat/rcore`
*   **Role:** Foundational platform adapter.
*   **Tree:**
    ```text
    rcore/
    ├── rcore/
    │   ├── platform/
    │   │   ├── manager.py (Asset baking)
    │   │   ├── gateway.py (Tenant routing)
    │   │   ├── entity_groups.json (Intent mapping)
    │   │   └── schemas/
    │   │       └── ai_tools.json (Dynamic tools)
    │   └── api.py
    └── setup.py
    ```

### [bench (Frappenize)](https://github.com/Frappenize/bench)
*   **Path:** `/home/jules/ecosystem/bench`

### [frappe (Frappenize)](https://github.com/Frappenize/frappe)
*   **Path:** `/home/jules/ecosystem/frappe`

## 2. Intelligence & Storage

### [brain (RokctAI)](https://github.com/RokctAI/brain)
*   **Path:** `/home/jules/ecosystem/brain`
*   **Role:** Long-term memory and cognitive storage (pgvector).
*   **Tree:**
    ```text
    brain/
    ├── brain/
    │   ├── memory/
    │   │   └── doctype/
    │   │       ├── engram/ (Vectorized facts)
    │   │       └── engram_permission/
    │   ├── synaptic/ (Embedding logic)
    │   └── api.py (Semantic search)
    └── The-Rokct-Protocol (Protocol documentation)
    ```

## 3. Orchestration & Control

### [control (RokctAI)](https://github.com/RokctAI/control)
*   **Path:** `/home/jules/ecosystem/control_pat`
*   **Role:** Orchestration for multi-tenant Hermes instances. Found in control site only.

### [rpanel (RokctAI)](https://github.com/RokctAI/rpanel)
*   **Path:** `/home/jules/ecosystem/rpanel`

### [rpaas (RokctAI)](https://github.com/RokctAI/rpaas)
*   **Path:** `/home/jules/ecosystem/rpaas`

## 4. ERP Applications
*   [erpnext (Frappenize)](https://github.com/Frappenize/erpnext) - `/home/jules/ecosystem/erpnext`
*   [hrms (Frappenize)](https://github.com/Frappenize/hrms) - `/home/jules/ecosystem/hrms`
*   [lending (Frappenize)](https://github.com/Frappenize/lending) - `/home/jules/ecosystem/lending`
*   [payments (Frappenize)](https://github.com/Frappenize/payments) - `/home/jules/ecosystem/payments`
*   [crm (Frappenize)](https://github.com/Frappenize/crm) - `/home/jules/ecosystem/crm`

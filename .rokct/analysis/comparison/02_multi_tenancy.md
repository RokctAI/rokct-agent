# Comparison Point 2: Multi-Tenancy & Data Isolation (done)

| Feature | GoClaw (Fork) | Hermes Agent (v0.7.0) |
| :--- | :--- | :--- |
| **Primary Store** | **PostgreSQL (Multi-tenant)** | **SQLite (Profiles) or PostgreSQL (Plugin)** |
| **User Isolation** | `tenant_id` at DB level | **Profiles** or **Dynamically Scoped Plugin** |
| **API Key Storage** | Encrypted in DB (AES-256) | **Credential Pools** (auth.json) |
| **Concurrency** | Lane-based scheduling | **Sequential Tool Routing** (v0.7.0) |

### Discussion

#### GoClaw's Multi-Tenant Strength
GoClaw is designed for a SaaS model. Every row in the database (agents, tools, memory, cron) is scoped by a `tenant_id`. This allows you to host a "managed agent service" for multiple companies with absolute cryptographic and architectural isolation. 

#### Hermes Agent's Isolation Layers
Hermes provides two layers of isolation that perfectly map to your "Tenants vs. Teammates" requirement.

##### 1. Session Isolation (The "Teammate" Layer)
If two people message the **same** Hermes instance via WhatsApp:
- Hermes uses the **`chat_id`** (their phone number) to create a deterministic session key.
- **Result:** Person A and Person B have **completely separate conversation histories**. They cannot see each other's messages.
- **Teammates:** This is ideal for a single tenant where teammates share the same "Company Knowledge" (Skills/Memory) but have private chats with the agent.

##### 2. Profile Isolation (The "Tenant" Layer)
This addresses your request for `~/.hermes/profiles/{$tenant}/memories/`.
- By running Hermes with `--profile tenant_a`, it uses an entirely different folder for everything.
- **Isolation:** Memories, Skills, and even which LLM provider is used are 100% isolated.
- **Tenants:** This is the "Gold Standard" for multi-tenancy. Tenant A's memories can never leak to Tenant B because they are in different directories and potentially handled by different processes.

#### Deployment Strategy
| Level | Isolation Method | Best For |
| :--- | :--- | :--- |
| **Teammates** | Session-key (Single Profile) | Shared company context, private history. |
| **Tenants** | Native Profiles (`--profile`) | Absolute data/context separation. |

#### Scale Recommendation (v2026.4.3 Update)
With the latest **Pluggable Memory Provider Interface** and **Credential Pools** in Hermes Agent v0.7.0:

1.  **Unified Credential Management:**
    - Use **Same-Provider Credential Pools** to manage API keys for hundreds of tenants in a single Hermes instance. 
    - No need to spin up separate Docker containers for every tenant's keys.

2.  **`FrappeMemoryProvider` (pgvector):**
    - Implement a native memory plugin that connects directly to your rPanel PostgreSQL database.
    - **Isolation:** Scope searches by `tenant_id` at the SQL level, leveraging your existing `pgvector` investment.

3.  **Deployment Strategy:**
    - **Small Scale:** Use Hermes **Profiles** (`--profile {tenant}`) for absolute file-system isolation.
    - **Enterprise Scale:** Use a single Hermes Gateway with **Credential Pools** and the **`FrappeMemoryProvider`** to handle thousands of tenants dynamically via the session `user_id`.

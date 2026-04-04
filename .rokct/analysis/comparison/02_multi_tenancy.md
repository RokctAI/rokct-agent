# Comparison Point 2: Multi-Tenancy & Data Isolation

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **Primary Store** | **PostgreSQL (Multi-tenant)** | **SQLite (Per Profile)** |
| **User Isolation** | `tenant_id` at DB level | `session_key` at SQLite level |
| **API Key Storage** | Encrypted in DB (AES-256) | File-based `.env` or `auth.json` |
| **Concurrency** | Lane-based scheduling | Concurrent Python threads |

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
With the latest **Pluggable Memory Provider Interface** in Hermes Agent:
- You can now implement a **`FrappeMemoryProvider`** as a native plugin.
- This allows Hermes to use **pgvector** in your Frappe PostgreSQL database for memory, providing the same high-scale isolation as GoClaw.
- **Isolation:** You can scope vector searches using a `tenant_id` column, ensuring perfect data separation even within a single Hermes process.

For your Life Manager service:
- Start with **Native Profiles** for easy setup.
- Transition to a **Custom pgvector Provider** when you need to scale to thousands of tenants while keeping the superior Hermes learning loop.

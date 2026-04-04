# Comparison Point 3: Learning Loop & Memory

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **User Modeling** | None | **Honcho (Dialectic Modeling)** |
| **Skill Learning** | Manual | **Autonomous (Skill Creation)** |
| **Search Engine** | pgvector (Semantic) | FTS5 (SQLite Full Text) |
| **Persistence** | Database Records | Markdown Files (`MEMORY.md`) |

### Discussion

#### The "Self-Improving" Agent
This is Hermes's greatest strength for your **Life/Career Manager**.
- **Autonomous Skills:** After the agent completes a complex task (like generating a CV or planning a week), it can autonomously decide to save the "process" it discovered as a new Skill. This means the agent literally gets smarter the more you use it.
- **Honcho Modeling:** Hermes uses the Honcho dialectic system to "think" about you. It doesn't just store what you said; it builds a psychological model of your preferences, goals, and communication style.

#### GoClaw's Semantic Search
GoClaw is superior at **Semantic Retrieval**. Its use of `pgvector` allows the agent to find "similar" past experiences based on meaning rather than just keywords. Hermes relies on FTS5 (Full Text Search), which is extremely fast and reliable for keywords but less "intuitive" for broad conceptual searches.

#### v2026.4.3 Update: Pluggable Memory
The latest Hermes release introduces a **Pluggable Memory Provider Interface**. This means you no longer have to choose between GoClaw's "Better Search" and Hermes's "Growth."

You can now:
1.  Use the **Honcho** plugin for deep user modeling.
2.  Use a **Vector Store** plugin (like `mem0` or a custom `pgvector` provider) for high-accuracy semantic search.
3.  Register **both** at the same time to get the ultimate Life Manager foundation.

#### Recommendation
For a Life Manager, **Hermes Agent (v2026.4.3+)** is now the undisputed winner. It combines autonomous growth with the ability to plug into production-grade vector databases.

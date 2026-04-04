# Comparison Point 7: Multi-Agent Orchestration (done)

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **Philosophy** | Team-centric (Task Board) | Task-centric (Ephemeral Subagents) |
| **Delegation** | Explicit (Sync/Async links) | Dynamic (`delegate_task` tool) |
| **Communication**| Team Mailbox / Shared Board | Direct Tool Output / File sharing |
| **Isolation** | Shared Context Files | Fully Independent Sub-processes |

### Discussion

GoClaw's approach to multi-agent orchestration is built around the concept of "Agent Teams." It mimics a human office environment with a shared Kanban board (`team_tasks`) and formal communication channels. Agents have explicit permissions to delegate tasks to each other, making it ideal for persistent, long-running collaborative projects.

Hermes Agent uses a more dynamic, "on-demand" model. It allows the main agent to spawn ephemeral subagents to handle specific sub-tasks. These subagents are fully independent processes with their own toolsets and environments. This makes Hermes exceptionally good at parallelizing complex workflows (like "Search for X, then summarize while I perform Y") without the overhead of maintaining a permanent team structure.

For your **Life Manager** vision, Hermes's ability to spawn a specialized subagent for a quick task (e.g., "Subagent, go draft this invoice based on these achievements") while the main agent continues chatting with you is a powerful user experience.

**v0.7.0 Reasoning & Reliability:**
- **Thinking Persistence:** v0.7.0 preserves Anthropic thinking block signatures across tool-use turns, ensuring subagents don't "lose their train of thought" during complex delegations.
- **Death Spiral Prevention:** Improved handling of API disconnects during context compression ensures that parallel subagent tasks don't get stuck in infinite retry loops.

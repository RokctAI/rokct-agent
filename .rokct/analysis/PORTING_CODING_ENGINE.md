# Porting Strategy: SmartClaw Coding Engine to Hermes (Rokct Agent) (done)

This document outlines how we will port the advanced coding intelligence features from the Go-based SmartClaw to the Python-based Hermes Agent (v0.7.0), creating the **Rokct Agent**.

## 1. Architectural Mapper (The "Read-Only Expert")

**Go Feature:** `MapWorkspace()` identifies project roots (Frappe, Node, Go) and entry points.
**Hermes Implementation:** [DONE]
*   **Tool Name:** `workspace_map`
*   **Location:** `tools/rokct_mapper.py`
*   **Logic:** Reimplement the recursive directory walker in Python.
*   **v0.7.0 Advantage:** Use as a **ReadOnly Tool**. Instead of the agent guessing the file structure, it calls `workspace_map` once at the start of a session to see the "Big Picture."

## 2. Protocol & Rules Loader (The ".rokct" System)

**Go Feature:** `LoadProtocol()` and `loader.go` pull markdown rules and project context from a `.rokct` directory.
**Hermes Implementation:** [DONE]
*   **Mechanism:** Modify `agent/prompt_builder.py` to support a new `# ROKCT Protocol` section.
*   **Logic:** The agent will recursively scan the tenant's `.rokct/` directory (matching the structure seen in your Monorepo):
    - **`skills/`**: Automatically register skills found in `.rokct/skills/` as local Hermes skills.
    - **`workflows/`**: Inject active workflows (like `workspace_handshake.md`) into the system prompt.
    - **`project_map.md` / `decision_log.md`**: Inject these high-level context files into the "Project Context" section.
*   **Optimization:** Use Hermes's **Prompt Caching** to ensure this large protocol block doesn't increase per-turn costs.

## 3. Sophisticated Tool Loop Detection

**Go Feature:** `toolLoopState` tracks uniqueness ratios and read-only streaks to break infinite loops.
**Hermes Implementation:** [DONE]
*   **Location:** Integrate into `run_agent.py` within the `run_conversation` loop.
*   **Logic:** Port the Go thresholds (Warning at 3, Critical at 5) and the 0.6 uniqueness ratio logic.
*   **v0.7.0 Advantage:** If a loop is detected, Rokct Agent can use a **Subagent Delegation** to "step back" and analyze why it's stuck, then report a correction back to the main agent.

## 4. Execution & Verification Loop

**Go Feature:** `exec_output_cap.go` and `filesystem.go` handle sandboxed execution.
**Hermes Implementation:**
*   **Sandboxing:** Leverage Hermes's native **Docker environment**.
*   **Visual Trust:** For any development-mode file mutations, enforce **v0.7.0 Inline Diff Previews**. 
*   **Safe Mode:** By default, Rokct Agent will operate in "Safe Mode" for tenants, where it can propose code changes (with diffs) but requires user `/approve` on WhatsApp before applying them to the site.

## 5. Role-Based Access Control (Control vs. Tenant)

The Rokct Agent will automatically detect its environment by reading the local `site_config.json` (matching your `app_role` logic). [DONE]

*   **Control Site (`app_role: control`):**
    - **Full Coding Engine Enabled:** The agent has full access to structural editing, patching, and the `.rokct` protocol.
    - **Purpose:** Used for platform-wide maintenance and global development tasks.

*   **Tenant Site (`app_role: tenant`):**
    - **Restricted Mode:** Coding engine features (mutating file tools) are **disabled**. 
    - **Read-Only Mapping:** The `workspace_map` tool remains available as a "Read-Only" feature so the agent can understand the context without being able to modify site files.
    - **ERP-First:** The agent is restricted to standard ERP tools (`erpnext`, `crm`) and document writing within its designated workspace.

## 6. Deployment as a Plugin

To keep the Hermes core clean, the **Rokct Coding Engine** will be implemented as a specialized **Skill Pack**.
*   `skills/development/rokct-expert/SKILL.md`: Contains the high-level rules for Frappe development.
*   `skills/development/rokct-expert/tools/`: Contains the Python ports of the SmartClaw tools.

---
*End of Strategy*

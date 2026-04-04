# Comparison Point 6: Coding Engine Capabilities (done)

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **Architectural Insight**| **Native Mapper (Go/Frappe/Node)** | Basic File Tree |
| **Intent Management** | **Custom Intent Router** | Skill-based Routing |
| **Edit Methodology** | **`edit_structural` (Tree-sitter)**| String/Pattern Replace |
| **Protocol Support** | **ROKCT Protocol Native** | Markdown Skills |

### Discussion

#### GoClaw: The "Expert Architect"
Your custom GoClaw fork is actually **ahead of Hermes** in specific coding intelligence features.
- **Architectural Mapper:** Your `internal/coding/arch` code understands project roots and entry points for Frappe and Flutter. Hermes treats files as just "files."
- **Structural Editing:** Your `edit_structural` tool (which uses Tree-sitter in the roadmap) is more robust than simple pattern matching, as it understands the code's AST (Abstract Syntax Tree).
- **Intent Router:** Your `internal/agent/intent/router.go` performs a "pre-flight" check to restrict the agent to specific tools, saving tokens and preventing hallucinations.

#### Hermes: The "Reasoning Generalist"
Hermes relies on its high-level reasoning and extensive "Developer Skills" (`test-driven-development`, `systematic-debugging`) to solve coding tasks. It doesn't have a hardcoded "Intent Router"; instead, it trusts the agent to select the right skill.

#### Recommendation
When porting to Hermes, you should **bring these features with you**. You can reimplement your "Intent Router" and "Architectural Mapper" as Hermes Tools/Skills.

**v0.7.0 Opportunities:**
- **ACP Integration:** With v0.7.0, you can register your Architectural Mapper as an **MCP server** provided by your editor (VS Code/Zed). Hermes will pick it up automatically as a toolset.
- **Verification:** Use **Inline Diff Previews** to verify the structural edits proposed by your mapper before they are applied to the Frappe codebase.

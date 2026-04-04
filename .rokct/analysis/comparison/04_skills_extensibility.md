# Comparison Point 4: Skills & Extensibility

| Feature | GoClaw (Fork) | Hermes Agent |
| :--- | :--- | :--- |
| **Open Standards** | None | **agentskills.io compatible** |
| **Discovery** | Vector-based | **Progressive Disclosure** |
| **Runtime Hooks** | Limited | **Advanced (Setup/Pre-flight)** |
| **Sandboxing** | Docker (Internal) | Docker, Modal, Daytona, SSH |

### Discussion

#### Progressive Disclosure (Hermes)
Hermes solves the "Too many tools" problem using Progressive Disclosure. 
- The agent doesn't see 100 tools at once (which would confuse it and waste tokens). 
- It sees a "Table of Contents" of skills. 
- It can then "open" a specific skill (like `software-development`) to see the detailed tools and rules inside.
- This allows Hermes to support hundreds of specialized capabilities while remaining highly accurate.

#### agentskills.io Standard
Hermes uses the `agentskills.io` standard for its skills. This means you can easily download "Skill Packs" from the community or publish your own (e.g., a "Frappe Admin Pack"). GoClaw's skill format is proprietary to the repository.

#### Sandboxing Flexibility
Hermes supports multiple "Terminal Backends." You can tell Hermes to run its code execution in:
1.  **Local:** Your machine.
2.  **Docker:** An isolated container.
3.  **Modal:** Serverless cloud infrastructure.
4.  **Daytona:** Remote development environments.
This gives you extreme flexibility for where your "Life Manager" actually performs its work.

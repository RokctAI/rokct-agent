"""
ROKCT Protocol Loader

Loads markdown rules and project context from the .rokct directory.
"""

import os
from pathlib import Path
from typing import Dict, Optional

class RokctProtocol:
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path).resolve()
        self.rokct_path = self.workspace / ".rokct"
        self.rules: Dict[str, str] = {}
        self.is_healthy = False

    def load(self) -> bool:
        """Loads all .md and .txt files from the .rokct directory."""
        if not self.rokct_path.exists() or not self.rokct_path.is_dir():
            return False

        for root, dirs, files in os.walk(self.rokct_path):
            for file in files:
                if file.endswith((".md", ".txt")):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        rel_path = file_path.relative_to(self.rokct_path)
                        self.rules[str(rel_path)] = content
                    except Exception:
                        continue

        self.is_healthy = len(self.rules) > 0
        return self.is_healthy

    def format_for_prompt(self) -> str:
        """Returns the protocol rules as a formatted markdown string."""
        if not self.is_healthy:
            return ""

        lines = [
            "## GLOBAL WORKSPACE PROTOCOL (ROKCT)",
            "",
            "> This context is inherited from the Monorepo root and governs all development.",
            ""
        ]

        # Prioritize core files if they exist, then add others
        prioritized = ["README.md", "project_map.md", "decision_log.md"]
        seen = set()

        for filename in prioritized:
            if filename in self.rules:
                lines.append(f"### {filename}")
                lines.append("")
                lines.append(self.rules[filename])
                lines.append("")
                seen.add(filename)

        for filename, content in sorted(self.rules.items()):
            if filename not in seen:
                lines.append(f"### {filename}")
                lines.append("")
                lines.append(content)
                lines.append("")

        return "\n".join(lines)

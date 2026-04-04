"""
Rokct Workspace Mapper Tool

Identifies project roots, entry points, and configuration files within the workspace.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from tools.registry import registry

PROJECT_MOD = "mod"
PROJECT_NODE = "node"
PROJECT_FLUTTER = "flutter"
PROJECT_FRAPPE = "frappe"
PROJECT_PYTHON = "python"
PROJECT_UNKNOWN = "unknown"

SKIP_DIRS = {".git", "node_modules", ".next", "build", "dist", "vendor", "__pycache__", "venv"}

def detect_project_type(directory: Path) -> str:
    """Identifies the language/framework based on file presence."""
    if (directory / "main.go").exists() or (directory / "go.mod").exists():
        return PROJECT_MOD
    if (directory / "package.json").exists():
        return PROJECT_NODE
    if (directory / "pubspec.yaml").exists():
        return PROJECT_FLUTTER
    if (directory / "frappe-app.txt").exists():
        return PROJECT_FRAPPE
    if (directory / "requirements.txt").exists():
        return PROJECT_PYTHON
    return PROJECT_UNKNOWN

def is_entry_point(filename: str, project_type: str) -> bool:
    """Checks if a filename is a common entry point."""
    if project_type == PROJECT_MOD:
        return filename == "main.go"
    if project_type == PROJECT_NODE:
        return filename in ("index.js", "index.ts", "app.js")
    if project_type == PROJECT_FLUTTER:
        return filename == "main.dart"
    if project_type == PROJECT_PYTHON:
        return filename in ("app.py", "manage.py")
    return False

def is_config(filename: str) -> bool:
    """Checks if a filename is a configuration file."""
    return (filename.endswith((".env", ".yml", ".yaml", ".json")) or 
            filename in ("Makefile", "docker-compose.yml"))

def map_workspace(root_path: str = ".") -> str:
    """Scans the given path and identifies all project roots."""
    abs_root = Path(root_path).resolve()
    
    root_node = {
        "path": str(abs_root),
        "name": abs_root.name,
        "children": []
    }

    project_roots = []
    
    for root, dirs, files in os.walk(abs_root):
        current_path = Path(root)
        
        # Prune skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        pt = detect_project_type(current_path)
        if pt != PROJECT_UNKNOWN:
            project_roots.append(current_path)

    for rp in project_roots:
        rel_path = os.path.relpath(rp, abs_root)
        pt = detect_project_type(rp)
        
        node = {
            "path": rel_path if rel_path != "." else "",
            "name": rp.name,
            "type": pt,
            "is_root": True,
            "entry_points": [],
            "configs": []
        }
        
        try:
            for entry in os.scandir(rp):
                if entry.is_file():
                    if is_entry_point(entry.name, pt):
                        node["entry_points"].append(entry.name)
                    if is_config(entry.name):
                        node["configs"].append(entry.name)
        except OSError:
            pass
            
        root_node["children"].append(node)

    return json.dumps(root_node, indent=2)

registry.register(
    name="workspace_map",
    toolset="rokct-coding",
    schema={
        "name": "workspace_map",
        "description": "Recursively scans the workspace to identify project roots, entry points, and configuration files. Use this to understand the high-level architecture of the project.",
        "parameters": {
            "type": "object",
            "properties": {
                "root_path": {
                    "type": "string",
                    "description": "The root directory to start scanning from (default: '.')",
                    "default": "."
                }
            }
        }
    },
    handler=lambda args, **kw: map_workspace(args.get("root_path", ".")),
    emoji="🗺️"
)

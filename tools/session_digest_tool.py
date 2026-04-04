"""
Tool to generate a digest of active and idle gateway sessions.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from gateway.config import load_gateway_config
from gateway.session import SessionStore

logger = logging.getLogger(__name__)

def generate_session_digest(active_threshold_minutes: int = 60, format: str = "text") -> Any:
    """
    Generates a digest of current sessions.
    """
    try:
        config = load_gateway_config()
        from hermes_constants import get_hermes_home
        sessions_dir = get_hermes_home() / "sessions"
        
        store = SessionStore(sessions_dir, config)
        store._ensure_loaded()
        
        all_sessions = store.list_sessions()
        if not all_sessions:
            return "No sessions found."
            
        now = datetime.now()
        active = []
        idle = []
        
        threshold = now - timedelta(minutes=active_threshold_minutes)
        
        for entry in all_sessions:
            info = {
                "id": entry.session_id,
                "platform": entry.platform.value if entry.platform else "unknown",
                "user": entry.origin.user_name if entry.origin else "unknown",
                "last_active": entry.updated_at,
                "tokens": entry.total_tokens,
                "display_name": entry.display_name or entry.session_id[:12]
            }
            if entry.updated_at >= threshold:
                active.append(info)
            else:
                idle.append(info)
                
        if format == "card":
            rows = []
            for s in active[:3]:
                rows.append(f"🟢 {s['display_name']}")
            for s in idle[:3]:
                diff = now - s['last_active']
                hours = int(diff.total_seconds() // 3600)
                time_str = f"{hours}h" if hours > 0 else f"{int(diff.total_seconds() // 60)}m"
                rows.append(f"🔴 {s['display_name']} {time_str}")
            
            return {
                "title": "⚕ Your Sessions",
                "rows": rows,
                "footer": f"{len(active)} active / {len(idle)} idle"
            }

        lines = ["# 📊 Session Digest\n"]
        if active:
            lines.append("## 🔥 Active Sessions (Last hour)")
            for s in active:
                lines.append(f"- **{s['user']}** ({s['platform']}): `{s['id'][:8]}` - {s['tokens']} tokens")
            lines.append("")
        if idle:
            lines.append("## 😴 Idle Sessions")
            for s in idle[:5]:
                lines.append(f"- **{s['user']}** ({s['platform']}): `{s['id'][:8]}` (Last active: {s['last_active'].strftime('%H:%M')})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error generating digest: {e}"

def session_digest_tool() -> str:
    """Tool entry point."""
    digest = generate_session_digest()
    return json.dumps({"success": True, "digest": digest})

if __name__ == "__main__":
    print(generate_session_digest())

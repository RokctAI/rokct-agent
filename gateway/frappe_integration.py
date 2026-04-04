"""
Frappe integration for Hermes Gateway.
Handles calling Frappe APIs for ambient capture storage.
"""

import os
import json
import logging
import httpx
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

import time

OFFLINE_QUEUE_PATH = Path(os.path.expanduser("~/.hermes/frappe_queue.json"))

async def call_frappe_api(cmd: str, payload: Dict[str, Any], chat_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the Frappe gateway (tenant or control).
    Always use rokct aliases.
    """
    from hermes_constants import get_rokct_app_role
    
    base_url = os.getenv("FRAPPE_BASE_URL")
    api_key = os.getenv("FRAPPE_API_KEY")
    api_secret = os.getenv("FRAPPE_API_SECRET")
    
    if not all([base_url, api_key, api_secret]):
        logger.debug("Frappe credentials missing, simulating success.")
        return {"success": True, "message": "Simulated success (missing credentials)"}

    app_role = get_rokct_app_role()
    gateway = "rokct.platform.api.control" if app_role == "control" else "rokct.platform.api.tenant"
    url = f"{base_url.rstrip('/')}/api/method/{gateway}"
    
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }
    body = {"cmd": cmd, "payload": payload}

    async def do_call():
        async with httpx.AsyncClient() as client:
            return await client.post(url, json=body, headers=headers, timeout=30.0)

    try:
        response = await do_call()
        
        # Handle Validation Errors (4xx)
        if 400 <= response.status_code < 500:
            try:
                error_data = response.json()
                error_msg = error_data.get("message") or error_data.get("error") or "Validation error"
            except Exception:
                error_msg = response.text or "Validation error"
            return {"success": False, "error": error_msg, "type": "validation"}

        # Handle Transient Errors (5xx or timeout) - Retry once
        if response.status_code >= 500:
            logger.warning("Transient error %s, retrying in 3s...", response.status_code)
            await asyncio.sleep(3)
            response = await do_call()
            if response.status_code >= 500:
                if chat_id:
                    _queue_failed_call(cmd, payload, chat_id)
                return {"success": False, "error": "Server error after retry", "type": "transient"}

        response.raise_for_status()
        return response.json()

    except (httpx.ConnectError, httpx.TimeoutException) as e:
        logger.error("Frappe unreachable: %s", e)
        if chat_id:
            _queue_failed_call(cmd, payload, chat_id)
        return {"success": False, "error": "Saved locally — will sync when Frappe is back online", "type": "offline"}
    except Exception as e:
        logger.error("Frappe API call failed: %s", e)
        return {"success": False, "error": str(e)}

def _queue_failed_call(cmd: str, payload: dict, chat_id: str):
    """Save failed call to local offline queue."""
    queue = []
    if OFFLINE_QUEUE_PATH.exists():
        try:
            queue = json.loads(OFFLINE_QUEUE_PATH.read_text())
        except Exception:
            queue = []
    
    queue.append({
        "timestamp": time.time(),
        "cmd": cmd,
        "payload": payload,
        "chat_id": chat_id
    })
    
    OFFLINE_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    OFFLINE_QUEUE_PATH.write_text(json.dumps(queue, indent=2))

async def capture_to_frappe(intent: str, content: str, user_id: str, platform: str, chat_id: str) -> Dict[str, Any]:
    """
    Routes an ambient capture through the Frappe gateway.
    """
    method_map = {
        "reminder": "platform:create_reminder",
        "task": "platform:create_task",
        "note": "platform:create_note"
    }
    
    method = method_map.get(intent)
    if not method:
        return {"success": False, "error": f"Unknown intent: {intent}"}
        
    payload = {
        "content": content,
        "user": user_id,
        "platform": platform,
        "metadata": {
            "source": "hermes_ambient_capture",
            "intent": intent
        }
    }
    
    return await call_frappe_api(method, payload, chat_id=chat_id)

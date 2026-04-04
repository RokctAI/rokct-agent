"""
Ambient capture logic for Hermes Gateway.
Classifies messages without wake phrases into Reminders, Notes, or Tasks.
"""

import logging
import json
import re
from typing import Optional, Dict, Any
from gateway.platforms.base import MessageEvent

logger = logging.getLogger(__name__)

# Intent patterns for classification (fallback if transformer is unavailable)
INTENT_PATTERNS = {
    "reminder": [
        r"remind me (to|about|that)",
        r"don't forget to",
        r"remember to",
        r"at \d{1,2}(:\d{2})?\s*(am|pm)?",
        r"in \d+ (minute|hour|day)",
    ],
    "task": [
        r"todo:",
        r"add task",
        r"i need to",
        r"task:",
        r"must do",
    ],
    "note": [
        r"note:",
        r"capture this:",
        r"save this",
        r"write down",
    ]
}

async def classify_intent(text: str) -> str:
    """
    Classify the intent of the message.
    Uses Sentence Transformers if available, otherwise fallback to patterns.
    """
    try:
        from sentence_transformers import SentenceTransformer, util
        # This assumes a model is pre-loaded or cached. 
        # Using a small, fast model for gateway classification.
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        choices = ["reminder", "task", "note", "general chat"]
        text_emb = model.encode(text, convert_to_tensor=True)
        choice_embs = model.encode(choices, convert_to_tensor=True)
        
        scores = util.cos_sim(text_emb, choice_embs)[0]
        max_idx = scores.argmax().item()
        
        if scores[max_idx] > 0.4:
            return choices[max_idx]
    except Exception as e:
        logger.debug("SentenceTransformer classification failed, using patterns: %s", e)

    lowered = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        if any(re.search(p, lowered) for p in patterns):
            return intent
            
    return "general chat"

async def handle_ambient_capture(runner, event: MessageEvent) -> Optional[str]:
    """
    Handles messages that did not trigger the wake phrase.
    """
    text = event.text.strip()
    if not text:
        return None

    intent = await classify_intent(text)
    
    if intent == "general chat":
        # Ignore non-intent ambient noise
        return None

    # Handle Confirmation Loop
    platform_name = event.source.platform.value
    adapter = runner.adapters.get(event.source.platform)
    
    if not adapter:
        return None

    # Confirmation message
    confirmation_msg = f"💡 I've detected a **{intent}**. Should I capture this?\n\n> {text}\n\nReply with \"yes\" to confirm, or ignore to skip."
    
    # Store for confirmation in session store
    session_key = runner._session_key_for_source(event.source)
    runner._pending_approvals[session_key] = {
        "type": "ambient_capture",
        "intent": intent,
        "content": text,
        "event": event
    }

    await adapter.send(event.source.chat_id, confirmation_msg)
    return None

async def process_confirmed_capture(runner, session_key: str, choice: str) -> Optional[str]:
    """
    Processes a capture after user confirms it.
    """
    pending = runner._pending_approvals.pop(session_key, None)
    if not pending or pending.get("type") != "ambient_capture":
        return None

    if choice.lower() != "yes":
        return "Okay, I've ignored that capture."

    intent = pending["intent"]
    content = pending["content"]
    event = pending["event"]

    # Here we would integrate with Frappe/ERPNext
    # For now, we'll simulate a successful capture and scheduling
    
    from gateway.frappe_integration import capture_to_frappe
    success = await capture_to_frappe(
        intent=intent,
        content=content,
        user_id=event.source.user_id,
        platform=event.source.platform.value
    )

    if success:
        if intent == "reminder":
            # Also schedule a formal Hermes Cron Job for the reminder delivery
            try:
                from cron.jobs import create_job
                # Simple heuristic: if user said "in 5 minutes", we should parse it.
                # For now, we'll default to a 1-hour reminder if not parsed.
                # In a real scenario, we'd use the agent to parse the time.
                schedule = "1h" 
                if "minute" in content:
                    match = re.search(r"(\d+)\s*minute", content)
                    if match: schedule = f"{match.group(1)}m"
                elif "hour" in content:
                    match = re.search(r"(\d+)\s*hour", content)
                    if match: schedule = f"{match.group(1)}h"

                create_job(
                    prompt=f"Pinging you about your reminder: {content}",
                    schedule=schedule,
                    name=f"Reminder: {content[:20]}",
                    repeat=1,
                    deliver="origin",
                    origin=event.source.to_dict()
                )
            except Exception as e:
                logger.error("Failed to schedule reminder cron job: %s", e)

            return f"✅ Reminder set! I'll ping you here when it's time."
        elif intent == "task":
            return f"✅ Task added to your list."
        else:
            return f"✅ Note saved."
    else:
        return f"⚠️ I tried to save that {intent}, but I had trouble connecting to the backend. Please try again later!"

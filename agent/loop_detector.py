"""
Tool Loop Detection Middleware

Tracks recent tool calls to detect and break infinite loops.
"""

import hashlib
import json
import logging
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)

HISTORY_SIZE = 30
WARNING_THRESHOLD = 3
CRITICAL_THRESHOLD = 5

READ_ONLY_WARNING = 8
READ_ONLY_CRITICAL = 12

READ_ONLY_EXPLORATION_WARNING = 24
READ_ONLY_EXPLORATION_CRITICAL = 36

READ_ONLY_UNIQUENESS_THRESHOLD = 0.6

SAME_RESULT_WARNING = 4
SAME_RESULT_CRITICAL = 6

MUTATING_TOOLS = {
    "write_file", "patch", "edit", "edit_file",
    "spawn", "message", "create_image", "create_video",
    "create_audio", "text_to_speech", "cron", "publish_skill",
    "sessions_send"
}

class ToolCallRecord:
    def __init__(self, tool_name: str, args_hash: str):
        self.tool_name = tool_name
        self.args_hash = args_hash
        self.result_hash: Optional[str] = None

class LoopDetector:
    def __init__(self):
        self.history: List[ToolCallRecord] = []
        self.read_only_streak = 0
        self.seen_read_args = set()
        self.read_only_unique = 0
        self.consecutive_errors = 0

    def record_call(self, tool_name: str, args: Dict[str, Any]) -> str:
        args_hash = self.hash_args(tool_name, args)
        self.history.append(ToolCallRecord(tool_name, args_hash))
        if len(self.history) > HISTORY_SIZE:
            self.history = self.history[-HISTORY_SIZE:]
        
        self._update_mutation_state(tool_name, args)
        return args_hash

    def record_result(self, args_hash: str, result: str):
        res_hash = self._hash_result(result)
        for record in reversed(self.history):
            if record.args_hash == args_hash and record.result_hash is None:
                record.result_hash = res_hash
                break
        
        # Check for errors (naive heuristic)
        is_error = '"error"' in result.lower() or result.lower().startswith("error")
        if is_error:
            self.consecutive_errors += 1
        else:
            self.consecutive_errors = 0

    def detect(self, tool_name: str, args_hash: str) -> Tuple[Optional[str], Optional[str]]:
        """Returns (level, message) if a loop is detected."""
        results = []

        # 1. Consecutive errors (Highest priority)
        if self.consecutive_errors >= 3:
            results.append(("critical", "CRITICAL ERROR THRESHOLD REACHED: 3 consecutive tool failures. Please realign your strategy."))

        # 2. Direct Repetition (Same args, Same result)
        no_progress_count = 0
        last_result_hash = None

        for record in reversed(self.history):
            if record.args_hash != args_hash:
                continue
            if record.result_hash is None:
                continue
            if last_result_hash is None:
                last_result_hash = record.result_hash
            if record.result_hash == last_result_hash:
                no_progress_count += 1

        if no_progress_count >= CRITICAL_THRESHOLD:
            results.append(("critical", f"CRITICAL: {tool_name} has been called {no_progress_count} times with identical arguments and results. Stopping to prevent runaway loop."))
        elif no_progress_count >= WARNING_THRESHOLD:
            results.append(("warning", f"[System: WARNING — {tool_name} has been called {no_progress_count} times with the same arguments and identical results. This is not making progress. Try a completely different approach.]"))

        # 3. Read-only streaks
        streak_level, streak_msg = self._detect_read_only_streak()
        if streak_level:
            results.append((streak_level, streak_msg))

        if not results:
            return None, None

        # Return the most severe result
        for level in ["critical", "warning"]:
            for r_level, r_msg in results:
                if r_level == level:
                    return r_level, r_msg
        
        return None, None

    def _detect_read_only_streak(self) -> Tuple[Optional[str], Optional[str]]:
        if self.read_only_streak < READ_ONLY_WARNING:
            return None, None

        unique_ratio = self.read_only_unique / self.read_only_streak if self.read_only_streak > 0 else 0

        if unique_ratio > READ_ONLY_UNIQUENESS_THRESHOLD:
            if self.read_only_streak >= READ_ONLY_EXPLORATION_CRITICAL:
                return "critical", f"CRITICAL: {self.read_only_streak} consecutive read-only calls. Summarize findings before reading more."
            elif self.read_only_streak >= READ_ONLY_EXPLORATION_WARNING:
                return "warning", f"[System: You have read {self.read_only_streak} files. Please summarize what you learned.]"
        else:
            if self.read_only_streak >= READ_ONLY_CRITICAL:
                return "critical", f"CRITICAL: {self.read_only_streak} consecutive read-only calls (stuck). Making no progress."
            elif self.read_only_streak >= READ_ONLY_WARNING:
                return "warning", f"[System: WARNING — {self.read_only_streak} consecutive read-only calls. Stop re-reading and take action.]"
        
        return None, None

    def _update_mutation_state(self, tool_name: str, args: Dict[str, Any]):
        if tool_name in MUTATING_TOOLS:
            self.read_only_streak = 0
            self.read_only_unique = 0
            self.seen_read_args = set()
            return

        if tool_name in {"terminal", "execute_code", "bash"}:
            # Neutral tools
            return

        self.read_only_streak += 1
        args_hash = self.hash_args(tool_name, args)
        if args_hash not in self.seen_read_args:
            self.seen_read_args.add(args_hash)
            self.read_only_unique += 1

    def hash_args(self, tool_name: str, args: Dict[str, Any]) -> str:
        s = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        return hashlib.sha256(s.encode()).hexdigest()[:32]

    def _hash_result(self, result: str) -> str:
        return hashlib.sha256(result.encode()).hexdigest()[:32]

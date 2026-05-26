"""Trigger matching and execution engine."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Trigger:
    trigger_type: str
    trigger_text: str
    action_type: str
    action_value: str | None
    stop_on_match: bool = False


def matches_condition(text: str, trigger: Trigger) -> bool:
    text = text or ""
    pattern = trigger.trigger_text
    if pattern.startswith("*") and pattern.endswith("*") and len(pattern) > 2:
        return pattern[1:-1].lower() in text.lower()
    if pattern.endswith("*") and not pattern.startswith("*"):
        return text.lower().startswith(pattern[:-1].lower())
    if pattern.startswith("*") and not pattern.endswith("*"):
        return text.lower().endswith(pattern[1:].lower())
    if trigger.trigger_type == "contains":
        return pattern.lower() in text.lower()
    if trigger.trigger_type == "exact":
        return text.strip().lower() == pattern.strip().lower()
    if trigger.trigger_type == "starts_with":
        return text.lower().startswith(pattern.lower())
    if trigger.trigger_type == "ends_with":
        return text.lower().endswith(pattern.lower())
    if trigger.trigger_type == "regex":
        return bool(re.search(pattern, text, flags=re.IGNORECASE))
    return False


def parse_actions(trigger: Trigger) -> list[tuple[str, str | None]]:
    return [(a.strip(), trigger.action_value) for a in trigger.action_type.split(",") if a.strip()]

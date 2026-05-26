"""XP and leveling logic."""
from __future__ import annotations

import random

LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000,
    11: 15000,
    12: 20000,
}


def calculate_xp(message, has_user_sent_today: bool) -> int:
    xp = random.randint(1, 5)
    if getattr(message, "text", None):
        xp += len(message.text) // 100
    if getattr(message, "photo", None) or getattr(message, "video", None):
        xp += 2
    if not has_user_sent_today:
        xp += 10
    return min(xp, 10)


def level_for_xp(xp: int) -> int:
    levels = sorted(LEVEL_THRESHOLDS.items(), key=lambda x: x[1])
    current = 1
    for lvl, threshold in levels:
        if xp >= threshold:
            current = lvl
    while xp >= LEVEL_THRESHOLDS.get(current, 20000) + (current * 2500):
        current += 1
    return current

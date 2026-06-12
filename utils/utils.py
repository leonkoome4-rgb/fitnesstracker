from datetime import datetime
from typing import Tuple


def parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Date must be YYYY-MM-DD")


def is_lower_better(test_name: str) -> bool:
    n = test_name.lower()
    speed_keywords = ["sprint", "m", "sec", "seconds", "time", "40m", "100m", "200m"]
    for k in speed_keywords:
        if k in n:
            return True
    return False


def compute_improvement(prev: float, curr: float, lower_is_better: bool) -> Tuple[float, float, str]:
    # returns (difference, percent_change, status)
    if prev == 0:
        percent = float('inf')
    else:
        percent = (curr - prev) / abs(prev) * 100.0
    improved = (curr < prev) if lower_is_better else (curr > prev)
    status = "Improved" if improved else "Declined" if curr != prev else "No change"
    return curr - prev, percent, status

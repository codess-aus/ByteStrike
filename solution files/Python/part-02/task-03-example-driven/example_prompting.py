from datetime import datetime
from typing import List


def format_names(names: List[str]) -> List[str]:
    # Example: ["alice", "bob"] -> ["ALICE", "BOB"]
    return [name.upper() for name in names]


def format_dates(dates: List[str]) -> List[str]:
    # Using the same pattern as format_names above:
    # Example: ["2026-01-17", "2026-02-20"] -> ["Jan 17, 2026", "Feb 20, 2026"]
    return [datetime.strptime(d, "%Y-%m-%d").strftime("%b %d, %Y") for d in dates]

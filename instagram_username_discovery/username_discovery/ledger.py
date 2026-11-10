"""CSV ledger helpers. No network requests are made by this module."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from .generator import generate_candidates, is_syntactically_valid

FIELDS = [
    "username",
    "length",
    "format_valid",
    "profile_url",
    "evidence_status",
    "association",
    "source_url",
    "checked_at",
    "notes",
]
DEFAULT_STATUS = "NOT_CHECKED"


def profile_url(username: str) -> str:
    return "https://www.instagram.com/" + quote(username, safe="") + "/"


def export_candidates(
    output: str | Path,
    min_length: int = 2,
    max_length: int = 2,
) -> int:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for username in generate_candidates(min_length, max_length):
            writer.writerow({
                "username": username,
                "length": len(username),
                "format_valid": str(is_syntactically_valid(username)).lower(),
                "profile_url": profile_url(username),
                "evidence_status": DEFAULT_STATUS,
                "association": "",
                "source_url": "",
                "checked_at": "",
                "notes": "",
            })
            count += 1
    return count


def validate_csv(path: str | Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = set(FIELDS) - set(reader.fieldnames or [])
        if missing:
            return 0, [f"Missing columns: {', '.join(sorted(missing))}"]
        for line_number, row in enumerate(reader, start=2):
            count += 1
            username = row["username"]
            if not is_syntactically_valid(username):
                errors.append(f"Line {line_number}: invalid username syntax: {username!r}")
            if row["length"] != str(len(username)):
                errors.append(f"Line {line_number}: length mismatch for {username!r}")
    return count, errors


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

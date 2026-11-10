"""Candidate generation and preliminary syntax validation."""

from __future__ import annotations

from itertools import product
import string
from typing import Iterator

LETTERS = string.ascii_lowercase
DIGITS = string.digits
UNDERSCORE = "_"
PERIOD = "."
DEFAULT_ALPHABET = LETTERS + DIGITS + UNDERSCORE
ALL_DOCUMENTED_CHARACTERS = LETTERS + DIGITS + UNDERSCORE + PERIOD


def is_syntactically_valid(username: str) -> bool:
    """Apply conservative common Instagram username syntax checks.

    This is not an Instagram registration/availability check.
    """
    if not isinstance(username, str):
        return False
    if not 1 <= len(username) <= 30:
        return False
    if username.startswith(".") or username.endswith("."):
        return False
    if ".." in username:
        return False
    return all(ch in ALL_DOCUMENTED_CHARACTERS for ch in username)


def generate_candidates(
    min_length: int = 2,
    max_length: int = 2,
    alphabet: str = DEFAULT_ALPHABET,
) -> Iterator[str]:
    """Yield every syntactically valid candidate in deterministic order."""
    if min_length < 1 or max_length > 30 or min_length > max_length:
        raise ValueError("Require 1 <= min_length <= max_length <= 30")
    if not alphabet:
        raise ValueError("alphabet must not be empty")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet must not contain duplicate characters")
    if any(ch not in ALL_DOCUMENTED_CHARACTERS for ch in alphabet):
        raise ValueError("alphabet contains characters outside the supported set")

    for length in range(min_length, max_length + 1):
        for chars in product(alphabet, repeat=length):
            candidate = "".join(chars)
            if is_syntactically_valid(candidate):
                yield candidate


def two_character_count() -> int:
    """Count the default two-character search space."""
    return sum(1 for _ in generate_candidates(2, 2))

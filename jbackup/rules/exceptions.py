from __future__ import annotations

class MissingError(LookupError):
    "Error for 'Missing X' cases."

class MissingSectionError(MissingError):
    """Missing section in a rule file."""

class MissingOptionError(MissingError):
    """An error raised when an option does not exist."""

class RuleParserError(Exception):
    """An error raised while parsing a rule file."""

"""Rule configurations."""

class MissingSectionError(LookupError):
    """Missing section in a rule file."""

class RuleParserError(Exception):
    """An error raised while parsing a rule file."""

class MissingOptionError(LookupError):
    """An error raised when an option does not exist."""

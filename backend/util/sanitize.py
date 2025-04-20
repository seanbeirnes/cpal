import re
import html
import unicodedata

MAX_LEN = 1000

class QueryLengthError(Exception):
    """Custom exception to indicate a query exceed the max length allowed."""

class InjectionError(Exception):
    """Custom exception to indicate a potential injection attack."""
    pass

def sanitize_query(query: str) -> str:
    """
    Sanitize a user input string to reduce the risk of prompt injection
    or malicious content being sent to a language model.
    """

    # 1. Normalize Unicode form and unescape HTML entities early.
    query = unicodedata.normalize("NFKC", query)
    query = html.unescape(query)

    # 2. Improved Injection Pattern Matching (case-insensitive, whole word).
    injection_patterns = [
        r"(?i)\b(:?ignore|disregard|forget)\s+(?:\w+\s+?){0,2}previous\s+instructions\b",
        r"(?i)\b(:?ignore|disregard|forget)\s+.*\s+above\b",
        r"(?i)\bpretend\s+to\s+be\b",
        r"(?i)\byou\s+are\s+now\b",
        r"(?i)\bact\s+as\b",
        r"(?i)\bsimulate\s+being\b",
        r"(?i)\bsystem\s+message\b",
        r"(?i)<script[^>]*>.*?<\/script>",
    ]
    for pattern in injection_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            raise InjectionError("Potential prompt injection detected.")

    query = "".join(ch for ch in query if ch.isprintable())

    query = html.escape(query)

    max_length = 1000
    if len(query) > max_length:
        raise QueryLengthError("Query exceeds maximum characters")

    return query

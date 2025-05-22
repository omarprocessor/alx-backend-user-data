#!/usr/bin/env python3
"""
Provides a function to obfuscate specified fields in a log message.
"""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """Returns the obfuscated log message."""
    return re.sub(f"({'|'.join(fields)})=.*?{separator}",
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)

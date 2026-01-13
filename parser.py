"""
MIT License
Copyright (c) 2026 antoniooreany
Licensed under the MIT License. See the LICENSE file for details.
"""

"""parser.py

Functions to parse a keys/list file that describes which directories/packages
should be kept/copied. The parser is intentionally permissive: it accepts
one identifier per line (ignoring comments and blank lines) or multiple
identifiers separated by commas or whitespace on a single line.

Exports:
- parse_keys_from_file(path)
- parse_keys_from_text(text)
"""
from typing import Set, Iterable
import re
import logging


_DEFAULT_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-./]+")


def _split_tokens(line: str) -> Iterable[str]:
    # Strip comments starting with '#'
    line = line.split("#", 1)[0].strip()
    if not line:
        return []
    # Allow comma-separated or whitespace separated tokens
    parts = re.split(r"[,\s]+", line)
    return [p.strip() for p in parts if p.strip()]


def parse_keys_from_text(text: str) -> Set[str]:
    """
    Parse keys from a raw text input. Ignores empty lines and comments (#).
    Returns a set of unique keys.
    """
    keys = set()
    for raw_line in text.splitlines():
        for token in _split_tokens(raw_line):
            m = _DEFAULT_TOKEN_RE.fullmatch(token)
            if m:
                keys.add(token)
            else:
                logging.debug("Skipping token that doesn't match pattern: %s", token)
    return keys


def parse_keys_from_file(path: str) -> Set[str]:
    """
    Read a file and parse keys using parse_keys_from_text.
    """
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    return parse_keys_from_text(content)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse a keys file and print tokens.")
    parser.add_argument("file", help="Path to the file containing keys")
    args = parser.parse_args()
    keys = parse_keys_from_file(args.file)
    for k in sorted(keys):
        print(k)

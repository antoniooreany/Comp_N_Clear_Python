"""
MIT License
Copyright (c) 2026 antoniooreany
Licensed under the MIT License. See the LICENSE file for details.
"""

"""main.py

Top-level runner that wires together parser, deleter and copier.

Usage examples:
  python main.py --source /path/to/src --dest /path/to/target --list keys.txt
  python main.py --source repoA --dest repoB --list keys.txt --exclude .git,__pycache__ --dry-run
"""
import argparse
import logging
import sys
from typing import List

from parser import parse_keys_from_file
from deleter import remove_unlisted_dirs
from copier import copy_keys_from_source


def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Migrate Comp_N_Clear Java logic into Python: clean target and copy selected keys from a source."
    )
    p.add_argument("--source", "-s", required=True, help="Source root directory (contains key subdirectories).")
    p.add_argument("--dest", "-d", required=True, help="Destination root directory to clean and populate.")
    p.add_argument("--list", "-l", required=True, help="File that lists keys to keep/copy (one per line).")
    p.add_argument(
        "--exclude",
        "-e",
        default="",
        help="Comma-separated list of filename patterns to exclude (e.g. '.git,__pycache__').",
    )
    p.add_argument("--dry-run", action="store_true", help="Do not perform destructive actions; just log them.")
    p.add_argument("--verbose", "-v", action="count", default=0, help="Increase logging verbosity.")
    return p.parse_args(argv)


def _configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main(argv=None):
    args = _parse_args(argv or sys.argv[1:])
    _configure_logging(args.verbose)

    keys = parse_keys_from_file(args.list)
    if not keys:
        logging.error("No keys were parsed from %s; aborting.", args.list)
        return 2

    exclude_patterns = [p for p in (args.exclude or "").split(",") if p]

    logging.info("Parsed %d keys from list.", len(keys))
    logging.debug("Keys: %s", sorted(keys))

    # Step 1: Remove unlisted directories from destination
    removed = remove_unlisted_dirs(args.dest, keys, dry_run=args.dry_run)
    logging.info("Removed directories: %s", ", ".join(sorted(removed)) if removed else "<none>")

    # Step 2: Copy listed keys from source to destination
    copy_keys_from_source(args.source, args.dest, keys, exclude_names=exclude_patterns, dry_run=args.dry_run)
    logging.info("Completed operation (dry-run=%s).", args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

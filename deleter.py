"""
MIT License
Copyright (c) 2026 antoniooreany
Licensed under the MIT License. See the LICENSE file for details.
"""

"""deleter.py

Remove directories from a target root that are not present in a whitelist/set.
Provides a dry-run option.

Functions:
- remove_unlisted_dirs(dest_root, keep_keys, dry_run=False)
"""
import os
import shutil
import logging
from typing import Iterable, Set


def remove_unlisted_dirs(dest_root: str, keep_keys: Iterable[str], dry_run: bool = False) -> Set[str]:
    """
    Remove directories inside dest_root that are not present in keep_keys.
    Returns a set of directories that were removed (or would be removed in dry-run).
    """
    keep_set = set(keep_keys)
    removed = set()

    if not os.path.exists(dest_root):
        logging.warning("Destination root does not exist: %s", dest_root)
        return removed

    for name in os.listdir(dest_root):
        path = os.path.join(dest_root, name)
        if not os.path.isdir(path):
            logging.debug("Skipping non-directory in dest_root: %s", path)
            continue
        if name not in keep_set:
            if dry_run:
                logging.info("[dry-run] Would remove directory: %s", path)
                removed.add(name)
            else:
                logging.info("Removing directory: %s", path)
                try:
                    shutil.rmtree(path)
                    removed.add(name)
                except Exception as exc:
                    logging.exception("Failed to remove %s: %s", path, exc)
    return removed

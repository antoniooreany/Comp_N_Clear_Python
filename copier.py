"""
MIT License
Copyright (c) 2026 antoniooreany
Licensed under the MIT License. See the LICENSE file for details.
"""

"""copier.py

Responsible for copying source directories (or their contents) into a
destination, with support for exclude patterns and dry-run mode.

Functions:
- copy_directory_contents(src_dir, dest_dir, exclude_names=None, dry_run=False)
- copy_keys_from_source(source_root, dest_root, keys, exclude_names=None, dry_run=False)
"""
import os
import shutil
import fnmatch
import logging
from typing import Iterable, Optional


def _should_exclude(name: str, exclude_patterns: Optional[Iterable[str]]) -> bool:
    if not exclude_patterns:
        return False
    for pat in exclude_patterns:
        if fnmatch.fnmatch(name, pat):
            return True
    return False


def copy_directory_contents(
    src_dir: str,
    dest_dir: str,
    exclude_names: Optional[Iterable[str]] = None,
    dry_run: bool = False,
) -> None:
    """
    Copy the contents of src_dir into dest_dir. Existing dest_dir will be created
    if needed. Files or directories that match any pattern in exclude_names
    will be skipped.

    exclude_names are shell-style patterns (fnmatch).
    """
    if not os.path.exists(src_dir):
        logging.warning("Source does not exist, skipping copy: %s", src_dir)
        return

    logging.info("Copying contents from %s -> %s", src_dir, dest_dir)
    if dry_run:
        logging.info("Dry-run enabled; no files will be written.")
    os.makedirs(dest_dir, exist_ok=True)

    for name in os.listdir(src_dir):
        if _should_exclude(name, exclude_names):
            logging.debug("Excluding %s", name)
            continue

        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dest_dir, name)

        if os.path.isdir(src_path):
            if dry_run:
                logging.info("[dry-run] Would copy directory %s -> %s", src_path, dst_path)
            else:
                # Use copytree with dirs_exist_ok when available; fallback if needed
                try:
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                except TypeError:
                    # Older Python: implement copytree contents manually
                    if os.path.exists(dst_path):
                        logging.debug("Destination directory exists, merging contents: %s", dst_path)
                    else:
                        os.makedirs(dst_path, exist_ok=True)
                    for root, dirs, files in os.walk(src_path):
                        rel = os.path.relpath(root, src_dir)
                        target_root = os.path.join(dst_path, rel) if rel != "." else dst_path
                        os.makedirs(target_root, exist_ok=True)
                        for f in files:
                            if _should_exclude(f, exclude_names):
                                logging.debug("Excluding file %s", f)
                                continue
                            sfile = os.path.join(root, f)
                            dfile = os.path.join(target_root, f)
                            shutil.copy2(sfile, dfile)
        else:
            if dry_run:
                logging.info("[dry-run] Would copy file %s -> %s", src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)


def copy_keys_from_source(
    source_root: str,
    dest_root: str,
    keys: Iterable[str],
    exclude_names: Optional[Iterable[str]] = None,
    dry_run: bool = False,
) -> None:
    """
    For each key, copy source_root/key into dest_root/key (contents).
    """
    for key in keys:
        src_dir = os.path.join(source_root, key)
        dest_dir = os.path.join(dest_root, key)
        copy_directory_contents(src_dir, dest_dir, exclude_names=exclude_names, dry_run=dry_run)

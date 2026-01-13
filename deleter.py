"""deleter.py

Simple file deleter utility.
"""

import os


def delete_file(path, ignore_missing=False):
    """Delete the given file. If ignore_missing is True, don't raise if file missing.

    Returns True if file was deleted, False if file was missing and ignore_missing is True.
    """
    if not os.path.exists(path):
        if ignore_missing:
            return False
        raise FileNotFoundError(f"File not found: {path}")
    if os.path.isdir(path):
        raise IsADirectoryError(f"Path is a directory: {path}")
    os.remove(path)
    return True


if __name__ == "__main__":
    import argparse, sys
    p = argparse.ArgumentParser(description="Delete a file")
    p.add_argument("path", help="Path to file to delete")
    p.add_argument("--ignore-missing", action="store_true", help="Don't error if the file is missing")
    args = p.parse_args()
    try:
        deleted = delete_file(args.path, ignore_missing=args.ignore_missing)
        if deleted:
            print(f"Deleted: {args.path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

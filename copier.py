"""copier.py

Simple file copier utility.
"""

import shutil
import os


def copy_file(src, dst):
    """Copy a file from src to dst. Creates destination directories if necessary.

    Raises FileNotFoundError if src does not exist, or PermissionError on failure.
    """
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Source file not found: {src}")
    dst_dir = os.path.dirname(dst) or "."
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)


if __name__ == "__main__":
    import argparse, sys
    p = argparse.ArgumentParser(description="Copy a file")
    p.add_argument("src", help="Source file path")
    p.add_argument("dst", help="Destination file path")
    args = p.parse_args()
    try:
        copy_file(args.src, args.dst)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

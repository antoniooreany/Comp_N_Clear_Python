"""Main CLI for Comp_N_Clear_Python.

Provides copy and delete subcommands.
"""

import argparse
from copier import copy_file
from deleter import delete_file
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="comp_n_clear", description="Copy and delete utilities.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_copy = sub.add_parser("copy", help="Copy a file")
    p_copy.add_argument("src")
    p_copy.add_argument("dst")

    p_del = sub.add_parser("delete", help="Delete a file")
    p_del.add_argument("path")
    p_del.add_argument("--ignore-missing", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "copy":
            copy_file(args.src, args.dst)
            print(f"Copied {args.src} -> {args.dst}")
        elif args.cmd == "delete":
            deleted = delete_file(args.path, ignore_missing=args.ignore_missing)
            if deleted:
                print(f"Deleted {args.path}")
            else:
                print(f"File not found (ignored): {args.path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

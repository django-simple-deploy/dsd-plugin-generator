"""Define CLI for dsd-plugin-genrator."""

import argparse
from pathlib import Path
import sys


def parse_cli():
    parser = argparse.ArgumentParser(description="Plugin generator for django-simple-deploy.")
    parser.add_argument(
        "--target-dir",
        type=str,
        help="Path where the new directory will be written.",
    )
    args = parser.parse_args()

    # If provided, make sure target_dir exists before doing anything else.
    if args.target_dir:
        path = Path(args.target_dir)
        if not path.exists():
            msg = f"The path {path.as_posix()} does not exist."
            msg += "\n  Please create this directory and run the plugin generator again,"
            msg += "\n  or choose another location to write to."
            sys.exit(msg)

    return args
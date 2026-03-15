#!/usr/bin/env python3
"""
Decompile a .pyc file to stdout.

Usage:
    python main.py <file.pyc>
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path so uncompyle6 can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uncompyle6


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.pyc>", file=sys.stderr)
        sys.exit(1)

    pyc_file = sys.argv[1]

    if not os.path.exists(pyc_file):
        print(f"Error: File not found: {pyc_file}", file=sys.stderr)
        sys.exit(1)

    try:
        uncompyle6.decompile_file(pyc_file, sys.stdout)
    except Exception as e:
        print(f"Error decompiling {pyc_file}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

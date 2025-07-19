"""CLI — run subcommand."""
from __future__ import annotations
import argparse
import sys

from .reporters import render
from .runner import run_suite
from .suite import load_suite


def main(argv=None):
    p = argparse.ArgumentParser(prog="speechloop")
    sub = p.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run")
    run_p.add_argument("suite")
    run_p.add_argument("--format", default="text", choices=["text", "json", "html", "md"])
    args = p.parse_args(argv)
    if args.cmd == "run":
        s = load_suite(args.suite)
        sr = run_suite(s)
        sys.stdout.write(render(args.format, sr))
        return 0 if sr.summary["failed"] == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

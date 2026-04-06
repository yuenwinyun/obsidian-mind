#!/usr/bin/env python3
"""Build the release zip for obsidian-mind."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent.parent
EXACT_EXCLUDES = {
    ".DS_Store",
    ".claude/scripts/test_hooks.py",
}
PREFIX_EXCLUDES = (
    ".git/",
    ".github/",
    "thinking/session-logs/",
)


def should_exclude(relative_path: str) -> bool:
    if relative_path in EXACT_EXCLUDES:
        return True
    return any(
        relative_path == prefix[:-1] or relative_path.startswith(prefix)
        for prefix in PREFIX_EXCLUDES
    )


def build_zip(version: str, output_dir: Path) -> Path:
    zip_path = output_dir / f"obsidian-mind-{version}.zip"
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if should_exclude(rel):
                continue
            archive.write(path, rel)
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = build_zip(args.version, output_dir)
    print(zip_path)


if __name__ == "__main__":
    main()

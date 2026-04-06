#!/usr/bin/env python3
"""Validate template metadata consistency."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
MANIFEST = ROOT / "vault-manifest.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def first_release_heading(changelog_text: str) -> tuple[str, str]:
    match = re.search(r"^## v([0-9.]+) — (\d{4}-\d{2}-\d{2})$", changelog_text, re.MULTILINE)
    if not match:
        fail("Could not find a top-level release heading in CHANGELOG.md")
    return match.group(1), match.group(2)


def is_glob(pattern: str) -> bool:
    return any(char in pattern for char in "*?[]")


def normalize_version(version: str) -> str:
    parts = version.split(".")
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
    return ".".join(parts)


def main() -> None:
    changelog_text = CHANGELOG.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    changelog_version, changelog_date = first_release_heading(changelog_text)
    manifest_version = manifest.get("version")
    manifest_date = manifest.get("released")

    if normalize_version(manifest_version) != normalize_version(changelog_version):
        fail(
            "vault-manifest.json version does not match the latest CHANGELOG entry: "
            f"{manifest_version!r} != {changelog_version!r}"
        )

    if manifest_date != changelog_date:
        fail(
            "vault-manifest.json released date does not match the latest CHANGELOG entry: "
            f"{manifest_date!r} != {changelog_date!r}"
        )

    version_parts = changelog_version.split(".")
    major_minor = ".".join(version_parts[:2])
    fingerprint_key = f"v{major_minor}"
    fingerprints = manifest.get("version_fingerprints", {})
    if fingerprint_key not in fingerprints:
        fail(f"Missing version fingerprint for {fingerprint_key}")

    for entry in manifest.get("infrastructure", []):
        if is_glob(entry):
            continue
        path = ROOT / entry
        if not path.exists():
            fail(f"Infrastructure path listed in vault-manifest.json does not exist: {entry}")

    print("Template metadata looks consistent.")


if __name__ == "__main__":
    main()

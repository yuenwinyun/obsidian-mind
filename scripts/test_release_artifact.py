#!/usr/bin/env python3
"""Smoke-test the release artifact contents."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent


class TestReleaseArtifact(unittest.TestCase):
    def test_release_zip_contains_supported_runtime_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_release_zip.py",
                    "--version",
                    "test",
                    "--output-dir",
                    tmp_dir,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
                check=True,
            )
            zip_path = Path(proc.stdout.strip())
            self.assertTrue(zip_path.exists(), zip_path)

            with ZipFile(zip_path) as archive:
                names = set(archive.namelist())

            expected = {
                "AGENTS.md",
                ".codex/README.md",
                ".codex/prompts/standup.md",
                ".codex/prompts/dump.md",
                ".codex/prompts/wrap-up.md",
                "SOUL.md",
                "USER.md",
                "MEMORY.md",
                "HEARTBEAT.md",
                "TOOLS.md",
                "CLAUDE.md",
                "README.md",
            }
            excluded = {
                ".github/workflows/test.yml",
                ".github/workflows/release.yml",
                ".claude/scripts/test_hooks.py",
            }

            for item in expected:
                with self.subTest(expected=item):
                    self.assertIn(item, names)

            for item in excluded:
                with self.subTest(excluded=item):
                    self.assertNotIn(item, names)


if __name__ == "__main__":
    unittest.main()

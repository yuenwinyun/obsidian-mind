#!/usr/bin/env python3
"""End-to-end validation for the Codex-facing vault surface."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class TestCodexSurface(unittest.TestCase):
    def test_codex_entrypoints_exist(self) -> None:
        for relative_path in [
            "AGENTS.md",
            ".codex/README.md",
            ".codex/prompts/standup.md",
            ".codex/prompts/dump.md",
            ".codex/prompts/wrap-up.md",
        ]:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_agents_routes_to_all_prompt_files(self) -> None:
        agents = read_text("AGENTS.md")
        for relative_path in [
            ".codex/prompts/standup.md",
            ".codex/prompts/dump.md",
            ".codex/prompts/wrap-up.md",
        ]:
            with self.subTest(path=relative_path):
                self.assertIn(relative_path, agents)

    def test_prompt_files_cover_expected_workflows(self) -> None:
        expected = {
            ".codex/prompts/standup.md": ["# Standup", "North Star", "Suggested Focus"],
            ".codex/prompts/dump.md": ["# Dump", "Classify", "[[wikilink]]"],
            ".codex/prompts/wrap-up.md": ["# Wrap Up", "Done", "Suggested"],
        }
        for relative_path, snippets in expected.items():
            content = read_text(relative_path)
            for snippet in snippets:
                with self.subTest(path=relative_path, snippet=snippet):
                    self.assertIn(snippet, content)

    def test_docs_expose_codex_support(self) -> None:
        expectations = {
            "README.md": ["Codex", "AGENTS.md", ".codex/prompts/"],
            "CLAUDE.md": ["Codex Compatibility", "AGENTS.md", ".codex/prompts/"],
            "brain/Skills.md": ["Codex Prompt Library", "standup.md", "wrap-up.md"],
            "CONTRIBUTING.md": ["AGENTS.md", ".codex/prompts/", "test_codex_e2e.py"],
        }
        for relative_path, snippets in expectations.items():
            content = read_text(relative_path)
            for snippet in snippets:
                with self.subTest(path=relative_path, snippet=snippet):
                    self.assertIn(snippet, content)

    def test_manifest_tracks_codex_infrastructure(self) -> None:
        manifest = json.loads(read_text("vault-manifest.json"))
        self.assertIn("AGENTS.md", manifest["infrastructure"])
        self.assertIn(".codex/**", manifest["infrastructure"])
        self.assertIn("scripts/**", manifest["infrastructure"])
        self.assertIn("v3.6", manifest["version_fingerprints"])

        for relative_path in manifest["version_fingerprints"]["v3.6"]["exists"]:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_metadata_validator_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/validate_template_metadata.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)


if __name__ == "__main__":
    unittest.main()

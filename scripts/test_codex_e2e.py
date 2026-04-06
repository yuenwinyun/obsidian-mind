#!/usr/bin/env python3
"""Contract validation for the Codex and OpenClaw-facing vault surface."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def normalize_version(version: str) -> str:
    parts = version.split(".")
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
    return ".".join(parts)


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
            "README.md": ["Codex", "OpenClaw", "AGENTS.md", ".codex/prompts/"],
            "CLAUDE.md": ["Codex Compatibility", "OpenClaw Compatibility", "AGENTS.md", ".codex/prompts/"],
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
        latest_key = f"v{normalize_version(manifest['version'])}"
        self.assertIn(latest_key, manifest["version_fingerprints"])

        for relative_path in manifest["version_fingerprints"][latest_key]["exists"]:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_openclaw_workspace_files_exist(self) -> None:
        for relative_path in [
            "SOUL.md",
            "USER.md",
            "MEMORY.md",
            "HEARTBEAT.md",
            "TOOLS.md",
        ]:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_openclaw_docs_reference_workspace_files(self) -> None:
        expectations = {
            "AGENTS.md": ["OpenClaw", "SOUL.md", "USER.md", "MEMORY.md", "HEARTBEAT.md", "TOOLS.md"],
            "README.md": ["OpenClaw", "SOUL.md", "USER.md", "MEMORY.md", "HEARTBEAT.md", "TOOLS.md"],
            "brain/Skills.md": ["OpenClaw Workspace Files", "SOUL.md", "HEARTBEAT.md"],
        }
        for relative_path, snippets in expectations.items():
            content = read_text(relative_path)
            for snippet in snippets:
                with self.subTest(path=relative_path, snippet=snippet):
                    self.assertIn(snippet, content)

    def test_metadata_validator_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/validate_template_metadata.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)

    def test_readme_declares_support_matrix(self) -> None:
        readme = read_text("README.md")
        self.assertIn("### Runtime Support Matrix", readme)
        for runtime in ["Claude Code", "Codex", "OpenClaw"]:
            with self.subTest(runtime=runtime):
                self.assertRegex(readme, re.escape(runtime))


if __name__ == "__main__":
    unittest.main()

"""Run with: python3 -m unittest discover -s tests"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import install_rules  # noqa: E402

START = "<!-- patient-senior:start -->"


class InstallRulesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        (self.home / ".codex").mkdir(parents=True)
        (self.home / ".copilot").mkdir()
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self.env = mock.patch.dict(os.environ, {"HOME": str(self.home),
                                                "PATIENT_SENIOR_CONFIG": str(self.tmp / "none.json")}, clear=False)
        self.env.start()
        os.environ.pop("CODEX_HOME", None)

    def tearDown(self):
        self.env.stop()

    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = install_rules.main(list(argv))
        return code, out.getvalue()

    def test_global_dry_run_writes_nothing(self):
        _, out = self.run_main("--global", "--dry-run")
        self.assertIn("create  codex", out)
        self.assertIn("create  copilot-cli", out)
        self.assertFalse((self.home / ".codex" / "AGENTS.md").exists())

    def test_global_install_then_idempotent(self):
        self.run_main("--global", "--yes")
        agents = (self.home / ".codex" / "AGENTS.md").read_text()
        self.assertTrue(agents.startswith(START))
        self.assertIn("patient-senior is ON", agents)
        self.assertNotIn("{{", agents)
        _, out = self.run_main("--global", "--yes")
        self.assertIn("Nothing to do", out)

    def test_append_keeps_existing_content_and_remove_restores_it(self):
        target = self.repo / "AGENTS.md"
        target.write_text("# My rules\nBe kind.\n")
        self.run_main("--repo", str(self.repo), "--agents", "agents-md", "--yes")
        text = target.read_text()
        self.assertTrue(text.startswith("# My rules\nBe kind.\n\n" + START))
        self.run_main("--repo", str(self.repo), "--agents", "agents-md", "--remove", "--yes")
        self.assertEqual(target.read_text(), "# My rules\nBe kind.\n")

    def test_update_replaces_only_the_block(self):
        target = self.repo / "AGENTS.md"
        target.write_text(f"intro\n\n{START}\nold rule\n<!-- patient-senior:end -->\n\noutro\n")
        _, out = self.run_main("--repo", str(self.repo), "--agents", "agents-md", "--yes")
        self.assertIn("update", out)
        text = target.read_text()
        self.assertNotIn("old rule", text)
        self.assertTrue(text.startswith("intro\n\n" + START))
        self.assertTrue(text.endswith("\noutro\n"))

    def test_cursor_file_gets_always_apply_frontmatter(self):
        self.run_main("--repo", str(self.repo), "--agents", "cursor", "--yes")
        text = (self.repo / ".cursor" / "rules" / "patient-senior.mdc").read_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("alwaysApply: true", text)

    def test_claude_md_import_warning(self):
        (self.repo / "CLAUDE.md").write_text("@AGENTS.md\n")
        _, out = self.run_main("--repo", str(self.repo), "--dry-run")
        self.assertIn("CLAUDE.md imports AGENTS.md", out)

    def test_unknown_agent_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_main("--global", "--agents", "notepad", "--dry-run")


if __name__ == "__main__":
    unittest.main()


class HubSubstitutionTest(InstallRulesTest):
    def test_hub_and_level_flags(self):
        self.run_main("--repo", str(self.repo), "--agents", "agents-md", "--hub", "/vault/Senior", "--level", "light", "--yes")
        text = (self.repo / "AGENTS.md").read_text()
        self.assertIn("/vault/Senior", text)
        self.assertIn("level: light", text)

    def test_no_hub_teaches_in_chat_only(self):
        self.run_main("--repo", str(self.repo), "--agents", "agents-md", "--no-hub", "--yes")
        self.assertIn("no learning hub in this tool", (self.repo / "AGENTS.md").read_text())

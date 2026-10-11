"""Run with: python3 -m unittest discover -s tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "senior_hook.py"


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = self.tmp / "config.json"
        self.config.write_text(json.dumps({"hub": "/vault/Senior", "level": "full"}))
        self.project = self.tmp / "project" / "src"
        self.project.mkdir(parents=True)
        self.env = {**os.environ, "PATIENT_SENIOR_CONFIG": str(self.config),
                    "PATIENT_SENIOR_STATE": str(self.tmp / "state")}
        self.env.pop("PATIENT_SENIOR_LEVEL", None)

    def run_hook(self, command, event, **env):
        event = {"session_id": "s1", "cwd": str(self.project), **event}
        result = subprocess.run([sys.executable, str(HOOK), command], input=json.dumps(event),
                                capture_output=True, text=True, env={**self.env, **env})
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def level_shown(self, out):
        return out.splitlines()[0] if out else ""

    def test_session_start_fills_placeholders(self):
        out = self.run_hook("session-start", {"source": "startup"})
        self.assertIn("level: full", self.level_shown(out))
        self.assertIn("/vault/Senior", out)
        self.assertNotIn("{{", out)

    def test_not_set_up_message(self):
        self.config.write_text("{}")
        self.assertIn("run /senior-setup", self.run_hook("session-start", {}))

    def test_precedence_project_beats_user_and_env_beats_project(self):
        (self.tmp / "project" / ".patient-senior.json").write_text('{"level": "light"}')
        self.assertIn("level: light", self.level_shown(self.run_hook("session-start", {})))
        out = self.run_hook("session-start", {}, PATIENT_SENIOR_LEVEL="deep")
        self.assertIn("level: deep", self.level_shown(out))

    def test_session_level_survives_compaction(self):
        out = self.run_hook("prompt", {"prompt": "/senior light"})
        self.assertIn("now **light**", out)
        out = self.run_hook("session-start", {"source": "compact"})
        self.assertIn("level: light", self.level_shown(out))
        other = self.run_hook("session-start", {"session_id": "s2", "source": "startup"})
        self.assertIn("level: full", self.level_shown(other))

    def test_off_then_on_reinjects_rules(self):
        self.assertIn("OFF for this session", self.run_hook("prompt", {"prompt": "/senior off"}))
        self.assertEqual(self.run_hook("session-start", {"source": "compact"}), "")
        out = self.run_hook("prompt", {"prompt": "/patient-senior:senior"})
        self.assertIn("patient-senior is ON (level: full)", out)

    def test_ordinary_prompts_are_ignored(self):
        self.assertEqual(self.run_hook("prompt", {"prompt": "what does /senior light do?"}), "")
        self.assertEqual(self.run_hook("prompt", {"prompt": "fix the senior engineer bug"}), "")

    def test_subagent_json(self):
        data = json.loads(self.run_hook("subagent-start", {}))["hookSpecificOutput"]
        self.assertEqual(data["hookEventName"], "SubagentStart")
        self.assertIn("teachable", data["additionalContext"])

    def test_level_off_in_user_config_silences_everything(self):
        self.config.write_text('{"level": "off"}')
        self.assertEqual(self.run_hook("session-start", {}), "")
        self.assertEqual(self.run_hook("subagent-start", {}), "")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Inject the patient-senior rules into every Claude Code session and subagent.

Claude Code runs this from the plugin's SessionStart and SubagentStart hooks:
  - SessionStart: plain text on stdout is added to the session's context.
  - SubagentStart: context must be wrapped in hookSpecificOutput JSON.

Settings live in ~/.config/patient-senior/config.json (written by /senior-setup):
  {"hub": "/path/to/vault/Senior", "level": "full"}
Override the location with the PATIENT_SENIOR_CONFIG environment variable.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(os.environ.get("PATIENT_SENIOR_CONFIG", "~/.config/patient-senior/config.json")).expanduser()
LEVELS = {"light", "full", "deep", "off"}
NOT_SET_UP = "(not set up yet - run /senior-setup to choose an Obsidian vault folder)"


def load_config():
    try:
        cfg = json.loads(CONFIG.read_text())
    except (OSError, ValueError):
        cfg = {}
    level = cfg.get("level", "full")
    return {"hub": cfg.get("hub") or NOT_SET_UP, "level": level if level in LEVELS else "full"}


def main():
    subagent = "--subagent" in sys.argv
    cfg = load_config()
    if cfg["level"] == "off":
        return

    rules = (ROOT / "rules" / ("senior-subagent.md" if subagent else "senior-core.md")).read_text()
    rules = rules.replace("{{HUB}}", cfg["hub"]).replace("{{LEVEL}}", cfg["level"])

    if subagent:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": rules}}))
    else:
        sys.stdout.write(rules)


if __name__ == "__main__":
    main()

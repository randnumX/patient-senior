#!/usr/bin/env python3
"""patient-senior hooks for Claude Code.

    senior_hook.py session-start    SessionStart: print the rules (plain text becomes context)
    senior_hook.py subagent-start   SubagentStart: rules for helper agents, as hookSpecificOutput JSON
    senior_hook.py prompt           UserPromptSubmit: track /senior <level> per session

Claude Code passes a JSON object on stdin (session_id, source, cwd, prompt, ...).

Level resolution, first match wins:
  1. this session's saved level (set by /senior <level>; survives /compact and resume)
  2. PATIENT_SENIOR_LEVEL environment variable
  3. .patient-senior.json in the project folder or any parent  -> {"level": "light"}
  4. ~/.config/patient-senior/config.json                     -> {"hub": "...", "level": "full"}
  5. "full"
"""
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(os.environ.get("PATIENT_SENIOR_CONFIG", "~/.config/patient-senior/config.json")).expanduser()
STATE_DIR = Path(os.environ.get("PATIENT_SENIOR_STATE", "~/.local/state/patient-senior/sessions")).expanduser()
LEVELS = ("light", "full", "deep", "off")
NOT_SET_UP = "(not set up yet - run /senior-setup to choose an Obsidian vault folder)"
STATE_MAX_AGE_DAYS = 14
LEVEL_CMD = re.compile(r"^\s*/(?:patient-senior:)?senior(?:\s+(light|full|deep|off|on))?\s*$", re.I)


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def valid(level):
    return level if level in LEVELS else None


def project_level(cwd):
    for folder in [Path(cwd), *Path(cwd).parents]:
        found = folder / ".patient-senior.json"
        if found.is_file():
            return valid(read_json(found).get("level"))
    return None


def state_file(session_id):
    safe = re.sub(r"[^A-Za-z0-9_-]", "", session_id or "")
    return STATE_DIR / f"{safe}.json" if safe else None


def session_level(session_id):
    f = state_file(session_id)
    return valid(read_json(f).get("level")) if f else None


def save_session_level(session_id, level):
    f = state_file(session_id)
    if not f:
        return
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"level": level, "updated": int(time.time())}))
    cutoff = time.time() - STATE_MAX_AGE_DAYS * 86400
    for old in STATE_DIR.glob("*.json"):
        if old.stat().st_mtime < cutoff:
            old.unlink(missing_ok=True)


def resolve(event):
    user = read_json(CONFIG)
    level = (session_level(event.get("session_id"))
             or valid(os.environ.get("PATIENT_SENIOR_LEVEL"))
             or project_level(event.get("cwd") or os.getcwd())
             or valid(user.get("level"))
             or "full")
    return {"level": level, "hub": user.get("hub") or NOT_SET_UP}


def rules(name, cfg):
    text = (ROOT / "rules" / name).read_text()
    return text.replace("{{HUB}}", cfg["hub"]).replace("{{LEVEL}}", cfg["level"])


def session_start(event):
    cfg = resolve(event)
    if cfg["level"] != "off":
        sys.stdout.write(rules("senior-core.md", cfg))


def subagent_start(event):
    cfg = resolve(event)
    if cfg["level"] != "off":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart",
                                                 "additionalContext": rules("senior-subagent.md", cfg)}}))


def prompt(event):
    match = LEVEL_CMD.match(event.get("prompt") or "")
    if not match:
        return
    before = resolve(event)["level"]
    wanted = (match.group(1) or "on").lower()
    if wanted == "on":
        wanted = before if before != "off" else (valid(read_json(CONFIG).get("level")) or "full")
        wanted = "full" if wanted == "off" else wanted
    save_session_level(event.get("session_id"), wanted)
    if wanted == "off":
        sys.stdout.write("patient-senior is now OFF for this session (the user typed /senior off). "
                         "Stop the pre-flights, teaching, side quests and flashcards until it is turned back on.\n")
    elif before == "off":
        sys.stdout.write(rules("senior-core.md", {**resolve(event), "level": wanted}))
    else:
        sys.stdout.write(f"patient-senior level for this session is now **{wanted}** (was {before}). "
                         f"Apply the {wanted} depth from now on.\n")


def main():
    try:
        event = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except ValueError:
        event = {}
    handlers = {"session-start": session_start, "subagent-start": subagent_start, "prompt": prompt}
    command = sys.argv[1] if len(sys.argv) > 1 else "session-start"
    handlers.get(command, session_start)(event if isinstance(event, dict) else {})


if __name__ == "__main__":
    main()

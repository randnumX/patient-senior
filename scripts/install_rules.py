#!/usr/bin/env python3
"""Install patient-senior's rules for AI coding agents other than Claude Code.

    python3 install_rules.py --global --dry-run          # Codex + Copilot CLI, every repository
    python3 install_rules.py --repo . --yes              # AGENTS.md, Copilot, Cursor in this repo
    python3 install_rules.py --repo . --agents cursor --remove --yes

Works from a clone or piped from GitHub:
    curl -fsSL https://raw.githubusercontent.com/randnumX/patient-senior/main/scripts/install_rules.py | python3 - --global --dry-run

The rule is written between <!-- patient-senior:start --> and <!-- patient-senior:end --> markers;
nothing outside the markers is ever changed. Claude Code users get the rule from the plugin instead.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

NAME = "patient-senior"
RULES = "rules/senior-core.md"
CONFIG = Path(os.environ.get("PATIENT_SENIOR_CONFIG", "~/.config/patient-senior/config.json")).expanduser()
NO_HUB = "(no learning hub in this tool - skip writing side-quest, flashcard and profile files; still teach everything in chat)"
RAW = f"https://raw.githubusercontent.com/randnumX/{NAME}/main/{RULES}"
START, END = f"<!-- {NAME}:start -->", f"<!-- {NAME}:end -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def load_rules():
    here = Path(__file__).resolve().parent if "__file__" in globals() and __file__ != "<stdin>" else None
    local = here.parent / RULES if here else None
    if local and local.is_file():
        return local.read_text()
    with urllib.request.urlopen(RAW, timeout=15) as resp:  # piped from curl: fetch the published rules
        return resp.read().decode()


def global_targets():
    home = Path.home()
    codex = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
    return {"codex": (codex / "AGENTS.md", codex.is_dir()),
            "copilot-cli": (home / ".copilot" / "copilot-instructions.md", (home / ".copilot").is_dir())}


def repo_targets(repo):
    return {"agents-md": (repo / "AGENTS.md", True),
            "copilot": (repo / ".github" / "copilot-instructions.md", True),
            "cursor": (repo / ".cursor" / "rules" / f"{NAME}.mdc", True),
            "windsurf": (repo / ".windsurf" / "rules" / f"{NAME}.md", False),
            "cline": (repo / ".clinerules" / f"{NAME}.md", False)}


def user_config():
    try:
        return json.loads(CONFIG.read_text())
    except (OSError, ValueError):
        return {}


def block_for(rules, hub, level):
    rules = rules.replace("{{HUB}}", hub).replace("{{LEVEL}}", level)
    return f"{START}\n{rules.strip()}\n{END}\n"


def new_file_content(path, block):
    if path.suffix == ".mdc":
        return f"---\ndescription: {NAME} rule\nalwaysApply: true\n---\n\n{block}"
    return block


def plan(path, block, remove):
    text = path.read_text() if path.is_file() else None
    has = text is not None and START in text
    if remove:
        return ("remove", None) if has else ("skip", None)
    if text is None:
        return "create", new_file_content(path, block)
    if not has:
        return "append", text.rstrip("\n") + "\n\n" + block
    current = BLOCK_RE.search(text).group(0)
    if current.rstrip("\n") == block.rstrip("\n"):
        return "skip", None
    return "update", BLOCK_RE.sub(lambda _: block, text, count=1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    scope = ap.add_mutually_exclusive_group()
    scope.add_argument("--global", dest="glob", action="store_true", help="user-level files (default)")
    scope.add_argument("--repo", nargs="?", const=".", help="install into this repository (default: .)")
    ap.add_argument("--agents", help="comma-separated subset of agents")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    ap.add_argument("--remove", action="store_true", help="remove the rule block instead")
    ap.add_argument("--yes", action="store_true", help="write without asking")
    ap.add_argument("--hub", help="Obsidian learning-hub folder (default: from ~/.config/patient-senior/config.json)")
    ap.add_argument("--no-hub", action="store_true", help="agents that cannot write to the hub: teach in chat only")
    ap.add_argument("--level", choices=["light", "full", "deep"], help="default depth (default: config, else full)")
    args = ap.parse_args(argv)

    if args.repo:
        repo = Path(args.repo).expanduser().resolve()
        targets = repo_targets(repo)
    else:
        repo, targets = None, global_targets()
    chosen = args.agents.split(",") if args.agents else [k for k, (_, default) in targets.items() if default]
    unknown = [a for a in chosen if a not in targets]
    if unknown:
        sys.exit(f"Unknown agent(s): {', '.join(unknown)}. Choose from: {', '.join(targets)}")
    if not chosen:
        sys.exit("No supported agents detected for --global. Use --agents, or --repo for repository files.")

    cfg = user_config()
    hub = NO_HUB if args.no_hub else (args.hub or cfg.get("hub") or NO_HUB)
    level = args.level or (cfg.get("level") if cfg.get("level") in ("light", "full", "deep") else "full")
    block = "" if args.remove else block_for(load_rules(), hub, level)
    actions = []
    for agent in chosen:
        path = targets[agent][0]
        action, content = plan(path, block, args.remove)
        actions.append((agent, path, action, content))
        print(f"  {action:<7} {agent:<12} {path}")
    if repo and (repo / "CLAUDE.md").is_file() and "@AGENTS.md" in (repo / "CLAUDE.md").read_text() \
            and "agents-md" in chosen and not args.remove:
        print("  note: CLAUDE.md imports AGENTS.md - Claude Code would also get this rule from the file.")

    pending = [a for a in actions if a[2] != "skip"]
    if args.dry_run or not pending:
        print("Dry run - nothing written." if args.dry_run else "Nothing to do.")
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            sys.exit("Re-run with --yes to write (no terminal to ask for confirmation).")
        if input("Write these changes? [y/N] ").strip().lower() != "y":
            print("Cancelled.")
            return 1
    for agent, path, action, content in pending:
        if action == "remove":
            text = BLOCK_RE.sub("", path.read_text()).strip("\n")
            path.write_text(text + "\n" if text else "")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print(f"Done: {len(pending)} file(s) {'cleaned' if args.remove else 'written'}. "
          "Start a fresh session of the agent and ask it to run `ls -la`: it should explain before running.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
name: senior-init
description: >
  Install the patient-senior rules for other AI coding agents - Codex CLI,
  GitHub Copilot (CLI, VS Code), Cursor, Windsurf, Cline - globally or for the
  current repository, so they explain and teach too. Dry run first; never
  touches text outside its markers. Use for /senior-init.
argument-hint: "[global | repo] [--agents ...] [--no-hub] [--level light|full|deep] [--remove]"
---

# /senior-init

All file changes are made by the installer script (exact and tested) - do not edit the files yourself.
Script: `scripts/install_rules.py` at the plugin root (two folders up from this skill's directory).

1. **Dry run** - explain the command, then run it and show the output:
   ```bash
   python3 "<plugin root>/scripts/install_rules.py" --global --dry-run
   ```
   - `--repo .` instead of `--global` for this repository only (`AGENTS.md`, `.github/copilot-instructions.md`,
     `.cursor/rules/` by default).
   - The hub path and level come from `~/.config/patient-senior/config.json`. Use `--no-hub` for teammates or
     agents that should teach in chat without writing Obsidian notes, `--level` to set the depth.
   - Pass `--agents` and `--remove` through from the user's arguments.
2. Warn if the output notes that `CLAUDE.md` imports `AGENTS.md` - Claude Code already gets the rules from the
   plugin hook; suggest `--agents copilot,cursor` to skip `AGENTS.md`.
3. **Ask** the user to confirm, then run the same command with `--yes` instead of `--dry-run`.
4. Tell the user how to verify (a fresh session of that agent, ask it to run `ls -la` - it should explain
   first) and how to undo (`--remove --yes`).

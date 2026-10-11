---
name: senior-setup
description: >
  First-time setup for patient-senior: choose the Obsidian vault folder that
  becomes the learning hub, copy in Senior HQ (dashboard, side-quest and
  session bases, templates, profile, flashcard decks) and write
  ~/.config/patient-senior/config.json. Use for /senior-setup or when the hub
  says "not set up yet".
argument-hint: "[path to Obsidian vault] [folder name, default Senior]"
---

# /senior-setup

Follow the patient-senior rules while doing this: explain each step and command before running it.

1. **Find the vault.** If the user gave a path, use it. Otherwise look for folders containing `.obsidian/`
   (e.g. `find ~ -maxdepth 4 -type d -name .obsidian -not -path "*/Library/*" 2>/dev/null`), explain the
   command, and ask the user to pick one. Confirm the folder name for the hub (default `Senior`).
2. **Copy the templates without overwriting.** Source: `templates/vault/` at the plugin root (two folders up
   from this skill's directory). Destination: `<vault>/<folder>/`. Copy every file whose destination does
   not exist yet (`cp -Rn` is the no-clobber copy; explain `-R` recursive and `-n` no-clobber). List what was
   created and what was skipped because it already existed.
3. **Write the config.** Create `~/.config/patient-senior/config.json` (`mkdir -p` the folder first) with:
   ```json
   {"hub": "<absolute path to vault>/<folder>", "level": "full"}
   ```
   Keep any keys that already exist in the file; only set `hub` (and `level` if missing).
4. **Check Obsidian features.**
   - Bases: core plugin - check `<vault>/.obsidian/core-plugins.json` has `"bases": true`; if not, tell the
     user: Settings -> Core plugins -> Bases.
   - Spaced Repetition: community plugin folder `<vault>/.obsidian/plugins/obsidian-spaced-repetition`. If
     missing, tell the user: Settings -> Community plugins -> Browse -> "Spaced Repetition" (by
     st3v3nmw) -> Install -> Enable. Cards are plain Markdown and work without it; the plugin adds review
     and scheduling.
5. **Finish.** Tell the user to open `<folder>/Senior HQ.md` in Obsidian, and that the always-on mode
   starts with their next Claude Code session (the hook reads the new config). Offer `/senior status`.

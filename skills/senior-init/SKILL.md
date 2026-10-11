---
name: senior-init
description: >
  Write the patient-senior rules into the current repository's instruction
  files for other AI coding tools (AGENTS.md, GitHub Copilot, Cursor,
  Windsurf, Cline) so they explain and teach too. Dry run first; never
  overwrites. Use for /senior-init.
argument-hint: "[--dry-run | --only agents|copilot|cursor|windsurf|cline]"
---

# /senior-init

Source rules: `rules/senior-core.md` at the plugin root (two folders up from this skill's directory).
Replace `{{LEVEL}}` with the configured level (default `full`) and `{{HUB}}` with the configured hub path, or
with "the learning hub is not available in this tool; skip side-quest and flashcard files" for teammates who
do not use Obsidian.

Targets (repo root):

| Tool | File |
|---|---|
| Many agents (Codex, OpenCode, Claude Code via `@AGENTS.md`) | `AGENTS.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/patient-senior.mdc` (frontmatter `alwaysApply: true`) |
| Windsurf | `.windsurf/rules/patient-senior.md` |
| Cline | `.clinerules/patient-senior.md` |

Steps:
1. **Dry run first** (always, unless the user passed `--force`): for each target say *create*, *append* (file
   exists without our block) or *skip* (block already present). Show the list and ask before writing.
2. Wrap the rules in markers so they can be updated or removed later:
   `<!-- patient-senior:start -->` ... `<!-- patient-senior:end -->`. When appending to an existing file,
   add the block at the end and change nothing else.
3. Warn when `AGENTS.md` is imported by a `CLAUDE.md` (`@AGENTS.md`): Claude Code will then load the rules
   from the file as well as from the plugin hook - suggest `--only` to skip it.
4. Report what was written and how to remove it (delete the marked block).

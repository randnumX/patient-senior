# Changelog

All notable changes to patient-senior. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [0.2.0] - 2026-10-11
### Added
- `UserPromptSubmit` hook: `/senior <level>` is remembered per session and survives `/compact`; `/senior` after `/senior off` re-injects the rules.
- Level priority: session, `PATIENT_SENIOR_LEVEL`, `.patient-senior.json` in the project, user config, `full`.
- `/senior-stats`: side quests, cards due, sessions and streak, mastered items - counted by a script.
- `scripts/install_rules.py`: install the rules for Codex, Copilot, Cursor, Windsurf and Cline without Claude Code.
- Unit tests, CI, contributing and security docs.
### Changed
- `/senior-init` now calls the installer script.
- Pairs with command-anatomy for aligned command trees.

## [0.1.0] - 2026-10-11
### Added
- Always-on mentor mode: pre-flights, command breakdowns with recall challenges, professor-style teaching, decision points, senior lens.
- Side quests and Obsidian Spaced Repetition flashcards in a Senior HQ learning hub.
- Skills: senior, senior-setup, sidequest, sidequests, flashcards, quiz, recap, senior-init.

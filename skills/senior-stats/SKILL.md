---
name: senior-stats
description: >
  Show learning statistics from the patient-senior hub: side quests by status
  and what is up next, flashcards per deck with cards due for review and never
  reviewed, sessions and streak, and mastered concepts and commands. Use for
  /senior-stats, "how am I doing", "what should I review".
argument-hint: "[--json]"
---

# /senior-stats

Counting is done by a script so the numbers are exact - never estimate them yourself.

1. Run (read-only, explain it as usual):
   ```bash
   python3 "<this skill's directory>/scripts/stats.py"
   ```
   It reads the hub path from `~/.config/patient-senior/config.json`; pass a path to override, `--json` for
   machine-readable output.
2. Show the output verbatim in a `text` block.
3. Add at most three lines of advice, based only on the numbers:
   - cards due -> "review N due cards (Obsidian: Spaced Repetition: Review flashcards)";
   - a high-priority or long-waiting side quest -> offer `/sidequests <title>`;
   - many cards never reviewed -> suggest installing or opening the Spaced Repetition plugin;
   - a streak -> name it, briefly.

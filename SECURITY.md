# Security

## What runs on your machine

patient-senior is mostly Markdown instructions. The only code is small, dependency-free Python:

- `hooks/senior_hook.py` - runs at session start, helper-agent start and on each prompt. Reads `~/.config/patient-senior/config.json` and an optional `.patient-senior.json`, writes small per-session level files to `~/.local/state/patient-senior/sessions/` (auto-deleted after 14 days). No network.
- `skills/senior-stats/scripts/stats.py` - read-only; counts files in your learning hub. No network.
- `scripts/install_rules.py` - writes only between its markers in the instruction files you choose; when piped from `curl` it downloads `rules/senior-core.md` from this repository.
- The agent itself writes Markdown notes into the learning-hub folder you chose in `/senior-setup`, and nowhere else on its own initiative.

There is no telemetry and no background process.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting (Security tab -> "Report a vulnerability") rather than a
public issue.

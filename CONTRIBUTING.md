# Contributing to patient-senior

Thanks for helping. Issues and pull requests are welcome.

## Run the checks

```bash
python3 -m unittest discover -s tests      # unit tests (no dependencies)
claude plugin validate .                   # marketplace manifest
claude plugin validate .claude-plugin/plugin.json
claude plugin validate skills
claude plugin eval . --runs 1 --no-publish # behaviour evals, with vs without the plugin (uses your Claude account)
```

## Ground rules

- **Rules are code.** A change to anything in `rules/` or a `SKILL.md` changes how agents behave. Describe the
  behaviour you saw before and after, and run the evals - models follow instructions differently, and a
  wording that looks better can work worse.
- **Scripts do the exact work, the model does the judgement.** Counting, aligning and editing files belong in
  tested Python with no dependencies beyond the standard library.
- **Honest numbers only.** Do not claim savings, accuracy or learning gains in docs without a reproducible
  measurement in `evals/`.
- Keep `CHANGELOG.md` up to date and bump `version` in `.claude-plugin/plugin.json` for releases.
